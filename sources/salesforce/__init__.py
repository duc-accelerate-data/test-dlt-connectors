import dlt
from dlt.sources import DltResource
from typing import Iterator

@dlt.source
def salesforce(
    instance_url: str = dlt.config.value,
    username: str = dlt.secrets.value,
    password: str = dlt.secrets.value,
    security_token: str = dlt.secrets.value,
) -> Iterator[DltResource]:
    """Minimal Salesforce source for Studio connector-source verification."""
    yield dlt.resource([], name="accounts")
