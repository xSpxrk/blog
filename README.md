# Разработка backend для блога
В данном проекте будет реализовано создание пользователями постов
## Настройка репозитория
Создаем файл .env.
В файле .env добавляем необходимые нам поля, для подключения к базе данных.

# Запуск проекта

1. Создайте виртуальное окружение.
```bash
python -m venv env
```
2. Войдите в виртуальное окружение.
- Для windows.
```bash
env\Scripts\activate.bat
```
- Для unix систем.
```bash
source env/Scripts/activate
```
3. Используйте пакетный менеджер [pip](https://pypi.org/project/pip/) для установки зависимостей.
```bash
pip install -r requirements.txt
```
4. Создаем таблицы в нашей базе данных.
```bash
alembic upgrade 041d
```
5. Запускаем проект из главной директории.
```bash
uvicron app.main:app --reload
```