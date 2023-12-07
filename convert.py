import argparse
import numpy as np
import json
from scipy.spatial.transform import Rotation
import math
import cv2

def transform_coordinates(c2w):
    c2w[0:3,2] *= -1 # flip the y and z axis
    c2w[0:3,1] *= -1
    c2w = c2w[[1,0,2,3],:]
    c2w[2,:] *= -1 # flip whole world upside down
    return c2w


def read_transformations(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    matrices = []
    avg_pos = np.array([0.0,0.0,0.0])
    for line in lines:
        elements = [float(x) for x in line.strip().split(',')]
        matrix = np.array(elements).reshape((4, 4)).T
        new_mat = transform_coordinates(matrix)
        avg_pos += new_mat[:3,3]
        matrices.append(new_mat.tolist())  # Convert NumPy array to a nested list
    
    avg_pos[1] *= -1
    avg_pos[2] *= -1
    avg_pos = avg_pos/len(matrices)
    return matrices, avg_pos

def sharpness(imagePath):
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = cv2.Laplacian(gray, cv2.CV_64F).var()
	return fm

def main():
    parser = argparse.ArgumentParser(description='Process transformations and create JSON data.')
    parser.add_argument('data_path', type=str, help='Path to the data directory')
    args = parser.parse_args()

    file_path = f"{args.data_path}/transforms.txt"
    transformations, avg_pos = read_transformations(file_path)

    scale = 0.02
    print(avg_pos)
    
    offset = (avg_pos*scale).tolist()

    offset[0]+=0.0 # height
    offset[1]+=0.5
    offset[2]+=0.5  

    # offset = [0, -3.5, 2]

    w, h = 1024, 720
    fovx, fovy = 120, 120
    
    camera_angle_x = fovx*math.pi/180
    camera_angle_y = fovy*math.pi/180
    fl_x = w / (2 * math.tan(camera_angle_x / 2))
    fl_y = h / (2 * math.tan(camera_angle_y / 2))

    # camera_angle_x = math.atan(w / (fl_x * 2)) * 2
    # camera_angle_y = math.atan(h / (fl_y * 2)) * 2
    # fovx = camera_angle_x * 180 / math.pi
    # fovy = camera_angle_y * 180 / math.pi


    data = {
        "camera_angle_x": camera_angle_x,
        "camera_angle_y": camera_angle_y,
        "fl_x": fl_x,
        "fl_y": fl_y,
        "k1": 0,
        "k2": 0,
        "k3": 0,
        "k4": 0,
        "p1": 0,
        "p2": 0,
        "is_fisheye": False,
        "cx": 512.0,
        "cy": 360.0,
        "w": w,
        "h": h,
        "scale": scale,
        "offset": offset,
        "aabb_scale": 4,
        "frames": []
    }

    # File paths and sharpness for frames
    file_paths = [f"/images/{i}.png" for i in range(len(transformations))]
    sharpness_value = 7739.0

    # Populate frames in data
    for i, matrix in enumerate(transformations):
        frame_data = {
            "file_path": f".{file_paths[i]}",
            "sharpness": sharpness(f"{args.data_path}{file_paths[i]}"),
            "transform_matrix": matrix
        }
        data["frames"].append(frame_data)

    # print(data)
    # Save data as JSON
    with open(f"{args.data_path}/transforms.json", "w") as json_file:
        json.dump(data, json_file, indent=2)

    # print("\n")
    # with open(f"{args.data_path}/transforms.json", "r") as json_file:
    #     loaded_data = json.load(json_file)
    # print(json.dumps(loaded_data, indent=2))

if __name__ == "__main__":
    main()
