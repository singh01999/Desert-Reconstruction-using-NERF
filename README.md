# Results on youtube
- Playlist Link: [nerf results](https://www.youtube.com/playlist?list=PLpE2rfLkAl1BEUv8hyF6kycmggXIhf_T3)

# 3D Desert Reconstruction using NeRF
Title: Neural Radiance Fields (NeRF) based 3D Scene Reconstruction of a Desert Environment

It contains 2 folders one for collected datasets and another for unity project to collect simulated data. Instant NGP is used for NeRF reconstruction for which its official repository is provided below.
It also contain one python script used to preprocess data whose steps are mentioned below.

## Unity ROS Camera (package) - Data Collection
### A simple robot with 4 wheels
- A simple urdf file is created (along with xacro). This urdf file is imported to unity using urdf importer.
- A differential drive robot controller is implemented in unity. This subscribe to "cmd_vel" topic and generate commands for movement of robot in unity.

### LIDAR (3D laser Scanner)
- A 3D laser scanner sensor is implement using Ray Casting. It has parameters such as fov, angular_resolution (both horizontal and vertical), min_range, max_range etc.
- A Point Cloud publisher publish the generated point cloud to 'point_cloud' topic. It aslo publish the pose (position and orientation) of the laser_scanner to 'laser_scan_pose'.

### Camera
- A camera is attached to the robot which can be moved using ROS.

 ### Notes
 - This package is in ROS2 meaning unity scripts in this are written for ROS2, so if you will select ROS1 in unity (in [ROS-TCP-Connector](https://github.com/Unity-Technologies/ROS-TCP-Connector)) it will show compilation error. By default ROS2 is selected but if you want to run this in ROS1 you have to modify scripts accordingly.
 - Please do read how unity-ros framework works. [ROS Unity Hub](https://github.com/Unity-Technologies/Unity-Robotics-Hub) [ROS Unity Integration](https://github.com/Unity-Technologies/Unity-Robotics-Hub/blob/main/tutorials/ros_unity_integration/README.md)
 - User can edit xacro file and then generate urdf from it. And import new urdf into the unity to try different robot.
 - User can edit all parameters either from unity script or from panel.

### Installation and Running
- Read ROS-Unity integration (try few examples to get the grasp on ros-unity framework works in general). [ROS Unity Hub](https://github.com/Unity-Technologies/Unity-Robotics-Hub) [ROS Unity Integration](https://github.com/Unity-Technologies/Unity-Robotics-Hub/blob/main/tutorials/ros_unity_integration/README.md)

#### Installation
- Download this package and open in unity.
- Create a ros workspace and build package [ROS-TCP-Endpoint](https://github.com/Unity-Technologies/ROS-TCP-Endpoint) in the workspace by downloading approriate branch (ROS or [ROS2 Branch of ROS-TCP-Endpoint](https://github.com/Unity-Technologies/ROS-TCP-Endpoint/tree/main-ros2) ) from github.
- Install teleop-twist-keyboard package to control robot using keyboard
  - `sudo apt-get install ros-noetic-teleop-twist-keyboard` change the ROS-DISTRO name from neotic to your ROS-DISTRO

#### Running
- Run ROS-TCP-Endpoint Server in one terminal [ROS–Unity Demo Setup](https://github.com/Unity-Technologies/Unity-Robotics-Hub/blob/main/tutorials/ros_unity_integration/setup.md)
  - ROS1: `roslaunch ros_tcp_endpoint endpoint.launch`
  - ROS2: `ros2 run ros_tcp_endpoint default_server_endpoint`
- Click on play button in unity to start the simualtion
- Run rviz in another terminal and add tf and point cloud topics to rviz for displaying them
  - ROS1: `rosrun rviz rviz`
  - ROS2: `rviz2`
- Run teleop_twist_keyboard in another terminal and control the robot using keyboard
  - ROS1: `rosrun teleop_twist_keyboard teleop_twist_keyboard.py`
  - ROS2: `ros2 run teleop_twist_keyboard teleop_twist_keyboard`
 

 ## Nerf Reconstruction
 Follow following steps
 - Clone the Official repo of instant NGP: [instant-ngp](https://github.com/NVlabs/instant-ngp) and install required dependencies like pytorch, numpy, cuda etc.
 - Create a folder dataset (collect your own or use provided here)
 - If using real dataset, follow the instructions provided in the instant NGP repo to prerpocess data using COLMAP
 - If using simulated data, run the convert.py script using below command
  - `convert.py <path to dataset>`
  - It will create a file named 'transforms.json'
 - Run the following command in the base folder of instant-ngp folder
  - `./instant-ngp <path to dataset>`  

## Credits
- Most of the code is from [Navigation 2 SLAM Example](https://github.com/Unity-Technologies/Robotics-Nav2-SLAM-Example). Following addition/modifications are made
  - Laser scanner code to make it scan in 3D as well as fast and publish [point cloud message](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/PointCloud2.html).
  - AGVController script has been modified and renamed as Robot Controller to control 4 wheel robot instead of 2.

