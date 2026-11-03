FROM python:latest
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENV TIDEWATCH_API_KEY=sk-demo-7f3a9c
EXPOSE 8000
CMD ["python", "-m", "hydrowatch.api"]
