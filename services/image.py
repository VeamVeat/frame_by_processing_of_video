import logging

import numpy as np
import cv2

from db.config import MinioService

logging.basicConfig(filename='../logs/video_sync.log', level=logging.INFO)


class ImageService:
    def __init__(self, storage_name, object_name_to_storage):
        self._storage_name = storage_name
        self._object_name_to_storage = object_name_to_storage


    @staticmethod
    def _get_image_bytes(storage_name: str, name_object: str) -> bytes:
        minio_service = MinioService()

        response = minio_service.get_object(storage_name, name_object)
        image_bytes = None

        try:
            image_bytes = response.read()
        except AttributeError as exp:
            logging.info(f"Read error: {exp}")

        response.close()
        response.release_conn()

        return image_bytes

    @staticmethod
    def _convert_bytes_to_array(image_bytes, dtype=np.uint8) -> np.ndarray:
        return np.frombuffer(image_bytes, dtype=dtype)

    @staticmethod
    def _decoding_image(decoded_image):
        return cv2.imdecode(decoded_image, cv2.IMREAD_COLOR)

    @staticmethod
    def _save_image(object_name: str, decoded_image):
        output_image_path = f"../images/{object_name}.jpg"

        cv2.imwrite(output_image_path, decoded_image)

    def process(self):
        image_bytes = self._get_image_bytes(self._storage_name, self._object_name_to_storage)
        image_array = self._convert_bytes_to_array(image_bytes)
        decoded_image = self._decoding_image(image_array)

        self._save_image(self._object_name_to_storage, decoded_image)

        return decoded_image
