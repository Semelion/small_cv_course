"""HSV → маска → контуры → рамки. Запуск: python textbook/examples/03_objects.py"""
import argparse
import cv2 as cv
import numpy as np



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-gui', action='store_true')
    parser.add_argument('--clean', action='store_true', help='Убрать мелкие точки морфологическим открытием')
    args = parser.parse_args()
    img = cv.imread('textbook/assets/scene.png')
    if img is None:
        raise FileNotFoundError('textbook/assets/scene.png')
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, (40, 80, 60), (85, 255, 255))
    if args.clean:
        kernel = np.ones((5, 5), np.uint8)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
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
        cv.putText(result, f'green {count}: {area:.0f}', (x, max(20, y - 10)),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 2, cv.LINE_AA)
        print(f'Объект {count}: area={area}, x={x}, y={y}, w={w}, h={h}')
    print('Найдено крупных зеленых объектов:', count)
    out = 'textbook/assets/generated'
    for name, image in [('mask', mask), ('selected', selected), ('overlay', overlay), ('objects', result)]:
        if not cv.imwrite(f'{out}/{name}.png', image):
            raise OSError(f'Не удалось сохранить {name}')
        if not args.no_gui:
            cv.imshow(name, image)
    if not args.no_gui:
        cv.waitKey(0)
        cv.destroyAllWindows()


if __name__ == '__main__':
    main()
