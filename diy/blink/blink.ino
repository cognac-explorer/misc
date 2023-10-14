void setup() {
    for (int i = 2; i < 7; i++) {
        pinMode(i, OUTPUT);
    }
}

void allLEDsOff(void)
{
    for (int i = 2; i < 7; i++) {
        digitalWrite(i, LOW);
    }
}

void loop() {
    // move one direction
    for (int i = 2; i < 7; i++) {
        allLEDsOff();
        for (int j = 1; j < i; j++) {
            digitalWrite(i, HIGH);
            delay(100);
            digitalWrite(i, LOW);
            delay(100);
        }
    }
    // reverse direction
     for (int i = 6; i > 2; i--) {
        allLEDsOff();
        digitalWrite(i, HIGH);
        delay(100);
    }
}