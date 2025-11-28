import os
from ament_index_python import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Get package path and URDF file path
    pkg_path = get_package_share_directory('matrix_bot')
    urdf_file = os.path.join(pkg_path, 'urdf', 'Matrix_bot.urdf')
    
    # READ URDF CONTENT as string
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Robot state publisher - pass URDF CONTENT, not path
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': use_sim_time}],
    )
    
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use sim time if true'),
        node_robot_state_publisher,
        rviz,
    ])
