from clover import srv
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from clover import long_callback
from std_srvs.srv import Trigger
import rospy
import math
import numpy as np

print('The drone has started.')
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

h_found = False
h_position = None

@long_callback
def image_callback(msg):
    global h_found, h_position
    img = bridge.imgmsg_to_cv2(msg, 'bgr8')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define the range of blue color in HSV
    lower_blue = np.array([90, 100, 100])
    upper_blue = np.array([130, 255, 255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)

    # Find contours in the mask
    contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:  # Assuming the letter H is represented by a rectangle
            x, y, w, h = cv2.boundingRect(contour)
            xc = x + w / 2
            yc = y + h / 2
            if not h_found:
                print('Found H at image coordinates x={}, y={}'.format(xc, yc))
                h_found = True
                h_position = (xc, yc)

navigate_wait(z=1, frame_id='body', auto_arm=True)
rospy.sleep(1)
navigate_wait(x=1, y=0, z=1, frame_id='aruco_map', speed=0.5)
rospy.sleep(1)
navigate_wait(x=1, y=0, z=1, frame_id='aruco_map', speed=0.5)
rospy.sleep(1)
navigate_wait(x=1, y=1, z=1, frame_id='aruco_map', speed=0.5)
rospy.sleep(1)
image_sub = rospy.Subscriber('main_camera/image_raw_throttled', Image, image_callback, queue_size=1)

# Wait until H is found
while not h_found and not rospy.is_shutdown():
    rospy.sleep(1)

if h_position:
    # Assuming the pixel coordinates can be mapped to the drone's coordinate system
    # This is a simplification; you may need a more complex transformation
    x_target, y_target = h_position

    # Convert image coordinates to world coordinates
    # This is a placeholder transformation; adjust according to your setup
    world_x = x_target / 100.0  # Example transformation
    world_y = y_target / 100.0  # Example transformation

    navigate_wait(x=world_x, y=world_y, z=0.5, frame_id='aruco_map', speed=0.5)
    rospy.sleep(10)
    land_wait()

print('Klyanus H nashel')
print('Bomb has been planted.')
