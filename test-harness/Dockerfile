FROM python:3.7.2-alpine

RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install kafka-python
RUN pip3 install flask_restful

WORKDIR /home/test-harness
COPY . /home/test-harness

CMD python main.py kafka
