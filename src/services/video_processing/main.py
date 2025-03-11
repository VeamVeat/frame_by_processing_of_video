import os

from dotenv import load_dotenv

from minio_service import MinioService
from processing_rtsp_stream import ProcessingRTSPStream
from search_same_moment import SearchSameMoment
from video_file_comparison import VideoFileComparison

load_dotenv('.env')

if __name__ == "__main__":
    os.makedirs('logs', exist_ok=True)

    # Создание бакетов
    create_bucket = MinioService()
    create_bucket.create_bucket()

    # Запуск потоков для обработки двух RTSP-стримов
    # При получении кадров по RTSP стриму, эти кадры нужно пересобрать в новые такие же файлы
    # и в потоке их записать на локальный MinIO.

    processing_rtsp_stream = ProcessingRTSPStream()
    processing_rtsp_stream.process()

    # Необходимо написать функцию, которая по прошествии определенного количества миллисекунд от начала просмотра видео,
    # сможет сопоставить записанный файл в MinIO с оригинальным файлом. Как следствие ожидаем, что попадем практически
    # кадр-в-кадр, с учетом динамического FPS. Результатом должно быть 2 расположенных сбоку друг от друга картинки,
    # соответствующих кадру выбранной миллисекунды.

    video_file_comparison = VideoFileComparison()
    video_file_comparison.process()

    # Необходимо написать функцию, которая сможет в двух разных видеофайлах с пункта №1 найти одинаковый момент,
    # соответствующий указанной миллисекунде. Результатом работы такой функции должен быть лог, который покажет,
    # сколько именно кадров в каждом файле пришлось пропустить, чтобы попасть в указанную точку на обоих видео.
    # Функция также должна делать снэпшот обоих таких кадров, для валидации.
    #
    search_same_moment = SearchSameMoment()
    search_same_moment.compare_videos(
        video_one_path=os.getenv('VIDEO_PATH_30FPS'),
        video_two_path=os.getenv('VIDEO_PATH_15FPS'),
        target_time_ms=int(os.getenv('TARGET_TIME_MS')),
        snapshot_dir=os.getenv('SNAPSHOTS_SEARCH_SAME_MOMENT_PATH'),
    )
