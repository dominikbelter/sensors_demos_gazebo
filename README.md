# sensors_demos_gazebo package simulates various sensors in the Gazebo environment

To start simulation use commands:

- IMU unit

  Launching: 
  
  ```roslaunch sensors_demos_gazebo imu.launch```
  
  Joint moving example:
  
  ```rostopic pub /joint1_controller/command std_msgs/Float64 "data: 0.5"```
  
- Kinect sensor

   ```roslaunch sensors_demos_gazebo kinect.launch```
  
- Hokuyo UTM 30

   ```roslaunch sensors_demos_gazebo hokuyo.launch```

