FROM python

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --noinput
