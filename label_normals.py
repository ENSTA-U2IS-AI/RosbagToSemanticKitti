"""Binary labelisation of .bin point clouds using normal estimation.
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
"""

print(
    """label_normals.py Copyright (C) 2023  Antoine DOMINGUES, ENSTA Paris
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions."""
)

import os
import argparse
import numpy as np
import open3d as o3d
from tqdm import tqdm

# Define all parameters using a parser
parser = argparse.ArgumentParser(
    description="Binary label of .bin files (SemanticKitti) using normal estimation."
)
parser.add_argument(
    "-d",
    "--dataset",
    required=True,
    help="path of the dataset",
)
parser.add_argument(
    "--id",
    required=True,
    help="id of the sequence",
)
parser.add_argument(
    "-b",
    "--bin",
    required=True,
    help="name of the bin folder",
)
parser.add_argument(
    "-n",
    "--name",
    default="labels",
    required=False,
    help="name of the label folder",
)
parser.add_argument(
    "-a",
    "--angle",
    default=30,
    type=float,
    required=False,
    help="threshold angle in degrees",
)
parser.add_argument(
    "--neighboor",
    default=50,
    type=int,
    required=False,
    help="number of neighboor in normal estimation",
)
args = parser.parse_args()

# Define all the parameters
path_dataset = args.dataset
id_sequence = args.id
folder_data = args.bin
folder_id = args.name
angle_degree = args.angle
nb_neighboors = args.neighboor

# Create all the folders if needed
sequences_folder = os.path.join(path_dataset, "sequences")
id_sequence_folder = os.path.join(sequences_folder, id_sequence)
label_folder = os.path.join(id_sequence_folder, folder_id)
folderExist = os.path.exists(label_folder)
if not folderExist:
    os.makedirs(label_folder)


def open_bin(file_path):
    # Open file (float32 format)
    data = np.fromfile(file_path, dtype=np.float32)
    # Reshape in 4 columns (x, y, z, intensity)
    return np.reshape(data, (-1, 4))


def estimate_normals(point_cloud, num_neighbors=50):
    # Convert the numpy array to an Open3D point cloud
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud[:, :3])

    # Estimate normals
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamKNN(num_neighbors))

    # Get the normal vectors
    normals = np.asarray(pcd.normals)

    return normals


def label_points(normals, reference=np.array([0, 0, 1])):
    # Initialize the output array
    label_array = np.zeros((normals.shape[0], 1), dtype=int)
    # Check if normalsiation is needed
    ref_norm2 = np.dot(reference.T, reference)
    if ref_norm2 != 1:
        normalised_ref = reference / ref_norm2**0.5
    else:
        normalised_ref = reference

    # Determine angle threshold 
    cos_angle = np.cos(np.deg2rad(angle_degree))

    # Calculate dot product for all normals at once
    dot_products = np.dot(normals, normalised_ref)

    # Check threshold and create an array of labels based on the dot product values
    label_array = np.where(np.abs(dot_products) <= cos_angle, 1, 0)

    return label_array


def write_label(label_array, folder_path, filename):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "wb+") as file:
        # For each label write in the right format
        for label in label_array:
            bin_label = np.uint32(label)
            # Id is set by default to 0
            file.write(bin_label)


# List of all files in the bin folder
bin_folder = os.path.join(id_sequence_folder, folder_data)
entries = os.listdir(bin_folder)

for bin_file in tqdm(entries):
    # Check if it is a .bin
    if bin_file[-4:] == ".bin":
        # Get the name of the file
        file_name = bin_file[:-4] + ".label"
        file_path = os.path.join(bin_folder, bin_file)
        # Open the bin file
        data_bin = open_bin(file_path)
        # Process normal estimation
        normals = estimate_normals(data_bin, nb_neighboors)
        # Generate an array of labels
        labels = label_points(normals)
        # Write the resulting .label file
        write_label(labels, label_folder, file_name)
