FROM python:3.11

COPY SetupEnv.sh test_frontend.py run_test.sh ./
RUN ./SetupEnv.sh

ENTRYPOINT ./run_test.sh