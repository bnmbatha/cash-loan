FROM python:3.11-slim

WORKDIR /app

# Copy all source files and configuration
COPY loan_service/ .
COPY common_libs ./common_libs
COPY loan_service/requirements.txt .
COPY alembic.ini .
COPY alembic ./alembic

# Set environment for internal imports
ENV PYTHONPATH=/app/common_libs

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install alembic

# Run Alembic migration before starting app
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8001"]
