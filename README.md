# RosbagToSemanticKitti : automatic way to convert a rosbag into the SemanticKitti format (LiDAR part)

This package was made convert a Rosbag into files and folder, following the architecture of the [SemanticKitti Dataset](http://www.semantic-kitti.org/index.html), using user-friendly python scripts.

## Conversion of the point clouds

The script named `convert_pointcloud.py` reads a given rosbag and write the corresponding `.bin` file for each frame of the LiDAR in the right folder. 

 * We have the following options:
     * ```-b, --bagfile [String]``` : Path to the bagfile
     * ```-d, --dataset [String]```: Path to the dataset
     * ```-t, --topic [String]```: Name of the topic of the Point Cloud (PointCloud2 format)
     * ```--id [String]```: Name of the sequence (default ```'00'```)
     * ```-n, --name [String]```: Name of the folder of the pointcloud files (default ```'velodyne'```)

These indications are also available by using ```-h```, it will display all the above informations

## Automatic labelisation using normal orientation threshold

The script named `label_normals.py` proceeds automatic labelisation for each cloud point created with the previous script and write them in a `.label` file. The id of each point is `0`.

 * We have the following options:
     * ```-d, --dataset [String]```: Path to the dataset
     * ```--id [String]```: Name of the sequence (default ```'00'```)
     * ``` -b, --bin [String]```: Name of the bin folder (set previously)
     * ```-n, --name [String]```: Name of the folder of the labels files (default ```'labels'```)
     * ```-a, --angle [Float]```: Threshold angle in degrees
     * ```--neighboor [Int]```: Number of neighboors used in normal estimation

These indications are also available by using ```-h```, it will display all the above informations

## Generate poses

For each sequence, a file named `poses.txt` has to be generated. This, can be done by using (according to the SemanticKitti website) a [surfel-based SLAM approach (SuMa)](http://jbehley.github.io/projects/surfel_mapping/index.html).

## Calibration file

Originally, in the SemanticKitti Dataset, different sensors (LiDAR and cameras) have been used. So, for each sequences, there is a file named `calib.txt` that contains all the projection matrices.
In this repository, a default file is made (identity matrix for each sensor), in the ```example/``` folder.

## Example

In the folder ```example/```, you can try the execution of the different script by building an example dataset from a given rosbag in this folder. To do so, make sure you have the required permissions (```chmod +x example.sh```) and execute the bash script named ```example.sh```. The only file that is missing is the ```poses.txt`` because it requires the execution of the [SuMa](http://jbehley.github.io/projects/surfel_mapping/index.html) script as mentionned before.

Little reminder : if you want to know the different information about the rosbag, open a terminal and type :

```bash
roscore
```
And in another terminal :
```bash
rosbag info bag_example.bag
```
