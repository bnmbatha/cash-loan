FROM python:3.11-slim

WORKDIR /app

# Copy from root project (you’ll run docker build from root: `cash-loan/`)
COPY loan_service/ .                      # Copy loan_service contents
COPY common_libs /app/common_libs         # Copy common_libs folder
COPY loan_service/requirements.txt .      # Requirements

# Make common_libs importable
ENV PYTHONPATH=/app:/app/common_libs

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]


