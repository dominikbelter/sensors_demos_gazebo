# sensors_demos_gazebo

Sensor demos for **Gazebo Sim** (`gz sim`, via `ros_gz`) on ROS 2 Lyrical.
(The original version targeted Gazebo Classic / `gazebo_ros_pkgs`, which is not
available in ROS 2 Jazzy and newer.)

Installation:

1. In your workspace `src` directory: `git clone https://github.com/Jakubach/sensors_demos_gazebo.git`
2. `sudo rosdep init` 
3. `rosdep update`
4. `rosdep install --from-paths src -y --ignore-src --rosdistro lyrical`
5. `colcon build`

Running:
1. In your workspace main directory: `source install/setup.bash`
2. Running with `launch` files:

Hokuyo sensor:

*  `ros2 launch sensors_demos_gazebo hokuyo_launch.py`

Imu sensor:

* `ros2 launch sensors_demos_gazebo imu_launch.py`

Kinect sensor:

* `ros2 launch sensors_demos_gazebo kinect_launch.py`

Ultrasonic promixity sensor:

* `ros2 launch sensors_demos_gazebo ultrasonic_launch.py`
  

Published topics:

| Demo | Topics |
|---|---|
| hokuyo | `/hokuyo/scan` (LaserScan) |
| imu | `/imu/data` (Imu), `/joint_states` |
| kinect | `/kinect/color/image_raw`, `/kinect/color/camera_info`, `/kinect/depth/image_rect_raw`, `/kinect/depth/camera_info`, `/kinect/depth_registered/points` |
| ultrasonic | `/ultrasonic/range` (Range), `/ultrasonic/scan` (raw cone rays) |

Notes:

* All demos load `worlds/sensors_world.sdf` (ground plane plus a few obstacles in front of the sensor).
* Gazebo Sim has no Range sensor: the ultrasonic sensor is a narrow 5x5-ray lidar,
  and the `ultrasonic_range` node converts it to `sensor_msgs/Range`.
* The world uses the Bullet-featherstone physics engine, because the Lyrical DART
  binary currently fails to load (`liboctomap.so.1.9` missing).
