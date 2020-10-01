gst-launch-1.0 nvarguscamerasrc wbmode=1 sensor_id=0 ! nvvidconv flip-method=2 ! nveglglessink
