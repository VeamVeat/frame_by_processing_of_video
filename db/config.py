import _io
from typing import Generator

import urllib3
from minio import Minio
from minio.datatypes import Object

class MinioService:
    def __init__(self):
        self._client = Minio(
            "0.0.0.0:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            secure=False
        )

    def put_object(
            self,
            bucket_name: str,
            object_name: str,
            buffer_io: _io.BytesIO,
            len_buffer_bytes: int,
            content_type: str
    ):
        # Use the BytesIO object with MinIO
        self._client.put_object(
            bucket_name,
            object_name,
            buffer_io,
            len_buffer_bytes,
            content_type=content_type
        )

    def list_objects(self, storage_name: str) -> Generator[Object, None, None]:
        return self._client.list_objects(storage_name)

    def get_object(self, storage_name: str, name_object: str) -> urllib3.response.HTTPResponse:
        return self._client.get_object(storage_name, name_object)
