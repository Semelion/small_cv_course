import cv2 as cv

marker_id = 7
output = 'textbook/assets/aruco_4x4_50_id7.png'

dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
marker = cv.aruco.generateImageMarker(dictionary, marker_id, 300)
printable = cv.copyMakeBorder(
    marker, 60, 60, 60, 60, cv.BORDER_CONSTANT, value=255
)

saved = cv.imwrite(output, printable)
if saved:
    print('Маркер сохранён:', output)
else:
    print('Не удалось сохранить маркер. Проверь путь:', output)
