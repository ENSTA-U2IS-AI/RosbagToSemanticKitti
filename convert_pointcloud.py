import os
import rosbag
import argparse
import numpy as np
import sensor_msgs.point_cloud2 as pc2
from tqdm import tqdm


# Define all parameters using a parser
parser = argparse.ArgumentParser(
    description="Convert a rosbag into files .bin using the SemanticKitti architecture."
)
parser.add_argument(
    "-b",
    "--bagfile",
    required=True,
    help="path of the bagfile",
)
parser.add_argument(
    "-d",
    "--dataset",
    required=True,
    help="path of the resulting dataset",
)
parser.add_argument(
    "-t",
    "--topic",
    required=True,
    help="name of the LiDAR topic",
)
parser.add_argument(
    "--id",
    default="00",
    required=False,
    help="id of the sequence",
)
parser.add_argument(
    "-n",
    "--name",
    default="velodyne",
    required=False,
    help="name of the LiDAR",
)
args = parser.parse_args()

# Define all the parameters
path_bagfile = args.bagfile
path_dataset = args.dataset
topic_lidar = args.topic
id_sequence = args.id
name_sensor = args.name

# Create all the folders if needed
sequences_folder = os.path.join(path_dataset, "sequences")
id_sequence_folder = os.path.join(sequences_folder, id_sequence)
data_folder = os.path.join(id_sequence_folder, name_sensor)
folderExist = os.path.exists(data_folder)
if not folderExist:
    os.makedirs(data_folder)

# Read the bag
bag = rosbag.Bag(path_bagfile, "r")
for index, (topic, msg, t) in tqdm(enumerate(bag.read_messages(topic_lidar))):
    # Generate the point list
    pc_list = list(pc2.read_points(msg))
    # Convert the list into an array
    pc_array = np.array(pc_list)
    x = pc_array[:, 0]
    y = pc_array[:, 1]
    z = pc_array[:, 2]
    intensity = pc_array[:, 3]
    # Prepare data to generate .bin file
    arr = np.zeros(
        x.shape[0] + y.shape[0] + z.shape[0] + intensity.shape[0], dtype=np.float32
    )
    arr[::4] = x
    arr[1::4] = y
    arr[2::4] = z
    arr[3::4] = intensity

    # Generate the file and type in float32
    path_file = os.path.join(data_folder, "{0:06d}.bin".format(int(index)))
    arr.astype("float32").tofile(path_file)
bag.close()