import cv2 as cv

dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
parameters = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(dictionary, parameters)

camera = 0
cap = cv.VideoCapture(camera)

if not cap.isOpened():
    print('Камера не открылась. Проверь доступ к камере или измени camera на 1.')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print('Не удалось получить кадр.')
        break

    corners, ids, rejected = detector.detectMarkers(frame)
    if ids is not None:
        cv.aruco.drawDetectedMarkers(frame, corners, ids)

    cv.imshow('ArUco', frame)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv.destroyAllWindows()
