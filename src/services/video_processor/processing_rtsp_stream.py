import os
import tempfile
import threading

import cv2

from minio_service import MinioService
from logger import setup_logger

logger = setup_logger()


class ProcessingRTSPStream:
    @staticmethod
    def capture_and_upload(rtsp_url: str, output_prefix: str, bucket_name: str):
        """
        Захват кадров из RTSP-стрима и загрузка в MinIO.
        :param rtsp_url: URL RTSP-стрима.
        :param output_prefix: Префикс для имени выходного файла.
        :param bucket_name: Имя бакета в MinIO.
        """
        # Подключение к RTSP-стриму
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            raise ValueError(f"Не удалось подключиться к RTSP-стриму: {rtsp_url}")

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        minio_service = MinioService()

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
            temp_filename = temp_file.name

            # Создаем VideoWriter для записи в временный файл
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_filename, fourcc, fps, (width, height))

            # Чтение и запись кадров
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                out.write(frame)

            cap.release()
            out.release()

            object_name = f"{output_prefix}_{int(cap.get(cv2.CAP_PROP_POS_MSEC))}.mp4"
            minio_service.fput_object(
                bucket_name,
                object_name,
                temp_filename
            )
            logger.info(f"Видео загружено в MinIO: {bucket_name}/{object_name}")

        os.remove(temp_filename)

    def process(self):
        """
        Запуск потоков для обработки двух RTSP-стримов.
        При получении кадров по RTSP стриму, эти кадры пересобираются в новые такие же файлы
        и в потоке их записываются на локальный MinIO.
        """

        rtsp_urls = [
            os.getenv('RTSP_URL_VIDEO_ONE'),
            os.getenv('RTSP_URL_VIDEO_TWO')
        ]

        bucket_names = [
            os.getenv('MINIO_BUCKET_ONE'),
            os.getenv('MINIO_BUCKET_TWO'),
        ]

        threads = []

        for i, (rtsp_url, bucket_name) in enumerate(zip(rtsp_urls, bucket_names)):
            thread = threading.Thread(
                target=self.capture_and_upload,
                args=(rtsp_url, f"video{i + 1}", bucket_name)
            )

            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
