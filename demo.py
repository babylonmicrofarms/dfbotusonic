# Copyright   [DFRobot](http://www.dfrobot.com), 2016
# Copyright   GNU Lesser General Public License
import time
from dfbotusonic.a02yyuw_ultrasonic_sensor import A02YYUWUltrasonicSensor, Status

DEFAULT_DEV_ID = "/dev/ttyAMA0"
dev_id = input(
    f"Enter the device file id linked to the DFRobot Ultrasonic UART interface default is ({DEFAULT_DEV_ID}): "
)
if dev_id == "":
    dev_id = DEFAULT_DEV_ID 

usonic_sensor = A02YYUWUltrasonicSensor(dev_id=dev_id)


def print_state():
    print(
        f"Status: {Status(usonic_sensor.status).name},\tDistance: {usonic_sensor.distance}"
    )


if __name__ == "__main__":
    while True:
        usonic_sensor.read()
        print_state()
        time.sleep(0.3)
