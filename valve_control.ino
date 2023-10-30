const int valve1 = 2;
const int led_pin = 13;

unsigned long valveActiveTime = 0;
unsigned long startTime = 0;

void setup() {
  pinMode(valve1, OUTPUT);
  pinMode(led_pin, OUTPUT);
  digitalWrite(valve1, HIGH); // HIGH = valve closed 
  digitalWrite(led_pin, LOW);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    if (Serial.read() == 'v') {
      valveActiveTime = Serial.parseInt();
      startTime = millis();
      digitalWrite(valve1, LOW);
      digitalWrite(led_pin, HIGH);
    }
    while (Serial.available() > 0) {
      Serial.read(); // Flush the buffer
    }
  }

  if (valveActiveTime > 0 && (millis() - startTime >= valveActiveTime)) {
    digitalWrite(valve1, HIGH);
    digitalWrite(led_pin, LOW);
    valveActiveTime = 0;
  }
}