#include <IRremote.h>
#include <Servo.h>

const int RECV_PIN = 7;
IRrecv irrecv(RECV_PIN);
decode_results results;

Servo servo;

void setup()
{
  Serial.begin(9600);
  irrecv.enableIRIn();
  irrecv.blink13(true);

  pinMode(5, OUTPUT);
  Serial.println("Hello");

  servo.attach(8);
  servo.write(0);
}

void loop()
{
  if (irrecv.decode(&results))
  {
    Serial.println(results.value, HEX);
    irrecv.resume();

    if(results.value == 0x2CA7FC6A) // 1ch
    {
      digitalWrite(5, HIGH);
      delay(50);
      digitalWrite(5, LOW);

      Serial.println("1 channel");

      for (int angle = 10; angle < 180; angle++)
      {
        servo.write(angle);
        delay(3);
      } 
    }

    if(results.value == 0x9FA1CDC3) // 2ch
    {
      digitalWrite(5, HIGH);
      delay(50);
      digitalWrite(5, LOW);

      Serial.println("2 channel");

      for (int angle = 180; angle > 10; angle--)
      {
        servo.write(angle);
        delay(3);
      } 
    }
  }
}

