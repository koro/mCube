// this only works on atmels with the 16bit timer such as the ATmega328

int signal = 400;
int times[] = {signal, 1100, signal, 1100, signal, 700, signal, 1100, signal, 700, signal, 700, signal, 700, signal, 700, signal, 11168};
int timeslen = 18;
int timecounter = 0;

void setTimes(int roll, int pitch, int yaw, int thrust)
{
  // pitch  (1): 0 -> forwards, 255 -> backwards
  // roll   (2): 0 -> right,    255 -> left
  // thrust (3): 0 -> down,     255 -> up
  // yaw    (4): 0 -> right,    255 -> left
  int low = 700;
  int high = 1500;
  int length = 22000;
  times[1] = map(pitch, 0, 255, low, high);
  times[3] = map(roll, 0, 255, low, high);
  times[5] = map(thrust, 0, 255, low, high);
  times[7] = map(yaw, 0, 255, low, high);
  int sum = 0;
  for(int i=0; i < timeslen-1; i++)
    sum += times[i];
  times[timeslen-1] = length-sum;
}

void setup() 
{
  // set pin 9 (OC1A) to output
  pinMode(9, OUTPUT);
  // 16bit timer1
  noInterrupts();
  // clear timer registers  
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;
  TIMSK1 = 0;
  // toggle OC1A on compare match
  TCCR1A |= (1 << COM1A0);
  // set mode to CTC with compare to OCR1A 
  TCCR1B |= (1 << WGM12);
  // set /8 prescale
  TCCR1B |= (1 << CS11);
  // enable ouptu compare A interrupts 
  TIMSK1 |= (1 << OCIE1A);
  // set compare match register
  OCR1A = 2000;
  interrupts();
  
  Serial.begin(115200);
}

ISR(TIMER1_COMPA_vect)        // interrupt service routine
{
  OCR1A = times[timecounter]*2;
  timecounter++;
  if(timecounter >= timeslen)
    timecounter = 0;
}

void loop() 
{
  if(Serial.available())
  {
    int roll = Serial.parseInt();
    int pitch = Serial.parseInt();
    int yaw = Serial.parseInt();
    int thrust = Serial.parseInt();
    if (Serial.read() == '\n')
    {
      setTimes(roll, pitch, yaw, thrust);
    }
  }     
}
