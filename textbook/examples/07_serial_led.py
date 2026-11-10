import time
import serial
from serial.tools import list_ports

# Показываем порты и выбираем плату.
for port in list_ports.comports():
    print(port.device, port.description)

port_name = input("Введите порт платы: ").strip()
board = serial.Serial(port_name, 115200, timeout=1, write_timeout=2)
time.sleep(2)  # Даём плате время после открытия порта.

try:
    while True:
        command = input("r / g / b / off / q: ").strip().lower()
        if command == "q":
            command = "off"
            board.write((command + "\n").encode("ascii"))
            answer = board.readline().decode("ascii").strip()
            if answer:
                print(answer)
            else:
                print("Нет ответа: выключение не подтверждено.")
            break

        if command not in ["r", "g", "b", "off"]:
            print("Введите r, g, b, off или q.")
            continue

        board.write((command + "\n").encode("ascii"))
        answer = board.readline().decode("ascii").strip()
        if answer:
            print(answer)
        else:
            print("Нет ответа за 1 секунду. Проверьте порт и прошивку.")
finally:
    board.close()
