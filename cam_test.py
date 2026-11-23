import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

if not cap.isOpened():
   print("打不开摄像头！")
else:
   while True:
       ret, frame = cap.read()
       if not ret:
           print("读取图像失败")
           break
       cv2.imshow("camera", frame)
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break
cap.release()
cv2.destroyAllWindows()
   
