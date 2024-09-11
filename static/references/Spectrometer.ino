#define clk PB0                          // 53 digtal pin
#define ROG PB1                          // 52 digital pin
#define SAMPLE_COUNT 2088                // Number of samples to read
volatile int sampleArray[SAMPLE_COUNT];  // Store every sample
char userInput;

// Sensor Initiation Process Start

void sensor_readout() {

  PORTB = 0B00000000;  // clk low ROG low*/

  PORTB = 0B00000011;  // ROG high and clock is high
  _delay_us(20);       // stay 20 uS fall/rise time
  PORTB = 0B00000010;  // clk low and ROG high
  _delay_us(20);       // stay 20 uS
  PORTB = 0B00000011;  // clk high ROG still high
  _delay_us(15);       // stay 15 uS
  PORTB = 0B00000001;  // ROG low Clk High
  _delay_us(25);       // stay 25 uS
  PORTB = 0B00000011;  // ROG high
  _delay_us(15);       // stay 15 uS
  PORTB = 0B00000010;  // clk low
  _delay_us(20);       // stay 20 uS

// Sensor Initiation Process End

// Sensor starts to capture data
 
  for (int x = 0; x <= 2088; x++) {
    //read sensor data
    PORTB = 0B00000011;  // clk high
    _delay_us(20);       // stay 20 uS
    PORTB = 0B00000010;  // clk low
    //_delay_loop_1(4);    // stay 250 nS
    _delay_us(7.8);  // stay 7.8 uS
    int pixel = analogRead(A9);
    sampleArray[x] = pixel;  //it takes 15 uS read and store the adc value in sample array acording to ths https://forum.arduino.cc/t/microcontroller-i-o-adc-benchmarks/315304/2#msg2257153
    _delay_us(3);            // stay 3 uS
  }

  PORTB = 0B00000000;  // clk low ROG low
  //delay(10);
}

void send_sample_array() {
  for (int i = 0; i < SAMPLE_COUNT; i++) {
    Serial.write((byte*)&sampleArray[i], sizeof(sampleArray[i]));
  }
  Serial.println();  // Add a newline character to indicate the end of the data
}

void setup() {
  DDRB = 0x03;  // 53, 52
  // set ADC prescale to 4 to speed it up
  ADCSRA = (ADCSRA & 0b11111000) | 0b011;  //0b010// Divide by 8 Prescaler for fast up the adc 8-0b011
  Serial.begin(230400);
}

void loop() {


  if (Serial.available() > 0) {

    userInput = Serial.read();  // read input from GUI

    // cheking to start reading data
    if (userInput == 'r') {

      // Read and save data to array

      for(int i = 0; i < 2; i++) {
         sensor_readout();
      }

      //send that data sending is going to start and hold on to read
      Serial.println("s");

      //sending all data to GUI
      for (int i = 0; i <= SAMPLE_COUNT; i++) {
        Serial.println(sampleArray[i]);
      }

      //send that data sending is over and stop reading
      Serial.println("f");
    }
  }
}
