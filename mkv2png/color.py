# 根据强度值归一化后的数值 可视化点云
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
def get_mpl_colormap(cmap_name):
    cmap = plt.get_cmap(cmap_name)
    # Initialize the matplotlib color map
    # Obtain linear color range
    x = np.linspace(0, 1, 256)
    x1 = np.linspace(0, 0.2, 50)
    x2 = np.linspace(0.2, 0.6, 100)
    x3 = np.linspace(0.6, 1, 106)
    y = np.concatenate([x1, x2, x3], 0)
    # y =plt.Normalize(np.min(y),np.max(y))
    sm = plt.cm.ScalarMappable(cmap=cmap)
    color_range = sm.to_rgba(y, bytes=True)[:, 2::-1]
    plt.figure()
    # xx=np.linspace(0,255,256)
    xx=[1]*len(y)
    
    # row = np.array(color_range).shape[0]   #获取行数n
    # for i in range(0,row ):
    #     print("{",color_range[i][0],",",color_range[i][1],",",color_range[i][1],"}",",")
    plt.scatter(y,xx,c=(color_range.reshape(256, 3).astype(np.float32) / 255.0))
    # plt.colorbar(sm)
    plt.show()
    #np.savetxt("/home/liubo/Downloads/mkvpng/a.txt", color_range, fmt = '%d', delimiter = ',')
    return color_range.reshape(256, 3).astype(np.float32) / 255.0


if __name__ == '__main__':
# 强度预测值可视化
    pre_remissions5000_2=np.random.randint(0,20,size=16)
    range_data = np.copy(pre_remissions5000_2)  #pre_remissions5000_2为强度值
    viridis_range = ((range_data - range_data.min()) /
                    (range_data.max() - range_data.min()) *
                    255).astype(np.uint8)
    viridis_map = get_mpl_colormap("coolwarm")
    viridis_colors = viridis_map[viridis_range]
    print("Down")
# self.scan_infer_vis5000.set_data(self.scan.points5000,#points5000为xyz点的坐标
#                                  face_color=viridis_colors[..., ::-1],  # self.scan.pre_label_color
#                                  edge_color=viridis_colors[..., ::-1],
#                                  siz



