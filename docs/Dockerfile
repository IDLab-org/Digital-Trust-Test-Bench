FROM python:slim

RUN pip install mkdocs

COPY ./mkdocs.yaml ./
COPY ./ ./docs

CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]