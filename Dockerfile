FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Export environment variables from env.txt
# Format: VAR=VALUE (no quotes, no spaces around =)
# Example:
# PG_HOST=localhost
# PG_USER=postgres
# PG_PASSWORD=admin

# Set environment variables at build time
RUN export $(cat env.txt | xargs)

EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "postgres:app", "--host", "0.0.0.0", "--port", "8000"]
