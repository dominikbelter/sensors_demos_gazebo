"""Convert the simulated ultrasonic cone (a small lidar) into sensor_msgs/Range.

Gazebo Sim has no native Range output, so the sensor is modelled as a 5x5-ray
lidar and this node reports the closest valid return as a single range.
"""
import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Range


class UltrasonicRange(Node):

    def __init__(self):
        super().__init__('ultrasonic_range')
        self.declare_parameter('field_of_view', 0.314)
        self.pub = self.create_publisher(Range, 'ultrasonic/range', 10)
        self.create_subscription(LaserScan, 'ultrasonic/scan', self.on_scan, 10)

    def on_scan(self, scan):
        valid = [r for r in scan.ranges
                 if math.isfinite(r) and scan.range_min <= r <= scan.range_max]
        msg = Range()
        msg.header = scan.header
        msg.radiation_type = Range.ULTRASOUND
        msg.field_of_view = self.get_parameter('field_of_view').value
        msg.min_range = scan.range_min
        msg.max_range = scan.range_max
        msg.range = min(valid) if valid else math.inf
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = UltrasonicRange()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
