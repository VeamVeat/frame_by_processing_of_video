FROM arm64v8/ubuntu:20.04

RUN apt-get update && apt-get install -y \
    python3-pip \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-good1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    python3-gst-1.0 \
    minio-client

RUN pip3 install minio opencv-python

COPY . /app
WORKDIR /app

CMD ["python3", "service/rtsp.py"]
CMD ["python3", "service/search_frames.py.py"]
