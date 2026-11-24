import numpy as np
import cv2

file_name = "cam_calib.npz"

try:
    calib_data = np.load(file_name)
    print("成功读取文件！文件里包含的键名有：",calib_data.files)
    camera_mtx = calib_data['mtx']
    dist_coeffs = calib_data['dist']
    
    print("内参 camera_mtx 是：\n", camera_mtx)
    print("畸变 dist_coeffs 是: \n",dist_coeffs)

except Exception as e:
    print("出错了：", e)
