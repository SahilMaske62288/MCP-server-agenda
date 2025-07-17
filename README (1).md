# MCP PostgreSQL Server

## Overview
This project implements a Multi-Channel Processing (MCP) server that integrates with PostgreSQL databases. It features Claude AI for handling user interactions and provides a robust interface for database operations.

## Features
- PostgreSQL database integration
- Claude AI powered responses
- Multi-channel request processing
- Customizable tools and commands
- Asynchronous data handling

## Prerequisites
- Python 3.8+
- PostgreSQL
- Required Python packages (see requirements.txt)

## Installation
```bash
git clone <repository-url>
cd mcp-postgres
pip install -r requirements.txt
```

## Configuration
1. Launch the PostgreSQL database using Docker Compose:

    ```bash
    services:
        postgres:
            image: postgres:16
            container_name: agenda_local_postgres
            restart: always
                environment:
                POSTGRES_USER: "postgres"
                POSTGRES_PASSWORD: "postgres"
                POSTGRES_DB: "MCP_agenda"
            ports:
                - "5432:5432"
            volumes:
                - postgres_data:/var/lib/postgresql/data
                - ./db init:/docker-entrypoint-initdb.d  # Mount SQL init script
                - ./csv:/csv  # mount csv folder

        volumes:
            postgres_data:
    ```

    ```bash
    docker-compose up -d
    ```
    Ensure you have a `docker-compose.yml` file configured with your PostgreSQL settings.
2. Configure Claude AI credentials
3. Define custom tools and commands

## Usage
```bash
python main.py
```

## Documentation
For detailed documentation about tools and commands, see `/docs`.

## License
MIT License

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## Authors
- Your Name

## Acknowledgments
- Claude AI
- PostgreSQL Team