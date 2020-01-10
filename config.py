save_path = './shapes2K'
n_images = 800
scale = 2

width, height = 2048, 1080
patch_size = 96

# Position (Gaussian Test)
# location_x_mean = width/2
# location_x_std = width/5
# location_y_mean = height/2
# location_y_std = height/5

# Radius
radius_mean = patch_size/4
radius_std = patch_size/10

# Rectangle
rectangle_mean = patch_size/2
rectangle_std = patch_size/5

# Color RGB (DIV2K)
color_mean = (114.35629928, 111.561547, 103.1545782)
color_std = (72.45974394708261, 68.87470687936465, 74.47221978843599)

n_shapes = 10000

rotated_rectangles = True

