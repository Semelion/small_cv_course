"""BGR → GRAY и HSV. Запуск: python textbook/examples/02_colors.py"""
import argparse
import cv2 as cv



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-gui', action='store_true')
    args = parser.parse_args()
    img = cv.imread('textbook/assets/scene.png')
    if img is None:
        raise FileNotFoundError('textbook/assets/scene.png')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    print('BGR shape:', img.shape, 'GRAY shape:', gray.shape, 'HSV shape:', hsv.shape)
    print('Зеленый пиксель, BGR:', img[120, 100], 'HSV:', hsv[120, 100])
    h, s, v = cv.split(hsv)
    out = 'textbook/assets/generated'
    for name, result in [('gray', gray), ('hue', h), ('saturation', s), ('value', v)]:
        if not cv.imwrite(f'{out}/{name}.png', result):
            raise OSError(f'Не удалось сохранить {name}')
        if not args.no_gui:
            cv.imshow(name, result)
    if not args.no_gui:
        cv.waitKey(0)
        cv.destroyAllWindows()
    print('Сохранено:', out)


if __name__ == '__main__':
    main()
