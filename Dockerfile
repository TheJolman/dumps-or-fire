ARG PYTHON_VERSION=3.10-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

# Dependecies
RUN pip install uv
COPY pyproject.toml uv.lock /code/
RUN uv export --format requirements-txt > requirements.txt
RUN uv pip install -r requirements.txt --system

COPY . /code
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn","--bind",":8000","--workers","2","dumps_or_fire.wsgi"]
