FROM python
COPY requirement.txt /req/
WORKDIR /app
RUN pip install -r /req/requirement.txt
# CMD python dog_info.py