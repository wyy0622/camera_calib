import cv2
#打开相机
cap = cv2.VideoCapture(0)
#判断相机是否成功打开
if not cap.isOpened():
    print("相机打开失败！")
    exit()
#计数，给图片命名
pic_num = 0
while True:
#读取一帧画面
    ret, img = cap.read()
    if ret == False:
        print("读取画面失败")
        break
   #显示画面窗口
    cv2.imshow("采集标定图片 | s保存 q退出",img)
    #监听按键
    key = cv2.waitKey(1)
    #按s保存
    if key == ord('s'):
       cv2.imwrite(f"calib_{pic_num}.jpg",img)
       print(f"成功保存第{pic_num}张：calib_{pic_num}.jpg")
       pic_num = pic_num + 1
    #按q退出采集
    elif key == ord('q'):
       break
cap.release()
cv2.destroyAllWindows()
       
