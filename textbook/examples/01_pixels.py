"""Матрица, обрезка и окрашивание. Запуск: python examples/01_pixels.py"""
from pathlib import Path
import argparse
import cv2 as cv
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-gui', action='store_true')
    args = parser.parse_args()
    img = cv.imread(str(ROOT / 'assets/scene.png'))
    if img is None:
        raise FileNotFoundError(ROOT / 'assets/scene.png')
    height, width = img.shape[:2]
    print('shape:', img.shape, 'dtype:', img.dtype)
    print('BGR пикселя x=100, y=120:', img[120, 100])
    crop = img[80:240, 60:260].copy()
    marked = img.copy()
    marked[120, 100] = (255, 255, 255)
    marked[115:126, 95:106] = (255, 255, 255)  # Увеличим метку до 11×11.
    tinted = img.copy()
    for y in range(height):
        for x in range(width):
            b, g, r = img[y, x]
            tinted[y, x] = (int(b), int(g), min(255, int(r) + 60))
    # Та же операция сразу над каналом; int16 предотвращает переполнение uint8.
    fast = img.copy()
    fast[:, :, 2] = np.clip(img[:, :, 2].astype(np.int16) + 60, 0, 255).astype(np.uint8)
    assert np.array_equal(tinted, fast)
    out = ROOT / 'assets/generated'
    out.mkdir(exist_ok=True, parents=True)
    for name, result in [('crop', crop), ('pixel', marked), ('tinted', tinted)]:
        if not cv.imwrite(str(out / f'{name}.png'), result):
            raise OSError(f'Не удалось сохранить {name}')
        if not args.no_gui:
            cv.imshow(name, result)
    if not args.no_gui:
        cv.waitKey(0)
        cv.destroyAllWindows()
    print('Сохранено:', out)


if __name__ == '__main__':
    main()
