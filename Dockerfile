FROM python:3.12-alpine

# Устанавливаем рабочую директорию
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Обновляем список пакетов и устанавливаем необходимые зависимости
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev

# Обновляем pip и устанавливаем зависимости проекта
RUN pip install --upgrade pip

# Копируем файл requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы в рабочую директорию
COPY . .