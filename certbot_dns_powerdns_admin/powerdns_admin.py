"""DNS Authenticator helper for PowerDNS Admin."""

import requests
import json


class PowerDNS_Admin:
    """DNS Authenticator helper for PowerDNS Admin

    This Authenticator helper communicates with the PowerDNS Admin API.
    """

    def __init__(self, api_url, api_key) -> None:
        self.api_url = api_url
        self.api_key = api_key

        self.headers = {"X-API-Key": f"{api_key}", "Content-Type": "application/json"}

    def _get_url(self, zone: str) -> str:
        return f"{self.api_url}/api/v1/servers/localhost/zones/{zone}"

    def _list_records(self, zone) -> json:
        try:
            response = requests.get(
                url=self._get_url(zone),
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as exception:
            raise exception

    def add_new_record(
        self, zone, record_name, record_type, record_ttl, record_content
    ):
        data = {
            "rrsets": [
                {
                    "name": f"{record_name}.",
                    "type": f"{record_type}",
                    "ttl": int(record_ttl),
                    "changetype": "REPLACE",
                    "records": [{"content": f'"{record_content}"', "disabled": False}],
                }
            ]
        }

        try:
            response = requests.patch(
                url=self._get_url(zone),
                data=json.dumps(data),
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
        except requests.HTTPError as exception:
            raise exception

    def update_record(
        self,
        zone,
        record_name_old,
        record_type_old,
        record_ttl_old,
        record_name_new,
        record_type_new,
        record_ttl_new,
        record_content_new,
    ):
        data = {
            "rrsets": [
                {
                    "name": f"{record_name_old}.",
                    "type": f"{record_type_old}",
                    "ttl": int(record_ttl_old),
                    "changetype": "REPLACE",
                    "records": [
                        {
                            "name": f"{record_name_new}.",
                            "type": f"{record_type_new}",
                            "ttl": int(record_ttl_new),
                            "content": f'"{record_content_new}"',
                            "disabled": False,
                        }
                    ],
                }
            ]
        }

        try:
            response = requests.patch(
                url=self._get_url(zone),
                data=json.dumps(data),
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
        except requests.HTTPError as exception:
            raise exception

    def delete_record(self, zone, record_name, record_type, record_ttl):
        data = {
            "rrsets": [
                {
                    "name": f"{record_name}.",
                    "type": f"{record_type}",
                    # "ttl": int(record_ttl),
                    "changetype": "DELETE",
                }
            ]
        }

        try:
            response = requests.patch(
                url=self._get_url(zone),
                data=json.dumps(data),
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
        except requests.HTTPError as exception:
            raise exception
