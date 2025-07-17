import os
import sys
import logging
import datetime
from datetime import datetime, timedelta
from typing import Any, List, Dict, Optional, Union, AsyncIterator
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

import asyncpg
import psycopg2
from dotenv import load_dotenv

from mcp.server.fastmcp.server import FastMCP, Context
app = FastMCP("appointments")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("server_module")

# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection parameters (Docker-friendly)
# PG_HOST = os.getenv('PG_HOST', 'localhost')  # Use Docker service name if in same Docker network
# PG_PORT = int(os.getenv('PG_PORT', 5432))
# PG_USER = os.getenv('PG_USER', 'postgres')
# PG_PASSWORD = os.getenv('PG_PASSWORD', 'postgres')  # Replace with your real password
# PG_DATABASE = os.getenv('PG_DATABASE', 'MCP_agenda')

# Database connection parameters
# connection_params = {
#     'host': os.getenv('PG_HOST', 'localhost'),  
#     'port': int(os.getenv('PG_PORT', "5432")),
#     'database': os.getenv('PG_DATABASE', 'MCP_agenda'),
#     'user': os.getenv('PG_USER', 'postgres'),
#     'password': os.getenv('PG_PASSWORD', 'postgres')
# }
connection_params = {
        'host': 'localhost',
        'port': 5432,
        'database': 'MCP_agenda',
        'user': 'postgres',
        'password': 'postgres'
    }

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Manage application lifecycle with type-safe context"""
    logger.debug("Initializing PostgreSQL database connection")
    conn = None
    try:
        conn = await asyncpg.connect(**connection_params)
        logger.debug("PostgreSQL connection established successfully")
        yield {"conn": conn}
    except Exception as e:
        logger.error(f"PostgreSQL connection error: {type(e).__name__}: {str(e)}", exc_info=True)
        yield {"conn": None}
    finally:
        if conn:
            logger.debug("Closing PostgreSQL connection")
            await conn.close()

# Initialize FastMCP server with lifespan context
mcp = FastMCP("appointments", lifespan=app_lifespan)


# retrieve data and filter by date
@mcp.tool()
async def retrieve_data_date(
    ctx: Context,
    date_appointment_start: Optional[str] = None,
    date_appointment_end: Optional[str] = None,
    limit: Optional[int] = None
) -> Union[Dict[str, Any], None]:
    """
    Retrieve agenda data filtered by appointment date.

    Args:
        date_appointment_start: First date of the appointment in YYYY-MM-DD format (column appointment_date in agenda table)
        date_appointment_end: Optional second date of the appointment in YYYY-MM-DD format (column appointment_date in agenda table)
        limit: Optional limit for number of rows

    Returns:
        Dictionary with appointments data, or None if error occurs
    """
    try:
        # Get connection from lifespan context
        conn = ctx.request_context.lifespan_context.get("conn")

        if conn is None:
            logger.error("Database connection is not available")
            return None

        # Validate input
        if not date_appointment_start and not date_appointment_end:
            logger.error("At least one of date_appointment_start or date_appointment_end must be provided")
            return None

        # Parse dates
        if date_appointment_start:
            appointment_date_obj1 = datetime.strptime(date_appointment_start, "%Y-%m-%d").date()
        if date_appointment_end:
            appointment_date_obj2 = datetime.strptime(date_appointment_end, "%Y-%m-%d").date()

        # Build query and parameters
        if not date_appointment_end:
            query = """
            SELECT t2.patient_name,
                t2.patient_address,
                t2.patient_phonenumber,
                t1.appointment_date,
                t1.start_hour,
                t1.end_hour,
                t3.appointment_type,
                t3.hourly_rate
            FROM agenda as t1
            LEFT JOIN patients as t2 ON t1.patient_id = t2.id
            LEFT JOIN appointment_types as t3 ON t1.appointment_id = t3.id
            WHERE t1.appointment_date = $1
            """
            params = [appointment_date_obj1]
            if limit:
                query += " LIMIT $2"
                params.append(limit)
            rows = await conn.fetch(query, *params)
        else:
            query = """
            SELECT t2.patient_name,
                t2.patient_address,
                t2.patient_phonenumber,
                t1.appointment_date,
                t1.start_hour,
                t1.end_hour,
                t3.appointment_type,
                t3.hourly_rate
            FROM agenda as t1
            LEFT JOIN patients as t2 ON t1.patient_id = t2.id
            LEFT JOIN appointment_types as t3 ON t1.appointment_id = t3.id
            WHERE t1.appointment_date >= $1 AND t1.appointment_date <= $2
            ORDER BY t1.appointment_date
            """
            params = [appointment_date_obj1, appointment_date_obj2]
            if limit:
                query += " LIMIT $3"
                params.append(limit)
            rows = await conn.fetch(query, *params)

        appointments = [dict(row) for row in rows]

        result = {
            "status": "success",
            "count": len(appointments),
            "date_start": date_appointment_start,
            "date_end": date_appointment_end if date_appointment_end else date_appointment_start,
            "appointments": appointments
        }

        logger.info(f"Successfully retrieved {len(appointments)} rows for selected dates")
        return result

    except asyncpg.PostgresError as e:
        logger.error(f"PostgreSQL error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error retrieving data for selected dates: {e}")
        return None



# retrieve data and filter by patient
@mcp.tool()
async def retrieve_data_patient(
    ctx: Context,
    patient_name: Optional[str] = None,
    patient_id: Optional[str] = None,
    limit: Optional[int] = None
) -> Union[Dict[str, Any], None]:
    """
    Retrieve agenda data filtered by patient.

    Args:
        patient_name: Name of the patient (column name in patients table)
        patient_id: Patient ID (column patient_id in patients table and agenda table)
        limit: Optional limit for number of rows

    Returns:
        Dictionary with appointments data, or None if error occurs
    """
    if not patient_name and not patient_id:
        logger.error("At least one of patient_name or patient_id must be provided")
        return None

    try:
        # Get connection from lifespan context
        conn = ctx.request_context.lifespan_context.get("conn")

        if conn is None:
            logger.error("Database connection or cursor is not available")
            return None

        if patient_id:
            query = """
            SELECT t2.patient_name,
                t2.patient_address,
                t2.patient_phonenumber,
                t1.appointment_date,
                t1.start_hour,
                t1.end_hour,
                t3.appointment_type,
                t3.hourly_rate
            FROM agenda as t1
            LEFT JOIN patients as t2 ON t1.patient_id = t2.id
            LEFT JOIN appointment_types as t3 ON t1.appointment_id = t3.id
            WHERE t1.patient_id = $1
            """
            params = [patient_id]
            if limit:
                query += " LIMIT $2"
                params.append(limit)
            rows = await conn.fetch(query, *params)
        else:
            query = """
            SELECT t2.patient_name,
                t2.patient_address,
                t2.patient_phonenumber,
                t1.appointment_date,
                t1.start_hour,
                t1.end_hour,
                t3.appointment_type,
                t3.hourly_rate
            FROM agenda as t1
            LEFT JOIN patients as t2 ON t1.patient_id = t2.id
            LEFT JOIN appointment_types as t3 ON t1.appointment_id = t3.id
            WHERE t2.name ILIKE $1
            """
            params = [patient_name]
            if limit:
                query += " LIMIT $2"
                params.append(limit)
            rows = await conn.fetch(query, *params)

        appointments = [dict(row) for row in rows]

        result = {
            "status": "success",
            "count": len(appointments),
            "patient_name": patient_name,
            "patient_id": patient_id,
            "appointments": appointments
        }

        logger.info(
            f"Successfully retrieved {len(appointments)} rows for "
            f"{'patient number ' + patient_id if patient_id else 'patient name ' + str(patient_name)}"
        )

        return result

    except asyncpg.PostgresError as e:
        logger.error(f"PostgreSQL error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error retrieving data for selected patient: {e}")
        return None


# retrieve data and filter by appointment_type
@mcp.tool()
async def retrieve_data_appointmentType(
    ctx: Context,
    appointment_type: Optional[str] = None,
    appointment_id: Optional[str] = None,
    limit: Optional[int] = None
) -> Union[Dict[str, Any], None]:
    """
    Retrieve agenda data filtered by appointment type.

    Args:
        appointment_type: Name of the appointment type (column name in appointment_types table)
        appointment_id: ID of the appointment type (column appointment_id in appointment_types table and agenda table)
        limit: Optional limit for number of rows

    Returns:
        Dictionary with appointments data, or None if error occurs
    """
    if not appointment_type and not appointment_id:
        logger.error("At least one of appointment_type or appointment_id must be provided")
        return None

    try:
        # Get connection from lifespan context
        conn = ctx.request_context.lifespan_context.get("conn")

        if conn is None:
            logger.error("Database connection is not available")
            return None

        if appointment_id:
            query = """
            SELECT t2.patient_name,
                t2.patient_address,
                t2.patient_phonenumber,
                t1.appointment_date,
                t1.start_hour,
                t1.end_hour,
                t3.appointment_type,
                t3.hourly_rate
            FROM agenda as t1
            LEFT JOIN patients as t2 ON t1.patient_id = t2.id
            LEFT JOIN appointment_types as t3 ON t1.appointment_id = t3.id
            WHERE t1.appointment_id = $1
            """
            params = [int(appointment_id)]
            if limit:
                query += " LIMIT $2"
                params.append(limit)
            rows = await conn.fetch(query, *params)
        else:
            query = """
            SELECT t2.patient_name,
                t2.patient_address,
                t2.patient_phonenumber,
                t1.appointment_date,
                t1.start_hour,
                t1.end_hour,
                t3.appointment_type,
                t3.hourly_rate
            FROM agenda as t1
            LEFT JOIN patients as t2 ON t1.patient_id = t2.id
            LEFT JOIN appointment_types as t3 ON t1.appointment_id = t3.id
            WHERE t3.appointment_type ILIKE $1
            """
            params = [appointment_type]
            if limit:
                query += " LIMIT $2"
                params.append(limit)
            rows = await conn.fetch(query, *params)

        appointments = [dict(row) for row in rows]

        result = {
            "status": "success",
            "count": len(appointments),
            "appointment_type": appointment_type,
            "appointment_id": appointment_id,
            "appointments": appointments
        }

        if appointment_id:
            logger.info(f"Successfully retrieved {len(appointments)} rows for appointment ID {appointment_id}")
        else:
            logger.info(f"Successfully retrieved {len(appointments)} rows for appointment type {appointment_type}")

        return result

    except asyncpg.PostgresError as e:
        logger.error(f"PostgreSQL error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error retrieving data for selected appointment type: {e}")
        return None


# Get info by id
@mcp.tool()
async def get_agenda_by_id(ctx: Context, id: int) -> Dict[str, Any] | None:
    """
    Retrieve agenda data by ID.
    
    Args:
        id: ID of the appointment (column id in agenda table)
    
    Returns:
        Dictionary with appointment details or None if error occurs
    """
    try:
        # Get connection from lifespan context
        conn = ctx.request_context.lifespan_context.get("conn")

        if conn is None:
            logger.error("Database connection is not available")
            return None
        
        query = """
        SELECT t2.patient_name,
            t2.patient_address,
            t2.patient_phonenumber,
            t1.appointment_date,
            t1.start_hour,
            t1.end_hour,
            t3.appointment_type,
            t3.hourly_rate
        FROM agenda as t1
        LEFT JOIN patients as t2 ON t1.patient_id = t2.id
        LEFT JOIN appointment_types as t3 ON t1.appointment_id = t3.id
        WHERE t1.id = $1
        """
        row = await conn.fetchrow(query, id)
        
        if row is None:
            logger.warning(f"No appointment found with ID {id}")
            return None
        
        result = dict(row)
        
        logger.info(f"Successfully retrieved appointment with ID {id}")
        return result

    except asyncpg.PostgresError as e:
        logger.error(f"PostgreSQL error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error retrieving appointment by ID {id}: {e}")
        return None

@mcp.tool()
async def get_week_summary(ctx: Context,
                           date: Optional[str] = None,
                           week_number: Optional[int] = None,
                           year: Optional[int] = None) -> Dict[str, Any] | None:
    """
    Get a summary of appointments for a specific week including a Gantt chart visualization.
    
    Args:
        date: Date string in YYYY-MM-DD format representing the first day of the week
        week_number: Optional week number (1-53)
        year: Optional year (defaults to current year)
    
    Returns:
        Dictionary with weekly summary and Gantt chart data or None if error occurs
    """
    try:
        conn = ctx.request_context.lifespan_context.get("conn")

        if conn is None:
            logger.error("Database connection is not available")
            return None

        # Use current year if not specified
        if year is None:
            year = datetime.now().year

        # Get week start based on input date or week number
        if date:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            week_start = date_obj
            week_end = date_obj + timedelta(days=6)
        elif week_number:
            # Get week start and end dates
            query = """
            SELECT 
                date_trunc('week', make_date($1, 1, 1) + ($2::int - 1) * '1 week'::interval) as week_start,
                date_trunc('week', make_date($1, 1, 1) + ($2::int - 1) * '1 week'::interval) + '6 days'::interval as week_end
            """
            week_dates = await conn.fetchrow(query, year, week_number)
            week_start = week_dates['week_start']
            week_end = week_dates['week_end']
        else:
            logger.error("Either date or week_number must be provided")
            return None

        # Get appointments for the week
        query = """
        SELECT 
            t2.patient_name,
            t1.appointment_date,
            t1.start_hour,
            t1.end_hour,
            t3.appointment_type
        FROM agenda t1
        LEFT JOIN patients t2 ON t1.patient_id = t2.id
        LEFT JOIN appointment_types t3 ON t1.appointment_id = t3.id
        WHERE t1.appointment_date BETWEEN $1 AND $2
        ORDER BY t1.appointment_date, t1.start_hour
        """
        params = [week_start, week_end]
        rows = await conn.fetch(query, *params)
        appointments = [dict(row) for row in rows]

        # Calculate summary statistics
        total_appointments = len(appointments)
        unique_patients = len(set(app['patient_name'] for app in appointments))
        appointment_types = {}
        for app in appointments:
            appointment_types[app['appointment_type']] = appointment_types.get(app['appointment_type'], 0) + 1

        # Create daily appointment counts
        daily_counts = {}
        for app in appointments:
            date_str = app['appointment_date'].strftime('%Y-%m-%d')
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1

        result = {
            "status": "success",
            "week_start": week_start.strftime('%Y-%m-%d'),
            "week_end": week_end.strftime('%Y-%m-%d'),
            "total_appointments": total_appointments,
            "unique_patients": unique_patients,
            "appointment_types": appointment_types,
            "daily_counts": daily_counts,
            "appointments": appointments
        }

        logger.info(f"Successfully retrieved week summary with {total_appointments} appointments")
        return result

    except asyncpg.PostgresError as e:
        logger.error(f"PostgreSQL error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error retrieving week summary: {e}")
        return None


@mcp.prompt()
def appointments_resume(date: str) -> str:
    """Create a summary report prompt for appointments."""
    return f"""You are an appointments manager. Give me a resume of appointments for this date: {date}?"""



# Define tools for the MCP server: create appointment
@mcp.tool()
async def create_appointment(
    ctx: Context,
    patient_name: str,
    appointment_date: Optional[str] = None,
    appointment_type: str = "General Consultation",
    start_time: Optional[str] = None,
    duration: int = 30,
    patient_address: Optional[str] = None,
    patient_phone: Optional[str] = None
) -> Dict[str, Any] | None:
    """
    Create a new appointment and patient if needed.
    
    Args:
        patient_name: Name of the patient
        appointment_date: Date of appointment (YYYY-MM-DD)
        appointment_type: Type of appointment (e.g. 'General Consultation')
        start_time: Start time of appointment in HH:MM format
        duration: Duration of the appointment in minutes
        patient_address: Optional address of the patient
        patient_phone: Optional phone number
    
    Returns:
        Dictionary with appointment details or None if error occurs
    """
    try:
        logger.info("Attempting to create appointment")
        conn = ctx.request_context.lifespan_context["conn"]
        cursor = ctx.request_context.lifespan_context.get("cursor")

        if conn is None or cursor is None:
            logger.error("Database connection or cursor is not available")
            return None

        async with conn.transaction():
            logger.info(f"Checking if patient '{patient_name}' exists...")
            query = """SELECT patient_number FROM patients WHERE name = %s"""
            params = (patient_name,)
            await cursor.execute(query, params)
            patient = await cursor.fetchone()

            if not patient:
                logger.info(f"Patient '{patient_name}' not found. Creating new patient...")
                last_patient_number = await cursor.fetchval(
                    'SELECT patient_number FROM patients order by patient_number desc limit 1'
                )
                if last_patient_number is None:
                    patient_number = "P001"
                else:
                    patient_number = f"P{int(last_patient_number[1:]) + 1:03d}"
                patient_number = await cursor.fetchval(
                    'INSERT INTO patients (patient_number, name, address, phonenumber) VALUES ($1, $2, $3, $4) RETURNING patient_number',
                    patient_number, patient_name, patient_address, patient_phone
                )
                logger.info(f"Created new patient with number: {patient_number}")

            else:
                patient_number = patient['patient_number']
                logger.info(f"Found existing patient with number: {patient_number}")


            logger.info(f"Checking if appointment type '{appointment_type}' exists...")
            appointment_type_record = await conn.fetchrow(
                'SELECT appointment_number FROM appointment_types WHERE name = $1',
                appointment_type
            )

            if not appointment_type_record:
                logger.info(f"Appointment type '{appointment_type}' not found. Creating new type...")
                appointment_number = await cursor.fetchval(
                    'INSERT INTO appointment_types (name) VALUES ($1) RETURNING appointment_number',
                    appointment_type
                )
                logger.info(f"Created new appointment type with appointment_number: {appointment_number}")
            else:
                appointment_number = appointment_type_record['appointment_number']
                logger.info(f"Found existing appointment type with appointment_number: {appointment_number}")

            


            logger.info("Formatting start and end times...")
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            start_time_obj = datetime.strptime(start_time, '%H:%M').time()
            start_dt = datetime.combine(appointment_date, start_time_obj)
            end_dt = start_dt + timedelta(minutes=duration)

            logger.info("calculating id ...")
            id_max = await conn.fetchval('SELECT max(id) as max_id FROM agenda')
            id_record = id_max + 1 if id_max else 1
            logger.info(f"ID of new record: {id_record}")

            logger.info("Inserting appointment into agenda...")
            appointment = await conn.fetchrow(
                '''
                INSERT INTO agenda (id, patient_number, appointment_type, appointment_date, start_hour, end_hour)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING *
                ''',
                id_record, patient_number, appointment_number, appointment_date, start_dt.time(), end_dt.time()
            )

            logger.info("Appointment successfully created")
            return dict(appointment)

    except psycopg2.Error as e:
        logger.error(f"PostgreSQL error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None


# Define tools for the MCP server: get number of rows in appointments table
@mcp.tool()
async def get_agenda_summary(ctx: Context) -> Dict[str, Any] | None:
    """
    Get a summary of the agenda system including appointment counts and averages.
    
    Returns:
        Dictionary with summary statistics or None if error occurs
    """
    try:
        conn = ctx.request_context.lifespan_context["conn"]
        cursor = ctx.request_context.lifespan_context.get("cursor")

        if conn is None or cursor is None:
            logger.error("Database connection or cursor is not available")
            return None
        
        # Get total appointments
        total_appointments = await cursor.fetchval('SELECT COUNT(*) FROM agenda')

        # Get total patients
        total_patients = await cursor.fetchval('SELECT COUNT(*) FROM patients')
        
        # Get daily average (last 30 days)
        daily_avg = await cursor.fetchval('''
            SELECT ROUND(AVG(count), 2) FROM (
                SELECT DATE(appointment_date), COUNT(*) as count 
                FROM agenda 
                WHERE appointment_date >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY DATE(appointment_date)
            ) as daily
        ''')
        
        # Get weekly average (last 12 weeks)
        weekly_avg = await cursor.fetchval('''
            SELECT ROUND(AVG(count), 2) FROM (
                SELECT DATE_TRUNC('week', appointment_date), COUNT(*) as count 
                FROM agenda 
                WHERE appointment_date >= CURRENT_DATE - INTERVAL '12 weeks'
                GROUP BY DATE_TRUNC('week', appointment_date)
            ) as weekly
        ''')
        
        # Get monthly average (last 12 months)
        monthly_avg = await cursor.fetchval('''
            SELECT ROUND(AVG(count), 2) FROM (
                SELECT DATE_TRUNC('month', appointment_date), COUNT(*) as count 
                FROM agenda 
                WHERE appointment_date >= CURRENT_DATE - INTERVAL '12 months'
                GROUP BY DATE_TRUNC('month', appointment_date)
            ) as monthly
        ''')
        
        logger.info("Successfully retrieved agenda summary")
        return {
            "total_appointments": total_appointments,
            "total_patients": total_patients,
            "daily_average": daily_avg or 0,
            "weekly_average": weekly_avg or 0,
            "monthly_average": monthly_avg or 0
        }
            
    except psycopg2.Error as e:
        logger.error(f"PostgreSQL error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error getting agenda summary: {e}")
        return None


if __name__ == "__main__":
    # Initialize and run the server
    try:
        logger.info("Starting MCP server")
        mcp.run(transport='stdio')
    except Exception as e:
        logger.critical(f"Server startup failed: {e}", exc_info=True)
        sys.exit(1)
