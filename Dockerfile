FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN mkdir /API_LOGIN
WORKDIR /API_LOGIN

COPY pyproject.toml /API_LOGIN/
RUN pip install poetry
RUN poetry install
COPY app /API_LOGIN/app
CMD ["poetry", "run", "uvicorn", "app.main:app"]
