// Обычный Raspberry Pi Pico: три отдельных LED через резисторы.
// 2, 3, 4 — номера GPIO, а не физических контактов.
void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  Serial.begin(115200);
  Serial.setTimeout(100);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "r") {
      digitalWrite(2, HIGH);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      Serial.println("OK r");
    } else if (command == "g") {
      digitalWrite(2, LOW);
      digitalWrite(3, HIGH);
      digitalWrite(4, LOW);
      Serial.println("OK g");
    } else if (command == "b") {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, HIGH);
      Serial.println("OK b");
    } else if (command == "off") {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      Serial.println("OK off");
    } else {
      Serial.println("ERR command");
    }
  }
}
