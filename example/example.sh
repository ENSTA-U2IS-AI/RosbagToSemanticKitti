#!/bin/bash
mkdir example_dataset
python3 ../convert_pointcloud.py -b ./bag_example.bag -d ./example_dataset -t /rslidar_points --id 00 -n example_bin
python3 ../label_normals.py -d ./example_dataset --id 00 -b example_bin -n example_labels -a 30 --neighboor 50
cp calib_example.txt ./example_dataset/calib.txt