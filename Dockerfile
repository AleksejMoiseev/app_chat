FROM python:3.8
WORKDIR /app
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requrements.txt