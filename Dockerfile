FROM python:3.10
ENV Token=0
WORKDIR /app
COPY requirements.txt .

RUN apt update

COPY . .

RUN pip install -r requirements.txt
CMD ["python","main.py"]