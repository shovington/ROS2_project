FROM osrf/ros:humble-desktop
 
# Change the default shell to Bash
SHELL [ "/bin/bash" , "-c" ]
 
# Install Git
RUN apt-get update && apt-get install -y git
 
# Create a Catkin workspace and clone TurtleBot3 repos
RUN source /opt/ros/humble/setup.bash \
 && mkdir -p /ros2_ws/src \
 && cd /ros2_ws/src \
 && git clone https://github.com/shovington/ROS2_project.git \
 && git clone https://github.com/shovington/ros2-third-party-robot.git

RUN cd /ros2_ws \
 && rosdep install --from-paths src -y --ignore-src \
 && apt-get install nlohmann-json3-dev
 
# Build the Catkin workspace and ensure it's sourced
RUN source /opt/ros/humble/setup.bash \
 && cd ros2_ws \
 && colcon build
RUN echo "source /ros2_ws/install/setup.bash" >> ~/.bashrc
 
# Set the working folder at startup
WORKDIR /ros2_ws