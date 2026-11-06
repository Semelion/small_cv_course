"""Отрисовка ArUco: камера или статическое изображение для проверки без камеры."""
import argparse
from pathlib import Path
import cv2 as cv


def make_detector():
    if not hasattr(cv, 'aruco') or not hasattr(cv.aruco, 'ArucoDetector'):
        raise RuntimeError('Нужен современный OpenCV с cv2.aruco.ArucoDetector. Проверьте интерпретатор и установку opencv-contrib-python (см. учебник).')
    dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
    parameters = cv.aruco.DetectorParameters()
    return cv.aruco.ArucoDetector(dictionary, parameters)


def annotate(frame, detector):
    corners, ids, rejected = detector.detectMarkers(frame)
    result = frame.copy()
    if ids is not None:
        cv.aruco.drawDetectedMarkers(result, corners, ids)
    return result, ids


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--camera', type=int, default=0)
    parser.add_argument('--image', type=Path, help='Проверка на файле вместо камеры')
    parser.add_argument('--no-gui', action='store_true', help='Только с --image: не открывать окно')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'assets' / 'aruco_detected.png')
    args = parser.parse_args()
    if args.no_gui and args.image is None:
        parser.error('--no-gui используется вместе с --image')
    detector = make_detector()
    if args.image is not None:
        frame = cv.imread(str(args.image))
        if frame is None:
            raise RuntimeError(f'Не удалось прочитать изображение: {args.image}')
        result, ids = annotate(frame, detector)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if not cv.imwrite(str(args.output), result):
            raise RuntimeError(f'Не удалось сохранить {args.output}')
        print('Найденные ID:', [] if ids is None else ids.flatten().tolist())
        print('Результат:', args.output)
        if not args.no_gui:
            try:
                cv.imshow('ArUco result', result)
                cv.waitKey(0)
            finally:
                cv.destroyAllWindows()
        return
    cap = cv.VideoCapture(args.camera)
    try:
        if not cap.isOpened():
            raise RuntimeError('Камера не открылась. Проверьте разрешение доступа, закройте другие приложения или попробуйте --camera 1.')
        while True:
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError('Не удалось получить кадр с камеры.')
            result, ids = annotate(frame, detector)
            cv.imshow('ArUco | Q or Esc to exit', result)
            if cv.waitKey(1) & 0xFF in (ord('q'), ord('Q'), 27):
                break
    finally:
        cap.release()
        cv.destroyAllWindows()


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, cv.error) as error:
        raise SystemExit(str(error))
