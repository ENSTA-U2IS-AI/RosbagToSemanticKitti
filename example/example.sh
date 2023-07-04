#!/bin/bash

: '
This script creates an example by executing the different scripts.
Copyright (C) 2023 Antoine DOMINGUES, ENSTA Paris

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'

cat << EOF
example.sh Copyright (C) 2023  Antoine DOMINGUES, ENSTA Paris
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
EOF

mkdir example_dataset
python3 ../convert_pointcloud.py -b ./bag_example.bag -d ./example_dataset -t /rslidar_points --id 00 -n example_bin
python3 ../label_normals.py -d ./example_dataset --id 00 -b example_bin -n example_labels -a 30 --neighboor 50
cp calib.txt ./example_dataset/calib.txt