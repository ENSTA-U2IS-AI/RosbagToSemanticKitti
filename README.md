# RosbagToSemanticKitti : automatic conversion from a rosbag to the SemanticKitti format (LiDAR part)

This package was made to convert a **Rosbag** with LiDAR frames (`PointCloud2`) into the architecture of the [**SemanticKitti Dataset**](http://www.semantic-kitti.org/index.html), using user-friendly python scripts. This repository has also a tool to perform automatic labeling. It calculates the angles of the normals on the estimated surface described by each point, and compares them to a threshold.

## Install all the requirements

This repository was tested with Python 3.8 and [**ROS Noetic**](http://wiki.ros.org/noetic/Installation/Ubuntu) with the `sensor_msgs/PointCloud2` ROS message type. **So, make sure you have it installed !**

Make sure to have all the [requirements](requirements.txt) for this repository. If you have pip installed, you can try :

```bash
pip install -r requirements.txt
```

## Conversion of the point clouds

The script [convert_pointcloud](convert_pointcloud.py) reads a given rosbag and write the corresponding `.bin` file for each frame of the LiDAR in the right folder.

* We have the following options:
  * `-b, --bagfile [String]` : Path to the bagfile
  * `-d, --dataset [String]`: Path to the dataset
  * `-t, --topic [String]`: Name of the topic of the Point Cloud (PointCloud2 format)
  * `--id [String]`: Name of the sequence (default `'00'`)
  * `-n, --name [String]`: Name of the folder of the point cloud files (default `'velodyne'`)

These indications are also available by using `-h`, it will display all the above informations

## Automatic labeling using normal orientation threshold

The script [label_normals](label_normals.py) proceeds automatic labeling for each cloud point created with the previous script and write them in a `.label` file. The id of each point is `0`.

We have developed this algorithm for labeling point clouds:

1. Estimate the normal on each point considering a number of neighboors to estimate the local surface
2. For each normal, compares its angle with a reference vector (here, the relative vertical)
3. If the angle is above the define threshold, the point is labeled as _obstacle_ (`1`) otherwise, the point is labeled as _free space_ (`0`)

* We have the following options:
  * `-d, --dataset [String]`: Path to the dataset
  * `--id [String]`: Name of the sequence (default `'00'`)
  * `-b, --bin [String]`: Name of the bin folder (set previously)
  * `-n, --name [String]`: Name of the folder of the labels files (default `'labels'`)
  * `-a, --angle [Float]`: Threshold angle in degrees
  * `--neighboor [Int]`: Number of neighboors used in normal estimation

These indications are also available by using `-h`, it will display all the above informations

## Generate poses

For each sequence, a file named `poses.txt` has to be generated. This, can be done by using (according to the SemanticKitti website) a [surfel-based SLAM approach (SuMa)](http://jbehley.github.io/projects/surfel_mapping/index.html).

## Calibration file

Originally, in the SemanticKitti Dataset, different sensors (LiDAR and cameras) have been used. So, for each sequences, there is a file named `calib.txt` that contains all the projection matrices.
This repository contains [a default file](example/calib.txt) (identity matrix for each sensor), and can be used for example if you only have one sensor and/or no calibration file.

## Example

In the folder [example/](example/), you can try the execution of the different scripts by building an example dataset from a given rosbag in this folder. To do so, make sure you have the required permissions (`chmod +x example.sh`) and execute the bash script named [example.sh](example/example.sh). The only file that is missing is the `poses.txt` because it requires the execution of the [SuMa](http://jbehley.github.io/projects/surfel_mapping/index.html) script as mentionned before.

Little reminder : if you want to know the different information about the rosbag, open a terminal and type :

```bash
roscore
```

And in another terminal :

```bash
rosbag info bag_example.bag
```
