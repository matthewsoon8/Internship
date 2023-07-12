#define STEP_PIN  10  //step
#define DIR_PIN   9   //direction
#define en_PIN   8    //direction
#define button_PIN  2 //Button Pin


const int sensorPin1 = A0; // 圧力センサ1のアナログ入力ピン   Index Finger
const int sensorPin2 = A1; // 圧力センサ2のアナログ入力ピン   Pinky
const int sensorPin3 = A2; // 圧力センサ3のアナログ入力ピン   Thumb
int vol_value1 = 0;
int vol_value2 = 0;
int vol_value3 = 0;

int data = 0;           
char userInput;

void moveMotor(){                 //This function moves the motor one step
   // digitalWrite(en_PIN, LOW);
    
    digitalWrite(STEP_PIN, HIGH);
    delay(1);
    digitalWrite(STEP_PIN, LOW);
    delay(1);
    
   // digitalWrite(en_PIN, HIGH);
}


void setup() {

  Serial.begin(9600); // シリアル通信の開始

  pinMode(DIR_PIN, OUTPUT);
  digitalWrite(DIR_PIN, LOW);
  
  pinMode(STEP_PIN, OUTPUT);
  digitalWrite(STEP_PIN, LOW);

  pinMode(en_PIN, OUTPUT);
  digitalWrite(en_PIN, HIGH);

  pinMode(button_PIN, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  
 
}

//float pinkyCoord[2] = {8, 1}  ;      //Pinky cooridnate is point of refferance
//float indexCoord[2] = {pinkyCoord[0], pinkyCoord[1] + 5.2};
//float thumbCoord[2] = {pinkyCoord[0] - 6.22, pinkyCoord[1] + 1.93};
float pinkyCoord[2] = {8, 1}  ;      //Pinky cooridnate is point of refferance
float indexCoord[2] = {pinkyCoord[0], 6.2};
float thumbCoord[2] = {1, 6.17};


float midPoint[2] = {  ((indexCoord[0] + pinkyCoord[0] + thumbCoord[0] ) / 3),((indexCoord[1] + pinkyCoord[1] + thumbCoord[1] ) / 3)} ;

float currentCOG[2] ={0,0};

float recalculated[2]={0,0};


int CurrentPosition=400;

int buttonState = 0;
int turnYes = 0 ;

void loop() {
  buttonState = digitalRead(button_PIN);
  if (buttonState ==HIGH){
    turnYes=1;
    digitalWrite(en_PIN, LOW);
  }

  
  //if(Serial.available()> 0){                  //If serial at all
    
    //userInput = Serial.read();               // read user input
      
     // if(userInput == 'g'){                  // if we get expected g value 

          double voltage1, voltage2, voltage3, resistance1, resistance2, resistance3, pressure1, pressure2, pressure3; // 変数の宣言
        
          static int previousValue1 = 0; // Last sensor value, reset previous value
          static int previousValue2 = 0; // 前回のセンサ値
          static int previousValue3 = 0; // 前回のセンサ値
        
          int vol_value1 = analogRead(sensorPin1); // Read analog value from pressure sensor 1 index
          int vol_value2 = analogRead(sensorPin2); // 圧力センサ2からのアナログ値の読み取り         Pinky
          int vol_value3 = analogRead(sensorPin3); // 圧力センサ3からのアナログ値の読み取り         Thumb
        
        
          int valueDifference1 = vol_value1 - previousValue1; // Calculate the difference from the previous value of sensor 1
          int valueDifference2 = vol_value2 - previousValue2; // センサ2の前回値との差を計算
          int valueDifference3 = vol_value3 - previousValue3; // センサ2の前回値との差を計算
        
          voltage1 = vol_value1 * 5 / 1023.0; // Calculation of output voltage from pressure sensor 1
          voltage2 = vol_value2 * 5 / 1023.0; // 圧力センサ2からの出力電圧の計算
          voltage3 = vol_value3 * 5 / 1023.0; // 圧力センサ3からの出力電圧の計算
          resistance1 = (5 - voltage1) / voltage1 * 1000.0;
          resistance2 = (5 - voltage2) / voltage2 * 1000.0;
          resistance3 = (5 - voltage3) / voltage3 * 1000.0;
          pressure1 = resistance1 / 1000.0; // Calculation of pressure value from pressure sensor 1
          pressure2 = resistance2 / 1000.0; // 圧力センサ2からの圧力値の計算
          pressure3 = resistance3 / 1000.0; // 圧力センサ3からの圧力値の計算

          if(pressure1<0.07){
            pressure1=0;
          }
          if(pressure2<0.07){
            pressure2=0;
          }
          if(pressure3<0.07){
            pressure3=0;
          }

          if(Serial.available()> 0){                  //If serial at all
    
            userInput = Serial.read();               // read user input
      
              if(userInput == 'g'){                  // if we get expected g value 
            
                Serial.print(pressure1); // Pressure value from pressure sensor 1
                Serial.print(",");
                Serial.print(pressure2); // 圧力センサ2からの圧力値
                Serial.print(",");
                Serial.println(pressure3); // 圧力センサ3からの圧力値
              }
          }


          
          if(  (pressure1 + pressure2 + pressure3)==0 ){
            pressure1=1;
            pressure2=1;
            pressure3=1;
          }

          

          currentCOG[0]=(indexCoord[0]*pressure1 + pinkyCoord[0]*pressure2 + thumbCoord[0]*pressure3 ) / (pressure1+pressure2+pressure3);     //X coordinate
          currentCOG[1]=(indexCoord[1]*pressure1 + pinkyCoord[1]*pressure2 + thumbCoord[1]*pressure3 ) / (pressure1+pressure2+pressure3);     //Y Coordinate
          
          recalculated[0] = currentCOG[0] - midPoint[0];      //COP XY coordinates centered on the true center
          recalculated[1] = currentCOG[1] - midPoint[1];
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


          //float xCentered = -1;
          //float yCentered = -1;
          float xCentered = recalculated[0];
          float yCentered = recalculated[1];

          float radius = (sqrt( sq(xCentered) + sq(yCentered)  ));
          
          if(xCentered ==0 && yCentered==0   ){
            yCentered=1;
          }
        
          
         // Serial.print(xCentered); // 圧力センサ2からの圧力値##########################
         // Serial.print(",");
          //Serial.println(yCentered); // 圧力センサ3からの圧力値

          float copAngle=0;
          
          if(xCentered>0){
              copAngle = (atan(yCentered/xCentered)) ;  
          }else{
              //copAngle = (atan(yCentered/xCentered));
              copAngle = (atan(yCentered/xCentered))+3.14;
          }

          
          if(copAngle<0){     //Angle not 0
              copAngle = (2*3.14)+copAngle;
          }
          
          float copAngleDegrees = copAngle *  (180/3.14);

          if(copAngleDegrees > 180){
            copAngleDegrees=copAngleDegrees-180;
          }

          
          //Serial.print("COP degrees: "); /////////////////////######################
          //Serial.print(copAngleDegrees);
          int CurrentPositionDegrees = map(CurrentPosition, 0, 1600, 0, 360);
          //Serial.print(", Cuurent Angle: ");
          //Serial.println(CurrentPositionDegrees);
          
          int threshold=10;
          float travelAngle = abs(copAngleDegrees-CurrentPositionDegrees);
          float travelSteps = map(travelAngle,0,360,0,1600);
          //copStepPosition = map(copAngleDegrees);
          
          if(travelSteps>100){
            travelSteps=75;
          }
          

          if(radius >1){
            if( copAngleDegrees < (CurrentPositionDegrees-threshold) ){             //Correcting for offcenter COP
                //Serial.println("Turning Counter clockwise");
                digitalWrite(DIR_PIN,LOW );
                for(int i=0;i < travelSteps  ;  i++){
                     moveMotor();
                     CurrentPosition=CurrentPosition-1;
                }
                
              }else if(copAngleDegrees > (CurrentPositionDegrees+threshold) ){
                //Serial.println("Turning clockwise");
                digitalWrite(DIR_PIN,HIGH );
                for(int i=0;i < travelSteps  ;  i++){
                     moveMotor();
                     CurrentPosition = CurrentPosition+1;
                }
            }else{
              //Serial.println("Centered");
            }
          }
          /*                                                        //#########################
          Serial.print("TOP has rotated to ");        
          Serial.print(CurrentPosition);
          Serial.print(" of angle ");
          Serial.println(map(CurrentPosition,0,1600,0,360)  );
          */
          //DIR_PIN LOW is Clockwise

          //DIR_PIN HIGH is Counter Clockwise
          
          



///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
          //Serial.print(recalculated[0]); // 圧力センサ2からの圧力値
          //Serial.print(",");
          //Serial.println(recalculated[1]); // 圧力センサ3からの圧力値

          previousValue1 = vol_value1; // Save the current value of sensor 1
          previousValue2 = vol_value2; // センサ2の現在値を保存
          previousValue3 = vol_value3; // センサ3の現在値を保存  
    //} // if user input 'g' 
  //} // Serial.available
} // Void Loop
