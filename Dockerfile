FROM python:3.10

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Install gpu dependencies
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt install -y libgl1-mesa-glx -y

# Copy local code to the container image
WORKDIR /app
ADD . .

RUN pip install -r requirements.txt
ENTRYPOINT ["gunicorn","--bind=0.0.0.0:8080","app:app"]