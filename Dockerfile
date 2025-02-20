FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
COPY ./main.py .
COPY ./src ./src
ENTRYPOINT [ "python", "main.py" ]
