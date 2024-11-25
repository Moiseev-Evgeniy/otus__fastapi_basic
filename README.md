#  Fake currency prediction service

## Открыть приложение (локально)

Приложение по умолчанию доступно по адресу http://localhost:8000/  
Документация API методов доступна по адресу http://localhost:8000/docs

## Настройка

Для добавления своих параметров сервера, опционально можно создать файл `.env` в корне проекта и заполнить его по примеру `.env.template`

Для установки зависимостей:

```bash
poetry install
```
Для добавления зависимостей:

```bash
poetry add <package_name>
```
Для обновления зависимостей:

```bash
poetry lock
poetry install
```

## Запуск

Для запуска необходимо перейти в директорию `fastapi_basic` запустить команду:

```bash
python src/main.py
```

Запуск в докере:
1)
```bash 
docker build --tag otus_fastapi_basic .
```
2)
```bash
docker run -d -p 8000:8000 otus_fastapi_basic
```