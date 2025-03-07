import logging

from datetime import datetime
from typing import Optional

from db.config import MinioService
from services.capture_rtsp_stream import CaptureRtspStreamService
from services.image import ImageService

logging.basicConfig(filename='../logs/video_sync.log', level=logging.INFO)

class SearchMatchingFrames:
    @staticmethod
    def _extract_timestamp(filename: str) -> int:
        """
        :param filename: "20250307112312_1.jpg"
        :return: milliseconds
        """
        timestamp_str = filename.split('_')[0]  # Извлекаем "20250307112312"
        datetime_object = datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")

        return int(datetime_object.timestamp() * 1000)


    def find_matching_frames(
            self,
            bucket_one,
            bucket_two,
            target_time_ms
    ) -> tuple[Optional[str], Optional[str]]:
        minio_service = MinioService()
        image_from_bucket_one = minio_service.list_objects(bucket_one)
        image_from_bucket_two = minio_service.list_objects(bucket_two)

        for image_one in image_from_bucket_one:
            object_name_one = image_one.object_name

            timestamp_for_one_image = self._extract_timestamp(object_name_one)

            if timestamp_for_one_image >= target_time_ms:
                for image_two in image_from_bucket_two:
                    object_name_two = image_two.object_name
                    timestamp_for_two_image = self._extract_timestamp(object_name_two)

                    if timestamp_for_two_image >= target_time_ms:
                        image_service = ImageService(
                            storage_name=bucket_one,
                            object_name_to_storage=object_name_one
                        )
                        prepare_image_one = image_service.process()

                        image_service = ImageService(
                            storage_name=bucket_two,
                            object_name_to_storage=object_name_two
                        )
                        prepare_image_two = image_service.process()

                        if prepare_image_one.shape == prepare_image_two.shape:
                            logging.info(f"Match found at: {target_time_ms} ms")
                            return object_name_one, object_name_two


if __name__ == '__main__':
    capture_rtsp_stream_service = CaptureRtspStreamService()
    capture_rtsp_stream_service.run(
        stream_names=['stream1', 'stream2'],
        buckets=['bucketone', 'buckettwo']
    )

    search_matching_frames = SearchMatchingFrames()
    frame_one, frame_two = search_matching_frames.find_matching_frames(
        "bucketone",
        "buckettwo",
        5000
    )
    logging.info(f"Frame_one: {frame_one}, Frame_two: {frame_two}")
