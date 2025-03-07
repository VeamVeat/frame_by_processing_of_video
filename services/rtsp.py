import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')

from gi.repository import Gst, GstRtspServer, GLib

Gst.init(None)

class MyFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, filename):
        GstRtspServer.RTSPMediaFactory.__init__(self)
        self.filename = filename

    def do_create_element(self, url):
        return Gst.parse_launch(f"filesrc location={self.filename} ! qtdemux ! queue ! rtph264pay config-interval=1 name=pay0 pt=96")

class GstServer:
    def __init__(self):
        self.server = GstRtspServer.RTSPServer()
        self.server.set_service("8554")
        self.mount_points = self.server.get_mount_points()

    def add_stream(self, path, endpoint):
        factory = MyFactory(path)
        factory.set_shared(True)
        self.mount_points.add_factory(endpoint, factory)
        print(f"Stream available at rtsp://localhost:8554{endpoint}")

    def start(self):
        self.server.attach()
        print("Server started")
        GLib.MainLoop().run()

if __name__ == "__main__":
    server = GstServer()
    server.add_stream("output1.mp4", "/stream1")
    server.add_stream("output2.mp4", "/stream2")
    server.start()
