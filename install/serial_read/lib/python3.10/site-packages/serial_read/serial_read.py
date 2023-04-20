import serial
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

from std_msgs.msg import String, Float32MultiArray


class SerialRead(Node):

    def __init__(self):
        super().__init__('serial_read')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'velocity', 10)
        timer_period = 0.05  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.joy_sub = self.create_subscription(Joy, 'joy', self.joy_callback, 10)

        self.ser = serial.Serial(port='/dev/ttyACM1', baudrate=115200, timeout=0, write_timeout=0.01)
        time.sleep(2)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.previous_encoder = [0, 0]

        self.joystick_input = Joy()

    def joy_callback(self, msg):
        self.joystick_input = msg

        left = self.joystick_input.axes[4]
        right = self.joystick_input.axes[1]
        right = int(right*255)
        left = int(left*255)
        # right_sign = self.joystick_input.axes[4]/right
        # left_sign = self.joystick_input.axes[1]/left

        cmd = "CMD," + str(right) + "," + str(left) + ">"
        try:
            self.ser.write(bytes(cmd, 'utf-8'))
        except Exception as e:
            print(e)
            print("Error in writing")


    def timer_callback(self):
        msg = Float32MultiArray()
        encoded_string = self.ser.readline()
        try:
            string = encoded_string.decode('utf-8')
            ticks = string.rstrip().split(',')
            velocity = (float(ticks[1])*0.205, float(ticks[2])*0.205)

            # lowpass filter
            velocity = (0.5*velocity[0] + 0.5*self.previous_encoder[0], 0.5*velocity[1] + 0.5*self.previous_encoder[1])
            self.previous_encoder = velocity
            print("Velocity : ", velocity)
            msg.data = velocity
            # msg.data = str(velocity[0]) + "," + str(velocity[1])
            self.publisher_.publish(msg)
            # self.get_logger().info('Speed: "%s"' % msg.data)
        except Exception as e: 
            print(e)
            print("Error in decoding")

        
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