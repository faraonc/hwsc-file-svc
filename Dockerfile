FROM python:3.7.3
RUN git clone https://github.com/hwsc-org/hwsc-file-transaction-svc.git
WORKDIR hwsc-file-transaction-svc
RUN pip3.7 install pipenv
RUN pipenv install -v
CMD pipenv run python3.7 main.py
EXPOSE 50053