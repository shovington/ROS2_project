// Motor A connections
int enA = 9;
int in1 = 8;
int in2 = 7;
// Motor B connections
int enB = 3;
int in3 = 5;
int in4 = 4;

int cmd [2];
int ByteReceived = 0;
const char *delimiter =",";
char *token;
const char * searchedPattern1 = "CMD";

void setup() {

	Serial.begin(115200);

  Serial.setTimeout(100);
	// Set all the motor control pins to outputs
	pinMode(enA, OUTPUT);
	pinMode(enB, OUTPUT);
	pinMode(in1, OUTPUT);
	pinMode(in2, OUTPUT);
	pinMode(in3, OUTPUT);
	pinMode(in4, OUTPUT);

  pinMode(10, OUTPUT);
	// Turn off motors - Initial state
	digitalWrite(in1, LOW);
	digitalWrite(in2, LOW);
	digitalWrite(in3, LOW);
	digitalWrite(in4, LOW);

}

void loop() {

  if (Serial.available() > 0) {
    // Serial.print(Serial.available());
    String incomingString = Serial.readStringUntil('>');

    char str_array[incomingString.length()+1];
    incomingString.toCharArray(str_array, incomingString.length()+1);
    token = strtok(str_array, delimiter);

    char * pointer1 = strstr(token, searchedPattern1);
    if(pointer1)
    {
      token=strtok(NULL, delimiter);
      int i = 0;
      while (token != NULL) {
        cmd[i] = atoi(token);
        token=strtok(NULL, delimiter);
        i++;
      }
    }
  }
	speedControl(cmd);


}

void speedControl(int* cmd) {

  if (cmd[0] >= 0)
  {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(enA, cmd[0]);
  }
  else
  {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(enA, -cmd[0]);
  }

  if (cmd[1] >= 0)
  {
    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    analogWrite(enB, cmd[1]);
  }
  else
  {
    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    analogWrite(enB, -cmd[1]);
  }
}

