//Arduino Code Prim

// Order of to do:
// - Pin Assignment
// - Libraries 
// - Configs
// - 

//-------------- Libraries -------------------
#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>


//-------------- Pin Assignment ----------------
  //Colour pins
  const int greenPin = 5; // Green 
  const int yellowPin = 4; // Yellow
  const int redPin = 3; // Red
  
  //Buzzer Pins
  const int sigB = 2; // Signal Buzzer

  //Ultrasonic Sensor
  const int trig = 11; // Trigger Ultrasonic 
  const int echo = 10; // Echo Ultrasonic

  //Servo Pins
  const int sigS = 12; // Signal Servo





//--------- Config ---------
const long BAUD_RATE = 9600;
const int thresholdCM = 50; // Base threshold
const int minAngle = 0; // Min servo angle
const int maxAngle = 180; // Max servo Angle
const int stepAngle = 1; // Step size
const uint16_t servoMs = 20; // step interval
const uint32_t echoTOus = 20000UL; // Ultrasonic timeout

//------- Hysteresis & Stability --------
const int thresholdEnterCM = 50; // Enter Alert
const int thresholdExitCm = 55; // Exit Alert
const byte stableN = 3;         // Stable count
byte enterCnt = 0, exitCnt = 0;


//------ LCD -------
LiquidCrystal_I2C lcd(0x27, 16, 2);

//-------- Globals ---------
Servo scanner;
int anglecCur = minAngle;
int dir = +1;

bool alertNow = false;
bool lastAlert = false:

uint23_t tServoNext = 0;

//----- Buzzer scheduler ------
bool buzzOn = false;
uint32_t BuzzNext = 0; // When Buzzer next can buzz
uint16_t buzzOnMs = 20; // Change Buzzer on ms
uint16_t buzzOffMs = 200; // Change buzzer off ms

long lastDistCM = 9999; 

//------- Helpers --------
// Measure distance (cm)
long measureDistanceCM() {
	digitalWrite(trig, LOW);
	delayMircoseconds(2);
	digitalWrite(trig, HIGH);
	delayMircoseconds(10);
	digitalWrite(trig, LOW);
	
	unsigned long dur = pulseIn(echo, HIGH, echoTOus);
	if (dur == 0) return 9999;
	long cm = (long)(dur / 58.Of);
	if (cm <=0) cm = 9999;
	return cm; 
}

// Send Data to Serial
void sendData(int angle, long dist) {
	Serial.print(angle);
	Serial.print(",");
	Serial.print(dist);
	Serial.print(".");
}

// LED State
void setIdleIndicators() { //Idle
	digitalWrite(greenPin, HIGH);
	digitalWrite(redPin, LOW);
}

void setAlertIndicators() { //DANGER
	digitalWrite(redPin, HIGH);
	digitalWrite(greenPin, LOW);
}

// LCD messages
void lcdSetEmpty() {
	lcd.clear();
	lcd.setCursor(1, 0);
	lcd.print("We good");
	lcd.setCursor(0, 1);
	lcd.print("          ")
}

void lcdSetWarning() {
	lcd.clear();
	lcd.setCursor(4, 0);
	lcd.print ("Uh, we not good");
	lcd.setCursor(2, 1);
	lcd.print("Foriegn Object");
}

// Update LCD If stage changes
void updLCD(bool stage) {
	if (state != lastAlert) {
		if (state) lcdSetWarning();
		else lcdSetEmpty();
		lastAlert = state;	
	}
}
	
// Stable alert decision
bool computeStableAlert(long dist) {
	static bool state = false;
	if (!state){ 
		if (dist <= thresholdEnterCM) {
			if (++entercnt >= stableN) { state = true; enterCnt = 0; exitCnt = 0; }
			}
		else enterCnt = 0;
		}
	else {
		if (dist >=thresholdExitCM || dist == 9999) {
			if (++exitCnt >= stableN) { state = false; exitCnt = 0; enterCnt = 0; }
			}else exitCnt = 0;
		}
		return state;
	}
	
	
	
// Buzzer Timing 
void updBuzzScheduler(bool state, long dist) { 
	if (!state) {
	digitalWrite(sigB, LOW);
	buzzOn = false;
	return;
	}
	int mapped = map ((int)dist, 5, thresholdCM, 60, 300);
	mapped = constrain(mapped, 40, 400);
	buzzOffMs = (uint16_t)mapped;
}

// ------ Setup -------
void setup() {
	
	pinMode(greenPin, OUTPUT);
	pinMode(yellowPin, OUTPUT);
	pinMode(redPin, OUTPUT);
	pinMode(sigB, OUTPUT);
	pinMode(trig, OUTPUT);
	pinMode(echo, INPUT);

	Serial.begin(BAUD_RATE);

	scanner.attach(sigS);
	scanner.write(angleCur);

	lcd.init();
	lcd.backlight();
	lcd.clear();
	lcdSetEmpty();

	setIdleIndicators();

	uint32_t tNow = millis();
	tServoNext = tNow + servoMs;
	tBuzzNext = now;

}

// ------ Loop -------

void loop() {
  unit32_t now = millis();

  //Servo & Distance
	if ((int32_t)(now - tServoNext) >= 0) {
		tServoNext = now + servoMs;

		//Move Servo
		angleCur += dir * stepAngle;
		if (angleCur >= maxAngle) { angleCur = maxAngle; dir = -1; }
		else if (angleCur <= minAngle) { angleCur = minAngle; dir = +1; }
		scanner.write(angleCur);

		// Distance
		long d = measureDistanceCM();
		lastDistCM = d;

		// Alert state
		AlertNow = computeStableAlert(d);
		if (alertNow) setAlertIndicators();
		else setIdleIndicators();

		updLCD(alertNow);
		updBuzzScheduler(alertNow, d);
		sendData(angleCur, d);
}

// Buzzer Update 
	if (alertNow) {
		if ((int32_t)(now - tBuzzNext) >= 0) {
			if (buzzOn) {
				digitalWrite(sigB, HIGH);
				buzzOn = true;
				tBuzzNext = now + buzzOnMs;
			}
			else {
				digitalWrite(sigB, LOW);
				buzzOn = false;
				tBuzzNext = now + buzzOffMs;
			}
		}
	} else {	
		digitalWrite(sigB, LOW);
		buzzOn = false;
	}
}