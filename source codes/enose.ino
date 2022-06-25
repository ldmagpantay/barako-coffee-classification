//Electronic Nose Arduino Code

int mq2_dout = 2;
int mq7_dout = 3;
int mq135_dout = 4;
int mq137_dout = 5;

int mq2_analog = A5;
int mq7_analog = A4;
int mq135_analog = A3;
int mq137_analog = A2;

void setup() {
  Serial.begin(9600);//sets the baud rate

  //D-Out
  pinMode(mq2_dout, INPUT);
  pinMode(mq7_dout, INPUT);
  pinMode(mq135_dout, INPUT);
  pinMode(mq137_dout, INPUT);

  //Analog
  pinMode(mq2_analog, INPUT);
  pinMode(mq7_analog, INPUT);
  pinMode(mq135_analog, INPUT);
  pinMode(mq137_analog, INPUT);

  delay(1000);
}

void loop(){
  int mq2 = analogRead(mq2_analog);
  int mq7 = analogRead(mq7_analog);
  int mq135 = analogRead(mq135_analog);
  int mq137 = analogRead(mq137_analog);

  Serial.print(mq2);
  Serial.print('x');
  Serial.print(mq7);
  Serial.print('x');
  Serial.print(mq135);
  Serial.print('x');
  Serial.print(mq137);

  Serial.print('\n');
  delay(1000);
}
