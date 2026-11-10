# Запускай из папки CV_course: python textbook/examples/02_colors.py
import cv2 as cv

img = cv.imread('textbook/assets/scene.png')
if img is None:
    raise FileNotFoundError('Не найдено textbook/assets/scene.png. Запусти из CV_course.')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
print('BGR shape:', img.shape)
print('GRAY shape:', gray.shape)
print('HSV shape:', hsv.shape)
print('Зеленый пиксель BGR:', img[120, 100])
print('Тот же пиксель HSV:', hsv[120, 100])
h, s, v = cv.split(hsv)

cv.imwrite('textbook/assets/generated/gray.png', gray)
cv.imwrite('textbook/assets/generated/hue.png', h)
cv.imwrite('textbook/assets/generated/saturation.png', s)
cv.imwrite('textbook/assets/generated/value.png', v)
cv.imshow('original', img)
cv.imshow('gray', gray)
cv.imshow('H', h)
cv.imshow('S', s)
cv.imshow('V', v)
cv.waitKey(0)
cv.destroyAllWindows()
