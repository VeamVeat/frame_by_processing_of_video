import os

import gi
from dotenv import load_dotenv

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GstRtspServer, GLib

from logger import setup_logger

logger = setup_logger()

Gst.init(None)

load_dotenv('.env')


class RTSPMediaFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, path_to_video):
        super(RTSPMediaFactory, self).__init__()
        self._video_path = path_to_video

    def do_create_element(self, url):
        return Gst.parse_launch(f"{os.getenv('RTSP_PIPELINE')}")


class RTSPServer:
    def __init__(self, paths_to_video):
        self._paths_to_video = paths_to_video
        self._server = GstRtspServer.RTSPServer()
        self._server.set_service("8554")

        for index, path_to_video in enumerate(self._paths_to_video):
            factory = RTSPMediaFactory(path_to_video)
            factory.set_shared(True)
            mount_point = self._server.get_mount_points()
            mount_point.add_factory(f"/video{index+1}", factory)

        self._server.attach(None)


if __name__ == "__main__":
    video_paths = [
        os.getenv('VIDEO_PATH_30FPS'),
        os.getenv('VIDEO_PATH_15FPS')
    ]

    server = RTSPServer(video_paths)

    logger.info(f"RTSP-сервер запущен. Стримы доступны по адресам:")
    logger.info(f"{video_paths}")

    for video_path, _ in enumerate(video_paths):
        logger.info(f"{os.getenv('RTSP_URL')}{video_path+1}")

    loop = GLib.MainLoop()
    loop.run()
