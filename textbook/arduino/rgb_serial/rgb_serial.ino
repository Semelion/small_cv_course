// Reference: Raspberry Pi Pico, Arduino-Pico core by Earle Philhower.
// Three separate external LEDs, active HIGH. Numbers are GPIO, not header pins.
const int RED_PIN = 2;
const int GREEN_PIN = 3;
const int BLUE_PIN = 4;
String command;
bool overflow = false;

void setLeds(bool red, bool green, bool blue) {
  digitalWrite(RED_PIN, red ? HIGH : LOW);
  digitalWrite(GREEN_PIN, green ? HIGH : LOW);
  digitalWrite(BLUE_PIN, blue ? HIGH : LOW);
}

void handleCommand(String text) {
  text.trim();
  text.toLowerCase();
  if (text == "ping") {
    Serial.println("READY");
    return;
  }
  if (text == "r") setLeds(true, false, false);
  else if (text == "g") setLeds(false, true, false);
  else if (text == "b") setLeds(false, false, true);
  else if (text == "off") setLeds(false, false, false);
  else {
    Serial.println("ERR command");
    return;
  }
  Serial.print("OK ");
  Serial.println(text);
}

void setup() {
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);
  setLeds(false, false, false);
  command.reserve(16);
  Serial.begin(115200);
  // Do not wait forever for a PC: ping requests READY after port opening.
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {
      if (overflow) Serial.println("ERR too_long");
      else handleCommand(command);
      command = "";
      overflow = false;
    } else if (c != '\r' && !overflow) {
      if (command.length() < 16) command += c;
      else overflow = true;
    }
  }
}
