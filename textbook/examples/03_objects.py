# Запускай из папки CV_course: python textbook/examples/03_objects.py
import cv2 as cv

img = cv.imread('textbook/assets/scene.png')
if img is None:
    raise FileNotFoundError('Не найдено textbook/assets/scene.png. Запусти из CV_course.')

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
mask = cv.inRange(hsv, (40, 80, 60), (85, 255, 255))
selected = cv.bitwise_and(img, img, mask=mask)

overlay = img.copy()
overlay[mask > 0] = (0, 255, 255)
overlay = cv.addWeighted(img, 0.6, overlay, 0.4, 0)

contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
result = img.copy()
count = 0
for contour in contours:
    area = cv.contourArea(contour)
    if area < 500:
        continue
    count += 1
    x, y, w, h = cv.boundingRect(contour)
    cv.rectangle(result, (x, y), (x + w - 1, y + h - 1), (0, 200, 255), 3)
    cv.putText(result, 'green ' + str(count), (x, y - 10),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 2, cv.LINE_AA)
    print('Площадь:', area, 'Рамка:', x, y, w, h)
print('Найдено объектов:', count)

cv.imwrite('textbook/assets/generated/mask.png', mask)
cv.imwrite('textbook/assets/generated/selected.png', selected)
cv.imwrite('textbook/assets/generated/overlay.png', overlay)
cv.imwrite('textbook/assets/generated/objects.png', result)
cv.imshow('mask', mask)
cv.imshow('selected', selected)
cv.imshow('overlay', overlay)
cv.imshow('objects', result)
cv.waitKey(0)
cv.destroyAllWindows()
