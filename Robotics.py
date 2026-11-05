import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read() 
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    Lower_red1 = np.array([0, 120, 70])
    Upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, Lower_red1, Upper_red1)

    Lower_red2 = np.array([170, 120, 70])
    Upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, Lower_red2, Upper_red2) 

    mask = mask1 + mask2

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Target Acquired", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
    cv2.imshow('Live Feed', frame)
    cv2.imshow('What the robot "sees"', mask) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

cap.release()
cv2.destroyAllWindows()
