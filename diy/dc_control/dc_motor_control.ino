void setup()
{
    pinMode(6, OUTPUT);
    pinMode(13, OUTPUT);
}
void loop()
{
    // slow speed
    digitalWrite(13, LOW);
    for (int i = 0; i < 50; i++) {
        analogWrite(6, 30) ;
        delay(100);
    }
    // accelerate to max
    for (int i = 0; i < 256; i++) {
        analogWrite(6, i) ;
        delay(10);
    }
    // wait and change direction
    // now use max speed
    delay(1000);
    digitalWrite(13, HIGH);
    digitalWrite(6, LOW);
    delay(1000);
}