import serial
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

from std_msgs.msg import String


class SerialRead(Node):

    def __init__(self):
        super().__init__('serial_read')
        self.publisher_ = self.create_publisher(String, 'arduino_serial', 10)
        timer_period = 0.05  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.joy_sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)

        self.ser = serial.Serial(port='/dev/ttyACM1', baudrate=115200, timeout=0, write_timeout=0.01)
        time.sleep(2)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.joystick_input = Joy()

    def joy_callback(self, msg):
        self.joystick_input = msg

        right = self.joystick_input.axes[4]
        left = self.joystick_input.axes[1]
        right = int(right*255)
        left = int(left*255)
        # right_sign = self.joystick_input.axes[4]/right
        # left_sign = self.joystick_input.axes[1]/left

        cmd = "CMD," + str(right) + "," + str(left) + ">"
        print(cmd)
        try:
            self.ser.write(bytes(cmd, 'utf-8'))
        except Exception as e:
            print(e)
            print("Error in writing")
        print("Sent")


    def timer_callback(self):
        pass
        # nb_bytes = self.ser.in_waiting
        # print(nb_bytes)
        # msg = String()
        # encoded_string = self.ser.readline()
        # try:
        #     string = encoded_string.decode('utf-8')
        #     msg.data = string
        #     self.publisher_.publish(msg)
        #     self.get_logger().info('Publishing: "%s"' % msg.data)
        # except Exception as e: 
        #     print(e)
        #     print("Error in decoding")

        
def main(args=None):
    rclpy.init(args=args)

    serial_read = SerialRead()

    try:
        rclpy.spin(serial_read)
    except KeyboardInterrupt:
        serial_read.ser.close()

        # Destroy the node explicitly
        # (optional - otherwise it will be done automatically
        # when the garbage collector destroys the node object)
        serial_read.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()