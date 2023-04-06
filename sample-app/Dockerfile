FROM python:3.8.2-slim as pythonBuilder
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --target=/app/dependencies -r requirements.txt
COPY ./sample ./sample

FROM python:3.8.2-slim
ENV SERVING_PORT 8000
WORKDIR /app
COPY --from=pythonBuilder       /app .
ENV PYTHONPATH="${PYTHONPATH}:/app/dependencies"
ENV PATH="${PATH}:/app/dependencies/bin"
CMD ["uvicorn", "sample.main:app", "--workers", "1",  "--host", "0.0.0.0", "--port", "8000"]