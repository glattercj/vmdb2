FROM ubuntu:xenial
RUN set -x && apt-get update && apt-get install -y \
    python3-pip python3-yaml python3-jinja2 wget && \
    wget --no-check-certificate http://archive.ubuntu.com/ubuntu/pool/universe/p/python-cliapp/python3-cliapp_1.20170827-1_all.deb && \
    dpkg -i *.deb
RUN set -x && pip3 install pyinstaller
WORKDIR /root
CMD /bin/bash

