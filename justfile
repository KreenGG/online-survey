set shell := ["powershell.exe", "-c"]

default:
  just --list

runserver:
  python manage.py runserver

makemigrations:
  python manage.py makemigrations

migrate *args:
  python manage.py migrate {{args}}

startapp *args:
  python manage.py startapp {{args}}