FROM certbot/certbot

COPY "." "/tmp/certbot-dns-powerdns-admin"

RUN pip install "/tmp/certbot-dns-powerdns-admin"
