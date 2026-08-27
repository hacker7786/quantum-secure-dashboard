FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
COPY frontend ./frontend
COPY data ./data
COPY training ./training
RUN python training/train_model.py
WORKDIR /app/backend
EXPOSE 5000
CMD ["python", "app.py"]
