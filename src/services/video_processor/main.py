import os

from dotenv import load_dotenv

from minio_service import MinioService
from processing_rtsp_stream import ProcessingRTSPStream
from search_same_moment import SearchSameMoment
from video_file_comparison import VideoFileComparison

load_dotenv('.env')

if __name__ == "__main__":
    os.makedirs('logs', exist_ok=True)

    create_bucket = MinioService()
    create_bucket.create_buckets()

    processing_rtsp_stream = ProcessingRTSPStream()
    processing_rtsp_stream.process()

    video_file_comparison = VideoFileComparison()
    video_file_comparison.process()

    search_same_moment = SearchSameMoment()
    search_same_moment.compare_videos(
        video_one_path=os.getenv('VIDEO_PATH_30FPS'),
        video_two_path=os.getenv('VIDEO_PATH_15FPS'),
        target_time_ms=int(os.getenv('TARGET_TIME_MS')),
        snapshot_dir=os.getenv('SNAPSHOTS_SEARCH_SAME_MOMENT_PATH'),
    )
