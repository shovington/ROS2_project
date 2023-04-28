install docker : https://docs.docker.com/engine/install/ubuntu/
to build the docker 
    sudo docker build -t ros2_project .

To run the docker
    sudo docker run -it --network host ros2_project