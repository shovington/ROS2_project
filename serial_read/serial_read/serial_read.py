import serial
import time

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class SerialRead(Node):

    def __init__(self):
        super().__init__('serial_read')
        self.publisher_ = self.create_publisher(String, 'arduino_serial', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.ser = serial.Serial(port='/dev/ttyACM1', baudrate=115200, timeout=.1)
        
        # self.ser.flushInput()
        # self.ser.flushOutput()


    def write_read(self, x):
        self.ser.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        data = self.ser.readline()
        return data.decode('utf-8')

    def timer_callback(self):
        msg = String()
        encoded_string = self.ser.readline()
        try:
            string = encoded_string.decode('utf-8')
            msg.data = string
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: "%s"' % msg.data)
        # except Exception as e: 
        #     self.get_logger().warn(e)
        except:
            pass

        print("sending bytes to arduino")
        string = self.write_read("test0")
        print("response" + string + "\n")
        
def main(args=None):
    rclpy.init(args=args)

    serial_read = SerialRead()

    rclpy.spin(serial_read)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    serial_read.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()