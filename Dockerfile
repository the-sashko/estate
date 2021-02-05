FROM alpine:3.10.2

RUN apk add git bash xvfb python3 py3-pip

RUN mkdir /storage

RUN git clone https://github.com/the-sashko/estate /storage/estate_parser

RUN /bin/bash /storage/estate_parser/scripts/install.sh

RUN rm -rf /storage/estate_parser/data

EXPOSE 80

CMD ["./storage/estate_parser/scripts/run.sh"]
