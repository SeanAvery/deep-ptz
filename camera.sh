# csi --> rtp
gst-launch-1.0 nvarguscamerasrc ! nvvidconv ! videoconvert ! video/x-raw, format=BGR ! rtpvrawpay ! udpsink host=127.0.0.1 port=5004
