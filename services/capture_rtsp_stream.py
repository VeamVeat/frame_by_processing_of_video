import io
from datetime import datetime

import numpy
import cv2

from db.config import MinioService


class CaptureRtspStreamService:
    @staticmethod
    def save_frame_to_minio(
            frame: numpy.ndarray,
            bucket_name: str,
            object_name: str
    ):
        # Convert the frame to bytes (assuming frame is a numpy array)
        _, buffer = cv2.imencode('.jpg', frame)

        # Wrap the bytes in a BytesIO object
        buffer_io = io.BytesIO(buffer.tobytes())

        minio_service = MinioService()
        minio_service.put_object(
            bucket_name,
            object_name,
            buffer_io,
            len(buffer.tobytes()),
            content_type='image/jpeg'
        )


    def capture_rtsp_stream(self, rtsp_url: str, bucket_name: str):
        video_capture = cv2.VideoCapture(rtsp_url)
        frame_count = 0

        while video_capture.isOpened():
            ret, frame = video_capture.read()

            if not ret:
                break

            frame_count += 1
            object_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{frame_count}.jpg"

            self.save_frame_to_minio(frame, bucket_name, object_name)

        video_capture.release()

    def run(self, stream_names: list[str], buckets: list[str]):

        if len(stream_names) != len(buckets):
            return

        len_buckets = len(buckets)

        for bucket in range(len_buckets):
            l = stream_names[bucket]
            self.capture_rtsp_stream(
                f"rtsp://localhost:8554/{stream_names[bucket]}",
                buckets[bucket]
            )
