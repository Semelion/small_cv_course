"""Сохранить ArUco DICT_4X4_50 с белым полем; ID по умолчанию 7."""
import argparse
from pathlib import Path
import cv2 as cv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', type=int, default=7)
    args = parser.parse_args()
    if not 0 <= args.id < 50:
        parser.error('Для DICT_4X4_50 ID должен быть от 0 до 49.')
    if not hasattr(cv, 'aruco') or not hasattr(cv.aruco, 'generateImageMarker'):
        raise SystemExit('Нужен современный opencv-contrib-python; проверьте интерпретатор.')
    dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
    marker = cv.aruco.generateImageMarker(dictionary, args.id, 300)
    printable = cv.copyMakeBorder(marker, 60, 60, 60, 60, cv.BORDER_CONSTANT, value=255)
    output = Path(__file__).resolve().parents[1] / 'assets' / f'aruco_4x4_50_id{args.id}.png'
    output.parent.mkdir(parents=True, exist_ok=True)
    if not cv.imwrite(str(output), printable):
        raise SystemExit(f'Не удалось сохранить {output}')
    print(output)


if __name__ == '__main__':
    main()
