from __future__ import annotations
from typing import Any, Mapping
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from ..config import settings

_client: InfluxDBClient | None = None

def _client_once() -> InfluxDBClient:
    global _client
    if _client is None:
        _client = InfluxDBClient(url=settings.influx_url, token=settings.influx_token, org=settings.influx_org)
    return _client

def write_measurement(measurement: str, fields: Mapping[str, Any], tags: Mapping[str, str] | None = None) -> None:
    cli = _client_once()
    write_api = cli.write_api(write_options=SYNCHRONOUS)
    p = Point(measurement)
    for k, v in (tags or {}).items():
        p = p.tag(k, v)
    for k, v in fields.items():
        p = p.field(k, v)
    write_api.write(bucket=settings.influx_bucket, org=settings.influx_org, record=p)
