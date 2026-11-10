"""Живое видео. Запуск: python textbook/examples/04_camera.py --camera 0"""
import argparse
import cv2 as cv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--camera', type=int, default=0, help='Номер камеры: 0, 1, ...')
    args = parser.parse_args()
    cap = cv.VideoCapture(args.camera)
    try:
        if not cap.isOpened():
            raise RuntimeError('Камера не открылась. Проверьте разрешение доступа, закройте другие приложения или попробуйте --camera 1.')
        while True:
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError('Не удалось получить кадр. Проверьте подключение камеры.')
            cv.imshow('Camera | Q or Esc to exit', frame)
            key = cv.waitKey(1) & 0xFF
            if key in (ord('q'), ord('Q'), 27):
                break
    finally:
        cap.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, cv.error) as error:
        raise SystemExit(str(error))
