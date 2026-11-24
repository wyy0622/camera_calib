import numpy as np#存矩阵
import cv2
file_name = "cam_calib.npz"
calib_data = np.load(file_name)#将npz中的数据导出来
#取出之前标定内参时得到的内参矩阵和畸变参数
mtx = calib_data['mtx']
dist_coeffs = calib_data['dist']

w=9
h=13
square_size = 0.015

objp = np.zeros((w*h,3),np.float32)
objp[:, :2] = np.mgrid[0:w,0:h].T.reshape(-1,2)
objp = objp*square_size

#4个3D世界座标点，x，y，z方向各延伸3cm，最后为原点
axis = np.float32([[0.03,0,0],
              [0,0.03,0],
              [0,0,0.03],
              [0,0,0]]).reshape(-1,3)

#找到角点之后迭代优化角点，让坐标更精准
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)
cap = cv2.VideoCapture(0)

while True:
   ret,frame = cap.read()#读一帧画面frame：读到的彩色图像
   if not ret:
      break
   gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
   ret_corner,corners = cv2.findChessboardCorners(gray,(w,h),None)
   if ret_corner:
      corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
      ret_pnp,rvec,tvec = cv2.solvePnP(objp,corners2,mtx,dist_coeffs)
      print("rvec: ",rvec)
      print("tvec: ",tvec)
      cv2,drawChessboardCorners(frame,(w,h),corners2,ret_corner)#在画面上画出识别到的棋盘角点，彩色连线，肉眼确认识别成功
      imgpts,_ = cv2.projectPoints(axis,rvec,tvec,mtx,dist_coeffs)#正向投影，将3维转化为2维，得到像素坐标
      imgpts = np.int32(imgpts).reshape(-1,2)#把投影出来的像素坐标转为整数像素格式，方便画线
      cv2.line(frame,imgpts[0],imgpts[3],(0,0,255),3)
      cv2.line(frame,imgpts[1],imgpts[3],(0,255,0),3)
      cv2.line(frame,imgpts[2],imgpts[3],(255,0,0),3)
   cv2.imshow("PnP",frame)
   if cv2.waitKey(1) & 0xFF == ord('q'):
      break
cap.release()
cv2.destroyAllWindows()
