import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_path
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command

import xacro

'''
def generate_launch_description():
    doc = xacro.process_file(os.path.join(get_package_share_directory('sensors_demo_gazebo'), 'imu.urdf.xacro'), mappings={'radius': '0.9'})
    robot_desc = doc.toprettyxml(indent='  ')
    params = {'robot_description': robot_desc}
    rsp = Node(package='robot_state_publisher',
                                  node_executable='robot_state_publisher_node',
                                  output='both',
                                  parameters=[params])

    return LaunchDescription([rsp])
'''







def generate_launch_description():

  use_sim_time = LaunchConfiguration('use_sim_time', default='false')
  urdf_file_name = 'imu.urdf.xacro'

  print("urdf_file_name : {}".format(urdf_file_name))

  urdf = os.path.join(
      get_package_share_directory('sensors_demo_gazebo'), urdf_file_name)

  #path_to_urdf = get_package_share_path('sensors_demo_gazebo') / 'urdf' / 'imu.urdf.xacro'
  
  #xacro_file = os.path.join(get_package_share_directory('sensors_demo_gazebo'), 'urdf/', 'imu.urdf.xacro')
  #assert os.path.exists(xacro_file), "The box_bot.xacro doesnt exist in "+str(xacro_file)
  
  xacro_file = urdf
  assert os.path.exists(xacro_file), "The imu.urdf.xacro doesnt exist in "+str(xacro_file)
  robot_description_config = xacro.process_file(xacro_file)
  robot_desc = robot_description_config.toxml()
  
  return LaunchDescription([
  
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'),
            
        #Node(
        #    package='robot_state_publisher',
        #    executable='robot_state_publisher',
        #    name='robot_state_publisher',
        #    output='screen',
        #    parameters=[{'use_sim_time': use_sim_time}],
        #    arguments=[urdf]),                 


        #Node(
    #		package='robot_state_publisher',
    #		executable='robot_state_publisher',
   # 		parameters=[{'robot_description': ParameterValue(
   #          	Command(['xacro ', str(urdf)]), value_type=str
   #     )
   # 	}]
	#	),
	Node(package="robot_state_publisher",executable="robot_state_publisher",name="robot_state_publisher",parameters=[{"robot_description": robot_desc}],output="screen"),		
	Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}]
            ),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='urdf_spawner',
            output='screen',
            arguments=["-topic", "/robot_description", "-entity", "imu.urdf.xacro"])
  ])
  

