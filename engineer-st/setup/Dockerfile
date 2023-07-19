FROM python:3.11-slim

RUN apt-get update \
    && apt-get install make -y \
    && apt-get clean

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY ./ .

EXPOSE 8501

CMD streamlit run Home.py