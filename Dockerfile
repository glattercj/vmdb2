# docker build -t vmdb2 .
# docker run -it --rm -v $(pwd):/root vmdb2 pyinstaller vmdb2.spec
FROM ubuntu:bionic
RUN set -x && apt-get update && apt-get install -y \
    python3-pip python3-yaml python3-jinja2 wget zlib1g-dev && \
    wget --no-check-certificate http://archive.ubuntu.com/ubuntu/pool/universe/p/python-cliapp/python3-cliapp_1.20170827-1_all.deb && \
    wget --no-check-certificate http://mirrors.kernel.org/ubuntu/pool/main/x/xz-utils/liblzma5_5.2.2-1.3_amd64.deb && \
    wget --no-check-certificate http://mirrors.kernel.org/ubuntu/pool/main/x/xz-utils/xz-utils_5.2.2-1.3_amd64.deb && \
    dpkg -i *.deb
RUN set -x && pip3 install pyinstaller==4.10
WORKDIR /root
CMD /bin/bash
