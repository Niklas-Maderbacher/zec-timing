FROM python:3.14-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Define environment variable
ENV FLASK_APP=app/main.py
ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]