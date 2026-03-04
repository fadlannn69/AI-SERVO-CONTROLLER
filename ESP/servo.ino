#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <Firebase_ESP_Client.h>
#include <addons/TokenHelper.h>
#include <addons/RTDBHelper.h>
#include "secrets.h"
#include <Servo.h>


// FIREBASE
FirebaseData fbdo;
FirebaseAuth auth;    
FirebaseConfig config;



// SERVO
Servo myservo;


void setup() {
    Serial.begin(115200);


    // ===== SERVO =====
    myservo.attach(D5);

    // ===== WIFI =====
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(300);
    }
    Serial.println("\nWiFi connected");

    // ===== FIREBASE =====
    //   auth.user.email = ""; // LOGIN FIRESTORE {OPTIONAL}
    //   auth.user.password = " ";


    config.api_key = " "; // ISI DENGAN API KEY
    config.database_url = " "; // ISI DENGAN DB URL

    Firebase.begin(&config, &auth);    
    Firebase.reconnectNetwork(true);

    Serial.println("Menunggu Firebase ready...");
    while (!Firebase.ready()) {
        Serial.print(".");
        delay(300);
    }
    Serial.println("\nFirebase siap!");
}

void loop() {
    // ===== SERVO =====
    if (Firebase.RTDB.getInt(&fbdo, "/servo/angle")) {
        int angle = fbdo.intData();
        angle = constrain(angle, 0, 180);
        myservo.write(angle);
        Serial.print("Sudut diterima: ");
        Serial.println(angle);
    } else {
        Serial.println("Gagal membaca servo:");
        Serial.println(fbdo.errorReason());
    }
}