# отец лох

from clover import srv
from pyzbar import pyzbar
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from clover import long_callback
from std_srvs.srv import Trigger
import rospy
import math


get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)

def navigate_wait(x=0, y=0, z=0, speed=0.5, frame_id='body', auto_arm=False):
    res = navigate(x=x, y=y, z=z, yaw=float('nan'), speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    if not res.success:
        raise Exception(res.message)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < 0.2:
            return
        rospy.sleep(0.2)

def land_wait():
    land()
    while get_telemetry().armed:
        rospy.sleep(0.2)

rospy.init_node('cv')
bridge = CvBridge()

@long_callback
def image_callback(msg):
    img = bridge.imgmsg_to_cv2(msg, 'bgr8')
    barcodes = pyzbar.decode(img)
    for barcode in barcodes:
        b_data = barcode.data.decode('utf-8')
        b_type = barcode.type
        (x, y, w, h) = barcode.rect
        xc = x + w/2
        yc = y + h/2
        print('Found {} with data {} with center at x={}, y={}'.format(b_type, b_data, xc, yc))


navigate_wait(z=1, frame_id='body', auto_arm=True)
rospy.sleep(1)
navigate_wait(x=1, y=0, z=1, frame_id='aruco_map', speed=0.5)
rospy.sleep(1)
navigate_wait(x=1, y=0, z=2, frame_id='aruco_map', speed=0.5)
rospy.sleep(1)
navigate_wait(x=1, y=1, z=2, frame_id='aruco_map', speed=0.5)
image_sub = rospy.Subscriber('main_camera/image_raw_throttled', Image, image_callback, queue_size=1)
rospy.sleep(3)
navigate_wait(x=1, y=2, z=2, frame_id='aruco_map', speed=0.5)
rospy.sleep(1)
navigate_wait(x=1, y=2, z=1, frame_id='aruco_map', speed=0.5)
rospy.sleep(1)
navigate_wait(x=0, y=2, z=1, frame_id='aruco_map', speed=0.5)
rospy.sleep(1)
navigate_wait(x=0, y=0, z=1, frame_id='aruco_map', speed=0.5)
rospy.sleep(1)
land_wait()