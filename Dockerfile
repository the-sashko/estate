FROM alpine:3.10.2

MAINTAINER inbox@sashko.me

RUN apk add git bash xvfb python3 py3-pip

RUN mkdir /storage

RUN cd /storage

RUN git clone https://github.com/the-sashko/estate estate_parser

RUN cd estate_parser

RUN /bin/bash scripts/install.sh

EXPOSE 80

CMD ["./storage/estate_parser/scripts/run.sh"]
