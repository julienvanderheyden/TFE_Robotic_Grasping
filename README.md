# Reliable Robotic Grasping for Uncertain Objects through Virtual Model Control

## Introduction

This project was developed as the Master's Thesis of Julien Vanderheyden at the University of Liège. It focuses on controlling a ShadowHand robotic hand to perform reliable grasping of uncertain objects using two main strategies:

- **Trajectory Planner**: A direct, predefined motion sequence.  
- **Object-Centric**: A more dynamic strategy that adapts to the shape of the object.

Three grasp types are implemented:
- Medium Wrap  
- Power Sphere  
- Lateral Pinch  

## Table of Contents

- [Installation](#installation)
- [Structure](#structure)
- [Usage](#usage)    
- [Examples](#examples,)  


## Installation

The only required package is the Julia module `VMRobotControl.jl`, found in the `julia/` directory.

```julia
cd julia
include("VMRobotControl.jl")
```

## Structure 

```graphql
├── my_package/              # ROS package containing communication and execution nodes
│   ├── src/                 # Python ROS nodes (e.g., rospy_client.py, rh_ros_bridge.py, etc.)
│   ├── launch/              # ROS launch files
│   ├── urdf/                # Robot description files (URDF)
│   ├── rviz/                # RViz visualization configurations
│   ├── include/             # (Optional) C++ headers or interface files
│   ├── package.xml          # ROS package metadata
│   └── CMakeLists.txt       # ROS build script
│
├── julia/                   # Julia codebase for grasp planning and control
│   ├── hand control files/  # Julia scripts for executing trajectory and object-centric grasps
│   │   ├── trajectory_planner_*.jl
│   │   ├── object_centric_*.jl
│   ├── notebooks/           # Jupyter notebooks for simulation, design, and analysis
│   │   └── *.ipynb
│   └── VMRobotControl.jl    # Julia module handling robotic control logic
│
├── plot/                    # Scripts for analyzing and visualizing experiment data
│   ├── csv_plotter.py
│   ├── csv_mismatch_plotter.py
│   ├── csv_coupled_mismatch_plotter.py
│   └── csv_animation.ipynb
```


## Usage

### Design and Simulation

Navigate to `julia/notebooks` and run the available notebooks for understanding the design of each of the 6 available grasps.

### Real Robot Control

Before launching any grasping operation, ensure the following ROS nodes are running:

```bash
rosrun my_package rospy_client.py 24 \shadowhand_command_topic \shadowhand_state_topic
rosrun my_package rh_ros_bridge.py <store_data>
```

`rospy_client` makes the link between Julia and ROS while `rh_ros_bridge` takes care of routing the command and state on the right topics, and can also be used to store data into a spreadsheet.

Arguments for `rh_ros_bridge.py`:
- `store_data` (boolean value)
- `--csv_filename=<name>`  
- `--row_limit=<max_rows>`  
- `--rfj0_reset_value=<value between 0 and 3.14>`  

#### Optional ROS Utilities

**RA Shaker (UR10 Arm Shaking)**

```bash
rosrun my_package ra_shaker.py <grasp_index>
# grasp_index: 1 (medium wrap), 2 (power sphere), 3 (lateral pinch)

rostopic pub /start_testing_x std_msgs/Empty "{}"
rostopic pub /start_testing_z std_msgs/Empty "{}"
```

**Hand Preshape**

```bash
rosrun my_package rh_hand_preshape.py <grasp_index>
# grasp_index: 0 (reset), 1–3 as above
```

### Grasp Execution (in Julia)

**Trajectory Planner Grasp**

```julia
include("trajectory_planner_medium_wrap.jl")
include("trajectory_planner_power_sphere.jl")
include("trajectory_planner_lateral_pinch.jl")
```

**Object-Centric Grasp**

```julia
include("object_centric_medium_wrap.jl")
object_centric_medium_wrap(cylinder_radius)

include("object_centric_power_sphere.jl")
object_centric_power_sphere(sphere_radius)

include("object_centric_lateral_pinch.jl")
object_centric_lateral_pinch(box_half_width, box_half_thickness)
```


## Examples

**Execute Object-Centric Grasp for a 2cm Radius Cylinder**
```julia
include("object_centric_medium_wrap.jl")
object_centric_medium_wrap(0.02)
```

**Reset Hand and Launch Trajectory Planner Power Sphere**
```bash
rosrun my_package rh_hand_preshape.py 0
```
```julia
include("trajectory_planner_power_sphere.jl")
```

