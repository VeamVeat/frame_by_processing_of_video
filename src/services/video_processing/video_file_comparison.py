import os
import tempfile

import cv2

from minio_service import MinioService
from logger import setup_logger

logger = setup_logger()


class VideoFileComparison:
    @staticmethod
    def list_objects_in_bucket(bucket_name: str):
        """
        Возвращает список объектов в бакете.
        :param bucket_name: Имя бакета.
        :return: Список имен объектов.
        """
        minio_service = MinioService()

        objects_b = minio_service.list_objects(bucket_name)
        return [obj.object_name for obj in objects_b]

    @staticmethod
    def download_video_from_minio(bucket_name: str, object_name: str):
        """
        Загружает видеофайл из MinIO во временный файл.
        :param bucket_name: Имя бакета.
        :param object_name: Имя объекта в MinIO.
        :return: Путь к временному файлу.
        """
        minio_service = MinioService()

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            temp_filename = temp_file.name

            minio_service.fget_object(bucket_name, object_name, temp_filename)
            logger.info(f"Видео {object_name} загружено из MinIO.")

            return temp_filename

    @staticmethod
    def find_frame_by_time(video_path: str, target_time_ms: int):
        """
        Находит кадр, соответствующий указанной временной метке.
        :param video_path: Путь к видеофайлу.
        :param target_time_ms: Временная метка в миллисекундах.
        :return: Кадр, соответствующий временной метке.
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Не удалось открыть видеофайл: {video_path}")

        # Устанавливаем временную метку
        cap.set(cv2.CAP_PROP_POS_MSEC, target_time_ms)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise ValueError(f"Не удалось прочитать кадр из видео: {video_path}")

        return frame

    def compare_videos(
            self,
            original_video_path: str,
            recorded_bucket: str,
            recorded_object: str,
            target_time_ms: int
    ):
        """
        Сравнивает оригинальное и записанное видео по указанной временной метке.
        :param original_video_path: Локальный путь к оригинальному видеофайлу.
        :param recorded_bucket: Имя бакета с записанным видео.
        :param recorded_object: Имя объекта с записанным видео.
        :param target_time_ms: Временная метка в миллисекундах.
        """
        recorded_file = self.download_video_from_minio(recorded_bucket, recorded_object)

        # Поиск кадров по временной метке
        original_frame = self.find_frame_by_time(original_video_path, target_time_ms)
        recorded_frame = self.find_frame_by_time(recorded_file, target_time_ms)

        combined_frame = cv2.hconcat([original_frame, recorded_frame])
        cv2.imwrite(os.getenv('SNAPSHOT_PATH').format(target_time_ms), combined_frame)

        logger.info(f"Снэпшот сохранен как {os.getenv('SNAPSHOT_PATH').format(target_time_ms)}")

        os.remove(recorded_file)

    def process(self):
        recorded_object = self.list_objects_in_bucket(os.getenv('MINIO_BUCKET_ONE'))[0]

        # Сравнение видео
        self.compare_videos(
            os.getenv('VIDEO_PATH_30FPS'),
            os.getenv('MINIO_BUCKET_ONE'),
            recorded_object,
            int(os.getenv('TARGET_TIME_MS'))
        )
