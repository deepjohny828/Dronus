# отец лох

from clover import srv
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from clover import long_callback
import rospy
import numpy as np

# Инициализация ROS-узла
rospy.init_node('color_scanner')

# Сервисы для управления дроном и LED-лентой
set_effect = rospy.ServiceProxy('led/set_effect', srv.SetLEDEffect)

# Инициализация CvBridge
bridge = CvBridge()

def get_dominant_color(image):
    # Преобразование изображения в цветовое пространство HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Определение диапазона цветов для поиска (например, все цвета)
    mask = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 255]))

    # Нахождение контуров
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return (0, 0, 0)  # Возвращаем черный цвет, если контуры не найдены

    # Нахождение самого большого контура
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Извлечение доминирующего цвета из области контура
    roi = image[y:y+h, x:x+w]
    average_color = cv2.mean(roi)[:3]

    return tuple(int(c) for c in average_color)

def get_color_name(r, g, b):
    # Определение имени цвета на основе значений RGB
    if r > 200 and g < 50 and b < 50:
        return "Red"
    elif r < 50 and g > 200 and b < 50:
        return "Green"
    elif r < 50 and g < 50 and b > 200:
        return "Blue"
    elif r > 200 and g > 200 and b < 50:
        return "Yellow"
    elif r < 50 and g > 200 and b > 200:
        return "Cyan"
    elif r > 200 and g < 50 and b > 200:
        return "Magenta"
    elif r > 200 and g > 200 and b > 200:
        return "White"
    elif r < 50 and g < 50 and b < 50:
        return "Black"
    else:
        return "Unknown"

@long_callback
def image_callback(msg):
    # Преобразование изображения из сообщения ROS в формат OpenCV
    img = bridge.imgmsg_to_cv2(msg, 'bgr8')

    # Получение доминирующего цвета
    dominant_color = get_dominant_color(img)
    b, g, r = dominant_color

    # Получение имени цвета
    color_name = get_color_name(r, g, b)

    # Вывод цвета в консоль
    print(f"Dominant color: {color_name} (G={g}, B={b}, R={r})")

    # Установка цвета LED-ленты
    set_effect(effect='fill', r=r, g=g, b=b)

    # Отображение изображения
    cv2.imshow('Image', img)
    cv2.waitKey(1)

# Подписка на топик камеры
image_sub = rospy.Subscriber('main_camera/image_raw', Image, image_callback, queue_size=1)

# Основной цикл
rospy.spin()
