# Используем официальный Python образ
FROM python:3.13-slim
RUN pip install --upgrade pip
# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем команду для запуска бота
CMD ["python", "main.py"]