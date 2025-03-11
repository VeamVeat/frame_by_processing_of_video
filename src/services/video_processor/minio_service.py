import os

from dotenv import load_dotenv
from minio import Minio, S3Error

from logger import setup_logger

logger = setup_logger()

load_dotenv('.env')


class MinioService:
    def __init__(self):
        self._minio_client = Minio(
            os.getenv('MINIO_ENDPOINT'),
            access_key=os.getenv('MINIO_ACCESS_KEY'),
            secret_key=os.getenv('MINIO_SECRET_KEY'),
            secure=False
        )
        self._bucket_names = [
            os.getenv('MINIO_BUCKET_ONE'),
            os.getenv('MINIO_BUCKET_TWO')
        ]

    def create_buckets(self):
        try:
            for bucket in self._bucket_names:
                if self._minio_client.bucket_exists(bucket):
                    logger.info(f"Бакет '{bucket}' уже существует.")
                    continue

                self._minio_client.make_bucket(bucket)
                logger.info(f"Бакет '{bucket}' успешно создан.")
        except S3Error as exp:
            logger.error(f"Ошибка при создании бакета: {exp}")

    def fput_object(
            self,
            bucket_name: str,
            object_name: str,
            temp_filename: str
    ):
        self._minio_client.fput_object(bucket_name, object_name, temp_filename)

    def bucket_exists(self, bucket_name: str):
        self._minio_client.bucket_exists(bucket_name)

    def make_bucket(self, bucket_name: str):
        self._minio_client.make_bucket(bucket_name)

    def fget_object(self, bucket_name, object_name, temp_filename):
        self._minio_client.fget_object(bucket_name, object_name, temp_filename)

    def list_objects(self, bucket_name):
        return self._minio_client.list_objects(bucket_name)
