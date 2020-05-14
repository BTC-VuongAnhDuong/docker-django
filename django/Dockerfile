FROM python:2.7
WORKDIR /usr/src/app
EXPOSE 8080
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "--bind", ":8080", "mysite.wsgi:application"]