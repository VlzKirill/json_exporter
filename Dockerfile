# Используем базовый образ Python
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы из текущего каталога внутрь контейнера
COPY . /app/

# Выполняем миграции и собираем статические файлы
RUN python manage.py migrate
#RUN python manage.py collectstatic --noinput

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Команда для запуска приложения при старте контейнера
CMD ["python", "manage.py", "runserver"]
