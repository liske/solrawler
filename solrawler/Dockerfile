FROM alpine:3.10

RUN apk --force-refresh add python3 py3-asn1 py3-asn1-modules py3-beautifulsoup4 py3-cffi py3-cryptography \
    py3-lxml py3-pypdf2 py3-requests py3-twisted && \
    pip3 install pysolr scrapy html5lib

ADD . /opt/solrawler

WORKDIR /opt/solrawler

USER 8984:8984

ENTRYPOINT [ "/opt/solrawler/entrypoint.sh" ]
CMD []
