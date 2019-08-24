#!/bin/sh


while true; do
    scrapy crawl $@

    echo "SLEEPING FOR ${SOLRAWLER_DELAY:-14400} SECONDS"
    sleep ${SOLRAWLER_DELAY:-86400}
done
