/* 
 * GRO 302 - Conception d'un robot mobile
 * Code de démarrage Template
 * Auteurs: Etienne Gendron     
 * date: Juin 2022
*/

/*------------------------------ Librairies ---------------------------------*/
#include <ArduinoJson.h> // librairie de syntaxe JSON
#include <SPI.h> // librairie Communication SPI
#include <LibS3GRO.h>

/*------------------------------ Constantes ---------------------------------*/

#define BAUD            115200      // Frequence de transmission serielle
#define UPDATE_PERIODE  100         // Periode (ms) d'envoie d'etat general


/*---------------------------- variables globales ---------------------------*/

IMU9DOF imu_;                       // objet imu

volatile bool shouldSend_ = false;  // drapeau prêt à envoyer un message
volatile bool shouldRead_ = false;  // drapeau prêt à lire un message

SoftTimer timerSendMsg_;            // chronometre d'envoie de messages
SoftTimer timerPulse_;              // chronometre pour la duree d'un pulse

uint16_t pulseTime_ = 0;            // temps dun pulse en ms
float PWM_des_ = 0;                 // PWM desire pour les moteurs
float left_command_ = 0;            // commande pour la roue gauche
float right_command_ = 0;           // commande pour la roue droite


float Axyz[3];                      // tableau pour accelerometre
float Gxyz[3];                      // tableau pour giroscope
float Mxyz[3];                      // tableau pour magnetometre

/*------------------------- Prototypes de fonctions -------------------------*/

void timerCallback();
void sendMsg(); 
void readMsg();
void serialEvent();

/*---------------------------- fonctions "Main" -----------------------------*/

void setup() {
  Serial.begin(BAUD);               // initialisation de la communication serielle
  imu_.init();                      // initialisation de la centrale inertielle
  
  // Chronometre envoie message
  timerSendMsg_.setDelay(UPDATE_PERIODE);
  timerSendMsg_.setCallback(timerCallback);
  timerSendMsg_.enable();
}
  
/* Boucle principale (infinie)*/
void loop() {

  if(shouldRead_){
    readMsg();
  }
  if(shouldSend_){
    sendMsg();
  }
  

  // mise a jour des chronometres
  timerSendMsg_.update();
  timerPulse_.update();
}

/*---------------------------Definition de fonctions ------------------------*/

void serialEvent(){shouldRead_ = true;}

void timerCallback(){shouldSend_ = true;}

void sendMsg(){
  /* Envoit du message Json sur le port seriel */
  StaticJsonDocument<500> doc;
  // Elements du message

  // doc["time"] = millis();
  // doc["PWM_des"] = PWM_des_;
  // doc["accelX"] = imu_.getAccelX();
  // doc["accelY"] = imu_.getAccelY();
  // doc["accelZ"] = imu_.getAccelZ();
  // doc["gyroX"] = imu_.getGyroX();
  // doc["gyroY"] = imu_.getGyroY();
  // doc["gyroZ"] = imu_.getGyroZ();
  doc["right"] = right_command_;
  doc["left"] = left_command_;

  // Serialisation
  serializeJson(doc, Serial);
  // Envoit
  Serial.println();
  shouldSend_ = false;
}

void readMsg(){
  // Lecture du message Json
  StaticJsonDocument<500> doc;
  JsonVariant parse_msg;

  // Lecture sur le port Seriel
  DeserializationError error = deserializeJson(doc, Serial);
  shouldRead_ = false;

  // Si erreur dans le message
  if (error) {
    Serial.print("deserialize() failed: ");
    Serial.println(error.c_str());
    return;
  }
  
  // Analyse des éléments du message message
  parse_msg = doc["left"];
  if(!parse_msg.isNull()){
     left_command_ = doc["left"].as<float>();
  }

  parse_msg = doc["right"];
  if(!parse_msg.isNull()){
     right_command_ = doc["right"].as<float>();
  }
}