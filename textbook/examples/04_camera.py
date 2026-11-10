import cv2 as cv

camera = 0
cap = cv.VideoCapture(camera)

if not cap.isOpened():
    print('Камера не открылась. Проверь доступ к камере или измени camera на 1.')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print('Не удалось получить кадр.')
        break

    cv.imshow('Camera', frame)
    key = cv.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv.destroyAllWindows()
