FROM python:3.10
ENV Token=0
WORKDIR /app
COPY requirements.txt .

RUN apt update
EXPOSE 80

COPY . .

RUN pip install -r requirements.txt
RUN chmod a+x runner.sh
CMD ["./run.sh"]