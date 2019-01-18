FROM python:2.7.13-alpine

RUN apk update &&\
    apk add git

RUN git clone https://github.com/shivamgupta01/bitcoin_transaction_analysis.git
WORKDIR /bitcoin_transaction_analysis
RUN chmod +x sniffer.py
RUN pip install boto3 &&\
    pip install base58 &&\
    pip install arrow &&\
    pip install sqlalchemy &&\
    pip install flask &&\
    pip install requests &&\
    pip install github_webhook
    
WORKDIR /bitcoin_transaction_analysis
ENTRYPOINT python app.py

# Docker Build command:
# docker build --no-cache -t bitcoin_transaction_analysis .

# Docker Run command:
# docker run --rm -it -p 4000:4000 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY bitcoin_transaction_analysis