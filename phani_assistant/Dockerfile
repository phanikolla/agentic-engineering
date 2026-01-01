FROM public.ecr.aws/docker/library/python:3.11-slim

# Install Lambda Web Adapter
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY me/ ./me/

# Set environment variables for Lambda Web Adapter
ENV PORT=7860
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860
ENV AWS_LWA_INVOKE_MODE=response_stream

# Run the application
CMD ["python", "app.py"]
