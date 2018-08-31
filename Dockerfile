ARG PY_VERSION=3.7
FROM python:${PY_VERSION}
RUN pip install --no-cache-dir pytest responses pandas
COPY . /src/
WORKDIR /src
RUN pip install .

CMD ["python", "-m", "pytest"]
