import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    pkg_share = get_package_share_directory('sensors_demos_gazebo')
    xacro_file_name = 'kinect.urdf.xacro'
    xacro_file = os.path.join(pkg_share, xacro_file_name)
    world_file = os.path.join(pkg_share, 'worlds', 'sensors_world.sdf')

    robot_desc = xacro.process_file(xacro_file).toxml()

    # Gazebo Sim (server + GUI), started unpaused (-r)
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r -v 3 {world_file}',
                          'on_exit_shutdown': 'true'}.items())

    # Spawn the model read from /robot_description
    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=['-topic', 'robot_description', '-name', 'kinect'])

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': True}])

    # Gazebo -> ROS topic bridge ('[' means Gazebo to ROS)
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/kinect/image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/kinect/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
            '/kinect/depth_image@sensor_msgs/msg/Image[gz.msgs.Image',
            '/kinect/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked',
        ],
        remappings=[
            ('/kinect/image', '/kinect/color/image_raw'),
            ('/kinect/camera_info', '/kinect/color/camera_info'),
            ('/kinect/depth_image', '/kinect/depth/image_rect_raw'),
            ('/kinect/points', '/kinect/depth_registered/points'),
        ],
        parameters=[{'use_sim_time': True}])

    return LaunchDescription([
        gz_sim,
        robot_state_publisher,
        spawn,
        bridge,
        # Same intrinsics for the depth image (registered RGB-D camera)
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='depth_camera_info_bridge',
            output='screen',
            arguments=['/kinect/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo'],
            remappings=[('/kinect/camera_info', '/kinect/depth/camera_info')],
            parameters=[{'use_sim_time': True}]),
    ])
