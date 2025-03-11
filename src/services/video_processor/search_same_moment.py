import cv2

from logger import setup_logger

logger = setup_logger()


class SearchSameMoment:
    @staticmethod
    def find_frame_by_time(video_path, target_time_ms):
        """
        Находит кадр, соответствующий указанной временной метке.
        :param video_path: Путь к видеофайлу.
        :param target_time_ms: Временная метка в миллисекундах.
        :return: Кадр, соответствующий временной метке, и количество пропущенных кадров.
        """
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise ValueError(f"Не удалось открыть видеофайл: {video_path}")

        # Получаем FPS видео
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_time_ms = 1000 / fps

        # Вычисляем целевой кадр
        target_frame = int(target_time_ms / frame_time_ms)

        # Пропускаем кадры до целевого
        skipped_frames = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                raise ValueError(f"Не удалось прочитать кадр из видео: {video_path}")

            # Если достигли целевого кадра, возвращаем его
            if skipped_frames >= target_frame:
                cap.release()
                return frame, skipped_frames

            skipped_frames += 1

    def compare_videos(
            self,
            video_one_path: str,
            video_two_path: str,
            target_time_ms: int,
            snapshot_dir: str
    ):
        """
        Функция, которая сможет в двух разных видеофайлах с пункта №1 найти одинаковый момент,
        соответствующий указанной миллисекунде.

        В log файл пишется, сколько именно кадров в каждом файле пришлось пропустить,
        чтобы попасть в указанную точку на обоих видео.

        Функция делает снэпшот обоих таких кадров, для валидации.

        :param video_one_path: Путь к первому видеофайлу.
        :param video_two_path: Путь ко второму видеофайлу.
        :param target_time_ms: Временная метка в миллисекундах.
        :param snapshot_dir: Папка для сохранения снэпшотов.
        """

        frame1, skipped_frames_one = self.find_frame_by_time(video_one_path, target_time_ms)
        frame2, skipped_frames_two = self.find_frame_by_time(video_two_path, target_time_ms)

        logger.info(f"Видео 1: Пропущено кадров: {skipped_frames_one}")
        logger.info(f"Видео 2: Пропущено кадров: {skipped_frames_two}")

        combined_frame = cv2.hconcat([frame1, frame2])
        snapshot_path = snapshot_dir.format(target_time_ms)
        cv2.imwrite(snapshot_path, combined_frame)

        logger.info(f"Снэпшот сохранен как {snapshot_path}")
