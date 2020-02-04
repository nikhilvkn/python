FROM alpine
RUN apk upgrade --no-cache \
  && apk add --no-cache \
    musl \
    build-base \
    python3 \
    python3-dev \
    postgresql-dev \
    bash \
    git \
    libffi-dev \
    curl \
  && pip3 install --no-cache-dir --upgrade pip \
  && rm -rf /var/cache/* \
  && rm -rf /root/.cache/*

RUN cd /usr/bin \
  # && ln -sf easy_install-3.5 easy_install \
  && ln -sf python3 python \
  && ln -sf pip3 pip

ADD bin/* /home/tivo/bin/
ADD data/* /home/tivo/data/
COPY etc /home/tivo/etc/

RUN pip install -r /home/tivo/data/requirements.txt

ENTRYPOINT [ "/home/tivo/bin/runme.sh" ]

CMD [ "-h" ]
