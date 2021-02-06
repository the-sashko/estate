FROM alpine:3.10.2

RUN apk add git=2.22.4-r0 --no-cache

RUN apk add bash=5.0.0-r0 --no-cache

RUN apk add xvfb=1.20.5-r2 --no-cache

RUN apk add firefox-esr=60.9.0-r0 --no-cache

RUN apk add python3=3.7.7-r1 --no-cache

RUN mkdir /storage

RUN git clone https://github.com/the-sashko/estate /storage/estate_parser

RUN /bin/bash /storage/estate_parser/scripts/install.sh

EXPOSE 80

CMD ["./storage/estate_parser/scripts/run.sh"]
