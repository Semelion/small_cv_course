import cv2 as cv

img = cv.imread('civic.jpeg')

cv.imshow('image', img)
cv.waitKey(0)
cv.destroyAllWindows()