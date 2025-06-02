FROM python:3.11-slim

WORKDIR /app

# Copy loan_service code
COPY loan_service/ .

# Copy shared libs
COPY common_libs ./common_libs

# Set PYTHONPATH so both app and common_libs are importable
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]

