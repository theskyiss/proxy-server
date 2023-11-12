# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir aiohttp bs4 lxml
EXPOSE 8232
CMD ["python", "proxy-server.py"]
