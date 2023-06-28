# semantickitti标注数据可视化的测试版本

import numpy as np
import yaml
import os

filename="/home/liubo/Downloads/000000.label"

print(os.path.splitext(filename))
yaml_name="semantic-kitti copy.yaml"
try:
    print("Opening config file %s" %yaml_name )
    CFG = yaml.safe_load(open(yaml_name, 'r'))
except Exception as e:
    print(e)
    print("Error opening yaml file.")
    quit()
color_dict = CFG["color_map"]

sem_color_lut = np.zeros((348416, 3), dtype=np.float32)
for key, value in color_dict.items():
    # sem_color_lut[key] = np.array(value, np.float32) / 255.0
    print(color_dict[key])
    sem_color_lut[key] = np.array(color_dict[key],np.float32)/ 255.0
    

label=np.fromfile(filename,dtype=np.int32)
sem_label = label & 0xFFFF  # semantic label in lower half
inst_label = label >> 16    # instance id in upper half
print('da')
