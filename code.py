using namespace std;

volatile int pulseCountA = 0;
volatile int pulseCountB = 0;

float flowRateA = 0.0;
float flowRateB = 0.0;

const int sensorPinA = 2;
const int sensorPinB = 3;
const int ledPin = 13;

float calibrationFactor = 7.5; // for YF-S201
float pipeLength = 115.0; // in cm (change as needed)

unsigned long oldTime = 0;

void pulseCounterA() {
    pulseCountA++;
}

void pulseCounterB() {
    pulseCountB++;
}

void setup() {
    Serial.begin(9600);

    pinMode(sensorPinA, INPUT);
    pinMode(sensorPinB, INPUT);
    pinMode(ledPin, OUTPUT);

    attachInterrupt(digitalPinToInterrupt(sensorPinA), pulseCounterA, FALLING);
    attachInterrupt(digitalPinToInterrupt(sensorPinB), pulseCounterB, FALLING);
}

void loop() {
    if ((millis() - oldTime) > 1000) { // every 1 second
        
        detachInterrupt(digitalPinToInterrupt(sensorPinA));
        detachInterrupt(digitalPinToInterrupt(sensorPinB));

        // Calculate flow rate (L/min)
        flowRateA = ((1000.0 / (millis() - oldTime)) * pulseCountA) / calibrationFactor;
        flowRateB = ((1000.0 / (millis() - oldTime)) * pulseCountB) / calibrationFactor;

        oldTime = millis();

        Serial.print("Flow A: ");
        Serial.print(flowRateA);
        Serial.print(" L/min | Flow B: ");
        Serial.print(flowRateB);
        Serial.println(" L/min");

        float diff = flowRateA - flowRateB;

        if (diff > 0.5) { // threshold
            digitalWrite(ledPin, HIGH);

            float leakPosition = (flowRateB / flowRateA) * pipeLength;

            Serial.print("LEAK DETECTED at distance: ");
            Serial.print(leakPosition);
            Serial.println(" cm from start");

        } else {
            digitalWrite(ledPin, LOW);
            Serial.println("No Leak");
        }

        pulseCountA = 0;
        pulseCountB = 0;

        attachInterrupt(digitalPinToInterrupt(sensorPinA), pulseCounterA, FALLING);
        attachInterrupt(digitalPinToInterrupt(sensorPinB), pulseCounterB, FALLING);
    }
}