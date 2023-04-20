import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
 
def generate_launch_description():
    ld = LaunchDescription()

    urdf_file_name = 'urdf/lawn_mower.urdf'
    urdf = os.path.join(
        get_package_share_directory('lawn_mower_robot'),
        urdf_file_name)
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    cartographer_config_dir = urdf = os.path.join(
        get_package_share_directory('lawn_mower_robot'),
        'config')
    

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name='robot_state_publisher',
        parameters=[{
                "robot_description": robot_desc
            }]
    )

    cartographer_node = Node(
        package="cartographer_ros",
        executable="cartographer_node",
        name='cartographer_node',
        remappings=[('echoes', '/scan')],
        arguments=['-configuration_directory', cartographer_config_dir,
               '-configuration_basename', 'cartographer_config.lua'
               ]
    )

    cartographer_occupancy_grid_node = Node(
        package="cartographer_ros",
        executable="cartographer_occupancy_grid_node",
        name='cartographer_occupancy_grid_node',
        arguments=['-resolution', '0.05']
    )
 
    ld.add_action(robot_state_publisher)
    ld.add_action(cartographer_node)
    ld.add_action(cartographer_occupancy_grid_node)
    return ld