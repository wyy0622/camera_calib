import cv2
import numpy as np
import glob
#棋盘格:内角点 行7,列9；方格边长 0.02m
w = 9
h = 7
square_size = 0.02#棋盘单个小方格边长

#生成世界坐标系下棋盘内角点的3D坐标objp
objp = np.zeros((w*h,3),np.float32)
objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)#w，h，-1都是为了在修改数值时能够自适应，不用去做多次修改，-1这里是numpy的特殊记号，numpy自己算出有多少行
objp = objp*square_size#世界坐标系里的真实距离

obj_points = []#3D世界坐标
img_points = []#2D像素坐标

#读取所有calib_开头的照片
images = glob.glob("calib_*.jpg")
for fname in images:
    img = cv2.imread(fname)
    if img is None:
        print("跳过损坏文件：",fname)
        continue
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#转换图片颜色格式，彩变黑白
ret,corner = cv2.findChessboardCorners(gray,(w,h),None)#一次返回两个值 ret：能不能找到全部内角点         corner：如果可找到，即所有内角点的像素坐标
if ret==True:
  obj_points.append(objp)
  #像素精确化 ： 粗略角点变精度更高的角点
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,30,0.001)#亚像素角点优化的迭代终止条件：误差达标-0.001,达到最大迭代次数30次
  corners2 = cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)#（11,11）：窗口大小，（-1,-1）：全部区域参与计算
  img_points.append(corners2)
  cv2.drawChessboardCorners(img,(w,h),corners2,ret)#把我们找到并且优化好的棋盘角点画在图片上。corners2优化后角点坐标。
  cv2.imshow("chess",img)#弹出窗口显示图片
  cv2.waitKey(400)#等待按键程序才继续
cv2.destroyAllWindows()
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)#相机标定，ret：重投影误差，mtx：内参矩阵，dist：畸变系数，rvecs:旋转向量（外参），tvecs：平移向量（内参）
print("相机内参矩阵 mtx:")
print(mtx)
print("畸变系数 dist：")
print(dist)
np.savez("cam_calib.npz",mtx=mtx,dist=dist)
print("参数已经保存到 cam_calib.npz")
