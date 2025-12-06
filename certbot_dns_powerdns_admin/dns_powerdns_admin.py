"""DNS Authenticator for PowerDNS Admin."""

from typing import Any
from typing import Callable
from typing import Optional

from certbot import errors
from certbot.plugins import dns_common
from certbot.plugins.dns_common import CredentialsConfiguration

from certbot_dns_powerdns_admin.powerdns_admin import PowerDNS_Admin


class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for PowerDNS Admin

    This Authenticator uses the PowerDNS Admin API to fulfill a dns-01 challenge.
    """

    description = "Authenticate using PowerDNS-Admin API."

    ttl: int = 60

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.credentials: Optional[CredentialsConfiguration] = None

    @classmethod
    def add_parser_arguments(
        cls, add: Callable[..., None], default_propagation_seconds: int = 10
    ) -> None:
        super().add_parser_arguments(add, default_propagation_seconds)
        add("credentials", help="PowerDNS Admin credentials INI file.")

    def more_info(self) -> str:
        return (
            "This plugin configures a DNS TXT record to respond to a dns-01 challenge "
            "using the PowerDNS Admin API."
        )

    def _validate_credentials(self, credentials: CredentialsConfiguration) -> None:
        url = credentials.conf("api-url")
        key = credentials.conf("api-key")

        if not url:
            raise errors.PluginError(
                f"{credentials.confobj.filename}: dns_powerdns_admin_api_url is required."
            )
        if not key:
            raise errors.PluginError(
                f"{credentials.confobj.filename}: dns_powerdns_admin_api_key is required."
            )

    def _setup_credentials(self) -> None:
        self.credentials = self._configure_credentials(
            "credentials",
            "PowerDNS Admin credentials INI file",
            None,
            self._validate_credentials,
        )

    def _get_powerdns_admin(self) -> PowerDNS_Admin:
        return PowerDNS_Admin(
            api_url=self.credentials.conf("api-url"),
            api_key=self.credentials.conf("api-key"),
        )

    def _get_zone(self, domain: str) -> str:
        return dns_common.base_domain_name_guesses(domain)[-2]

    def _perform(self, domain, validation_name, validation):
        powerdns_admin = self._get_powerdns_admin()

        powerdns_admin.add_new_record(
            zone=self._get_zone(domain),
            record_name=validation_name,
            record_type="TXT",
            record_ttl=self.ttl,
            record_content=validation,
        )

    def _cleanup(self, domain, validation_name, validation):
        powerdns_admin = self._get_powerdns_admin()

        powerdns_admin.delete_record(
            zone=self._get_zone(domain),
            record_name=validation_name,
            record_type="TXT",
            record_ttl=self.ttl,
        )
