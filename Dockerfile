FROM python

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --noinput
CMD gunicorn project4.wsgi --bind 0.0.0.0:$PORT