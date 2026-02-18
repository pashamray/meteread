import logging
from datetime import datetime, timezone

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from storage import AbstractStorage

logger = logging.getLogger(__name__)


class InfluxDBStorage(AbstractStorage):
    def __init__(self, url: str, token: str, org: str, bucket: str):
        self.bucket = bucket
        self.org = org
        self._client = InfluxDBClient(url=url, token=token, org=org)
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)

    def write(self, measurement: str, tags: dict, fields: dict, timestamp: datetime | None = None) -> None:
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)

        point = Point(measurement).time(timestamp)
        for key, value in tags.items():
            point = point.tag(key, value)
        for key, value in fields.items():
            point = point.field(key, value)

        self._write_api.write(bucket=self.bucket, org=self.org, record=point)
        logger.info(f"influxdb write: {measurement} {fields}")
