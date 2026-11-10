# Запускай из папки CV_course: python textbook/examples/01_pixels.py
import cv2 as cv

img = cv.imread('textbook/assets/scene.png')
if img is None:
    raise FileNotFoundError('Не найдено textbook/assets/scene.png. Запусти из CV_course.')

print('Размер:', img.shape)
print('Тип:', img.dtype)
print('BGR пикселя x=100, y=120:', img[120, 100])
height, width = img.shape[:2]

crop = img[80:240, 60:260].copy()
changed = img.copy()
changed[120, 100] = (255, 255, 255)
changed[115:126, 95:106] = (255, 255, 255)

tinted = img.copy()
for y in range(height):
    for x in range(width):
        b, g, r = img[y, x]
        tinted[y, x] = (int(b), int(g), min(255, int(r) + 60))

cv.imwrite('textbook/assets/generated/crop.png', crop)
cv.imwrite('textbook/assets/generated/pixel.png', changed)
cv.imwrite('textbook/assets/generated/tinted.png', tinted)
cv.imshow('original', img)
cv.imshow('crop', crop)
cv.imshow('pixel', changed)
cv.imshow('tinted', tinted)
cv.waitKey(0)
cv.destroyAllWindows()
