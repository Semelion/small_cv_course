"""Управление тремя внешними LED через USB Serial RP2040, 115200."""
import argparse
import time

import serial
from serial.tools import list_ports


def send_line(port, command):
    port.write((command + "\n").encode("ascii"))
    port.flush()


def wait_reply(port, expected, seconds=2):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        reply = port.readline().decode("ascii", errors="replace").strip()
        if reply == expected:
            return reply
        if reply.startswith("ERR"):
            raise RuntimeError("Плата: " + reply)
    raise TimeoutError(f"Нет ответа {expected!r}. Проверьте прошивку и порт.")


def connect(port):
    # Плата отвечает на ping в любой момент, даже если стартовое READY потерялось.
    deadline = time.monotonic() + 8
    while time.monotonic() < deadline:
        send_line(port, "ping")
        try:
            wait_reply(port, "READY", seconds=0.6)
            return
        except TimeoutError:
            pass
    raise TimeoutError("Плата не ответила READY за 8 секунд.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", help="COM5 или /dev/cu.usbmodem... или /dev/ttyACM0")
    parser.add_argument("--list", action="store_true", help="Показать доступные порты")
    args = parser.parse_args()
    if args.list:
        ports = list(list_ports.comports())
        for item in ports:
            print(f"{item.device}: {item.description}")
        if not ports:
            print("Последовательные порты не найдены.")
        return
    if not args.port:
        parser.error("укажите --port; сначала можно выполнить --list")
    try:
        with serial.Serial(args.port, baudrate=115200, timeout=0.2,
                           write_timeout=2) as port:
            connect(port)
            print("READY: r — красный, g — зелёный, b — синий, off — погасить, q — выход")
            try:
                while True:
                    command = input("> ").strip().lower()
                    if command == "q":
                        break
                    if command not in {"r", "g", "b", "off"}:
                        print("Введите r, g, b, off или q.")
                        continue
                    send_line(port, command)
                    print(wait_reply(port, "OK " + command))
            except (KeyboardInterrupt, EOFError):
                print("\nВыход.")
            finally:
                # При штатном выходе гасим свет; обрыв USB этого не гарантирует.
                try:
                    send_line(port, "off")
                    wait_reply(port, "OK off")
                except (serial.SerialException, TimeoutError, RuntimeError):
                    print("Не удалось подтвердить выключение LED.")
    except (serial.SerialException, TimeoutError, RuntimeError) as exc:
        raise SystemExit(f"Ошибка связи: {exc}") from exc


if __name__ == "__main__":
    main()
