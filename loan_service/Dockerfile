FROM python:3.11-slim
WORKDIR /app
COPY . .
COPY ../common_libs ./common_libs
ENV PYTHONPATH="${PYTHONPATH}:/app/common_libs"
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
