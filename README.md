# certbot-dns-powerdns-admin

Certbot DNS Authenticator plugin for PowerDNS Admin.

Inspired by other certbot-dns-* plugins found in the [official Certbot repository](https://github.com/certbot/certbot).

## Installation

Install native or extend official ``certbot/certbot`` Docker image.

## Native

```sh
pip install "https://github.com/Simon-Spettmann/certbot-dns-powerdns-admin"
```

### Docker image

```Dockerfile
FROM certbot/certbot

RUN pip install "https://github.com/Simon-Spettmann/certbot-dns-powerdns-admin/archive/refs/heads/main.zip"
```

## Configuration

Set `api_url` and `api_key` in `.ini` file.

```ini
# ./dns_powerdns_admin.ini
dns_powerdns_admin_api_url = https://example.com
dns_powerdns_admin_api_key = password
```

## Usage

Run `certbot` with `--authenticator "dns-powerdns-admin"` and `--dns-powerdns-admin-credentials "./dns_powerdns_admin.ini"`.

Optional: `--dns-powerdns-admin-propagation-seconds "60"`

```sh
certbot ... \
    --authenticator "dns-powerdns-admin" \
    --dns-powerdns-admin-credentials "./dns_powerdns_admin.ini" \
    --dns-powerdns-admin-propagation-seconds "60" \
    ...
```
