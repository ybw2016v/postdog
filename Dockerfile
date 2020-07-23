FROM python
COPY requirements.txt /req/
WORKDIR /req
RUN pip install -r requirements.txt
WORKDIR /app
# CMD python dog_info.py