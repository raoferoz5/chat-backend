FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Grant execution permissions to the startup shell script
RUN chmod +x start.sh

EXPOSE 8000

# Tell Docker to execute the shell script on startup
CMD ["./start.sh"]