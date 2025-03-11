ARG PYTHON_VERSION=3.10-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

# Install Dependecies
RUN pip install uv
COPY pyproject.toml uv.lock .python-version /code/
RUN uv add gunicorn
RUN uv sync

COPY . /code
RUN uv run manage.py collectstatic --noinput

EXPOSE 8000

CMD ["uv", "run", "gunicorn","--bind",":8000","--workers","2","dumps_or_fire.wsgi"]
