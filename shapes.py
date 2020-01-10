import numpy as np
import cv2
import mpcspy
import glob
import os
from tqdm import tqdm
from pathlib import Path

config = mpcspy.read_config('config.py')

# Folders
Path(config.save_path).mkdir(parents=True, exist_ok=True)
highres = os.path.join(config.save_path, 'HR')
bicubic = os.path.join(config.save_path, f'LR_bicubic/X{config.scale}')
Path(highres).mkdir(parents=True, exist_ok=True)
Path(bicubic).mkdir(parents=True, exist_ok=True)

for img_idx in tqdm(range(config.n_images)):
    # Create background with DIV2K Mean color
    image = np.ones((config.height, config.width, 3), dtype=np.uint8)
    image[:, :, 0] = image[:, :, 0] * config.color_mean[2] # B
    image[:, :, 1] = image[:, :, 1] * config.color_mean[1] # G
    image[:, :, 2] = image[:, :, 2] * config.color_mean[0] # R

    for i in range(config.n_shapes):
        shape = np.random.randint(0, 2)

        # Center (Gaussian)
        # x = int(np.random.normal(config.location_x_mean, config.location_x_std))
        # y = int(np.random.normal(config.location_y_mean, config.location_y_std))

        # Center (Uniform)
        x = int(np.random.uniform(0, config.width))
        y = int(np.random.uniform(0, config.height))

        # Color
        r = int(np.random.normal(config.color_mean[0], config.color_std[0]))
        g = int(np.random.normal(config.color_mean[1], config.color_std[1]))
        b = int(np.random.normal(config.color_mean[2], config.color_std[2]))

        if shape: # Rectangle
            rectangle_width = int(np.random.normal(config.rectangle_mean, config.rectangle_std))
            rectangle_height = int(np.random.normal(config.rectangle_mean, config.rectangle_std))
            if not config.rotated_rectangles:
                pt1 = (x - rectangle_width//2, y - rectangle_height//2)
                pt2 = (x + rectangle_width//2, y + rectangle_height//2)
                cv2.rectangle(image, pt1, pt2, (b, g, r), -1, lineType=cv2.LINE_AA)
            else:
                yaw = np.random.uniform(0.0, 2*np.pi)
                rect = ((x, y), (rectangle_width, rectangle_height), np.degrees(yaw))
                box = np.int0(cv2.boxPoints(rect))
                cv2.drawContours(image, [box], 0, (b, g, r), -1, lineType=cv2.LINE_AA)
        else: # Circle
            circle_radius = int(np.random.normal(config.radius_mean, config.radius_std))
            circle_radius = max(1, circle_radius)
            cv2.circle(image, (x, y), circle_radius, (b, g, r), -1, lineType=cv2.LINE_AA)

    # Low Res
    resized = cv2.resize(image, (config.width//config.scale,
        config.height//config.scale), interpolation=cv2.INTER_CUBIC)

    # Save
    name = f'{img_idx+1}'.zfill(len(str(config.n_images)))
    cv2.imwrite(os.path.join(highres, f'{name}.png'), image)
    cv2.imwrite(os.path.join(bicubic, f'{name}_x{config.scale}.png'), resized)
