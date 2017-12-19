#include <LiquidCrystal.h>

/* lcd shield tanımları */
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

/* Renk sensörü ile meyvelerin rengini algılayarak meyvenin sağlam, çürük yada farklı bir meyve olduğunu algılama */
int saglam = 0;
int saglam_olmayan = 0;
String a = "";

int LEDpin1 = 49;
int LEDpin2 = 50;
/* tanımlamalar */
/* Mesafe icin kullanilan tanimlar */
int trigPin = 33;
int echoPin = 31;
long sure;
long uzaklik;

/*icin kullanilan tanimlar */
int S0 = 40;
int S1 = 41;
int S2 = 43;
int S3 = 42;
int OUT = 44;
int LED = 45;


/* -- Uygulama icin kullanacagimiz renkyuzdeleri tanimlaniyor ---*/
int i = 0;
int RenkYuzdesi[7][3] = { {38, 31, 37}, // Sarı renk
  {13, 65, 26}, // Mavi renk
  {29, 36, 29}, // Beyaz renk
  {64, 31, 22}, // Kırmızı renk
  {64, 31, 22}, // Kırmızı renk
  {23, 34, 45},

  {64, 31, 22}
};

String Renkler[7] = {"Sari", "Mavi", "Beyaz", "portakal", "armut", "yesilelma", "yesil"};

/* Sensör hassasiyeti */
int aralik = 7;

/* Renk frekanslarının tutulduğu değişkenler */
int KirmiziYuzdesi, YesilYuzdesi, MaviYuzdesi;



void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT); /* trig pini çıkış olarak ayarlandı */
  pinMode(echoPin, INPUT); /* echo pini giriş olarak ayarlandı */

  /* RGB setup */
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(OUT, INPUT);
  pinMode(LED, OUTPUT);

  pinMode(LEDpin1, OUTPUT);
  pinMode(LEDpin2, OUTPUT);

  /* Lcd setup */
  lcd.begin(16, 2);

}

void loop() {
  for (i = 0; i < 1; i++) {
    digitalWrite(trigPin, LOW); /* sensör pasif hale getirildi */
    delayMicroseconds(1000);
    digitalWrite(trigPin, HIGH); /* Sensore ses dalgasının üretmesi için emir verildi */
    delayMicroseconds(4000);
    digitalWrite(trigPin, LOW);  /* Yeni dalgaların üretilmemesi için trig pini LOW konumuna getirildi */
    sure = pulseIn(echoPin, HIGH); /* ses dalgasının geri dönmesi için geçen sure ölçülüyor */
    uzaklik = sure / 29.1 / 2; /* ölçülen sure uzaklığa çevriliyor */
    //Serial.print(uzaklik);
    if ( uzaklik <= 15 ) {
      renkayari();
      //delay(3000);
    }
    else {
      lcd.setCursor(0, 0);
      lcd.print("Mesafe Fazla !!!");
      delay(1000);
      lcd.clear();
    }
  }
}
void TCS3200_Ac() {
  digitalWrite(LED, HIGH); // switch LED on
  digitalWrite(S0, HIGH); // output frequency scaling (100%)
  digitalWrite(S1, HIGH);
  delay(5);
}

void TCS3200_Kapat() {
  digitalWrite(LED, LOW); // switch LED off
  digitalWrite(S0, LOW); // power off sensor
  digitalWrite(S1, LOW);
}

void Filtresiz() {
  digitalWrite(S2, HIGH); // select no filter
  digitalWrite(S3, LOW);
  delay(5);
}

void KirmiziFiltre() {
  digitalWrite(S2, LOW); // select red filter
  digitalWrite(S3, LOW);
  delay(5);
}

void YesilFiltre() {
  digitalWrite(S2, HIGH); // select green filter
  digitalWrite(S3, HIGH);
  delay(5);
}

void MaviFiltre() {
  digitalWrite(S2, LOW); // select blue filter
  digitalWrite(S3, HIGH);
  delay(5);
}

void renkayari() {
  /* Renk Ayarlarinin yapilacagi fonk. */
  float BeyazFrekansi, KirmiziFrekansi, YesilFrekansi, MaviFrekansi;
  TCS3200_Ac();
  Filtresiz();
  BeyazFrekansi = float(pulseIn(OUT, LOW, 40000));
  KirmiziFiltre();
  KirmiziFrekansi = float(pulseIn(OUT, LOW, 40000));
  YesilFiltre();
  YesilFrekansi = float(pulseIn(OUT, LOW, 40000));
  MaviFiltre();
  MaviFrekansi = float(pulseIn(OUT, LOW, 40000));
  TCS3200_Kapat();
  KirmiziYuzdesi = int((BeyazFrekansi / KirmiziFrekansi) * 100.0);
  YesilYuzdesi = int((BeyazFrekansi / YesilFrekansi) * 100.0);
  MaviYuzdesi = int((BeyazFrekansi / MaviFrekansi) * 100.0);

  RengiBul();





}

void RengiBul() {


  if (Serial.available() > 0) {
    char serialListener = Serial.read();
    if (serialListener == '1') {   // Portakal secildiginde oygulanacak olan kisim
      while (true) {
        for (int renk = 0; renk < 5; renk ++) {
          if (KirmiziYuzdesi > RenkYuzdesi[renk][0] - 7 && KirmiziYuzdesi < RenkYuzdesi[renk][0] + 7 &&
              MaviYuzdesi > RenkYuzdesi[renk][1] - 7 && MaviYuzdesi < RenkYuzdesi[renk][1] + 7 &&
              YesilYuzdesi > RenkYuzdesi[renk][2] - 7 && YesilYuzdesi < RenkYuzdesi[renk][2] + 7 ) {
            if ((Renkler[renk]) == "portakal" ) {
              digitalWrite(LEDpin1, HIGH);
              saglam ++;

              yaziKontrol("portakal", saglam);
              delay(1000);


            }
            else {
              digitalWrite(LEDpin1, LOW);
              saglam_olmayan ++;
              delay(1000);

            }
          }
        }
        bittiMi_kontrol(saglam, saglam_olmayan);

        renkayari();
      }
    }
    else if (serialListener == '2') {   // yesil elma secildiginde oygulanacak olan kisim
      while (true) {
        for (int renk = 0; renk < 6; renk ++) {
          if (KirmiziYuzdesi > RenkYuzdesi[renk][0] - 7 && KirmiziYuzdesi < RenkYuzdesi[renk][0] + 7 &&
              MaviYuzdesi > RenkYuzdesi[renk][1] - 7 && MaviYuzdesi < RenkYuzdesi[renk][1] + 7 &&
              YesilYuzdesi > RenkYuzdesi[renk][2] - 7 && YesilYuzdesi < RenkYuzdesi[renk][2] + 7 ) {
            if ((Renkler[renk]) == "yesilelma" ) {
              digitalWrite(LEDpin1, HIGH);
              saglam ++;
              yaziKontrol("yesil Elma", saglam);
              delay(1000);
            }
            else {
              digitalWrite(LEDpin1, LOW);
              saglam_olmayan ++;
              delay(1000);

            }
          }
        }

        bittiMi_kontrol(saglam, saglam_olmayan);

        renkayari();
      }
    }

    else if (serialListener == '3') {   // kirmizi elma secildiginde oygulanacak olan kisim
      int okunduMu = 0;
      while (true) {
        for (int renk = 0; renk < 5; renk ++) {
          if (KirmiziYuzdesi > RenkYuzdesi[renk][0] - 7 && KirmiziYuzdesi < RenkYuzdesi[renk][0] + 7 &&
              MaviYuzdesi > RenkYuzdesi[renk][1] - 7 && MaviYuzdesi < RenkYuzdesi[renk][1] + 7 &&
              YesilYuzdesi > RenkYuzdesi[renk][2] - 7 && YesilYuzdesi < RenkYuzdesi[renk][2] + 7 ) {
            if ((Renkler[renk]) == "kirmizielma" ) {
              digitalWrite(LEDpin1, HIGH);
              saglam ++;
              yaziKontrol("Kirmizi Elma", saglam);
              delay(1000);


            }
            else {
              digitalWrite(LEDpin1, LOW);
              saglam_olmayan ++;
              delay(1000);
            }
          }

        }

        bittiMi_kontrol(saglam, saglam_olmayan);

        renkayari();
      }
    }
    else if (serialListener == '4') {   // mandalina secildiginde oygulanacak olan kisim

      while (true) {
        for (int renk = 0; renk < 5; renk ++) {
          if (KirmiziYuzdesi > RenkYuzdesi[renk][0] - 7 && KirmiziYuzdesi < RenkYuzdesi[renk][0] + 7 &&
              MaviYuzdesi > RenkYuzdesi[renk][1] - 7 && MaviYuzdesi < RenkYuzdesi[renk][1] + 7 &&
              YesilYuzdesi > RenkYuzdesi[renk][2] - 7 && YesilYuzdesi < RenkYuzdesi[renk][2] + 7 ) {
            if ((Renkler[renk]) == "mandalina" ) {
              digitalWrite(LEDpin1, HIGH);
              saglam ++;
              yaziKontrol("mandalina", saglam);
              delay(1000);


            }
            else {
              digitalWrite(LEDpin1, LOW);
              saglam_olmayan ++;
              delay(1000);
            }
          }

        }

        bittiMi_kontrol(saglam, saglam_olmayan);

        renkayari();
      }
    }
    else if (serialListener == '5') {   // armut secildiginde oygulanacak olan kisim

      while (true) {
        for (int renk = 0; renk < 5; renk ++) {
          if (KirmiziYuzdesi > RenkYuzdesi[renk][0] - 7 && KirmiziYuzdesi < RenkYuzdesi[renk][0] + 7 &&
              MaviYuzdesi > RenkYuzdesi[renk][1] - 7 && MaviYuzdesi < RenkYuzdesi[renk][1] + 7 &&
              YesilYuzdesi > RenkYuzdesi[renk][2] - 7 && YesilYuzdesi < RenkYuzdesi[renk][2] + 7 ) {
            if ((Renkler[renk]) == "armut" ) {
              digitalWrite(LEDpin1, HIGH);
              saglam ++;
              yaziKontrol("Armut", saglam);
              delay(1000);


            }
            else {
              digitalWrite(LEDpin1, LOW);
              saglam_olmayan ++;
              delay(1000);
            }
          }
        }
        bittiMi_kontrol(saglam, saglam_olmayan);

        renkayari();

      }
    }
    else if (serialListener == '6') {   // muz secildiginde oygulanacak olan kisim

      while (true) {
        for (int renk = 0; renk < 5; renk ++) {
          if (KirmiziYuzdesi > RenkYuzdesi[renk][0] - 7 && KirmiziYuzdesi < RenkYuzdesi[renk][0] + 7 &&
              MaviYuzdesi > RenkYuzdesi[renk][1] - 7 && MaviYuzdesi < RenkYuzdesi[renk][1] + 7 &&
              YesilYuzdesi > RenkYuzdesi[renk][2] - 7 && YesilYuzdesi < RenkYuzdesi[renk][2] + 7 ) {
            if ((Renkler[renk]) == "muz" ) {
              digitalWrite(LEDpin1, HIGH);
              saglam ++;
              yaziKontrol("Muz", saglam);
              delay(1000);


            }
            else {
              digitalWrite(LEDpin1, LOW);
              saglam_olmayan ++;
              delay(1000);
            }
          }

          bittiMi_kontrol(saglam, saglam_olmayan);

          renkayari();
        }
      }

    }
  }
}

void bittiMi_kontrol(int saglam, int saglam_olmayan) {
  String b;
  String c;

  if (Serial.available() > 0) {
    char serialListener = Serial.read();
    if (serialListener == 'P') {
      digitalWrite(LEDpin2, HIGH);
      b = saglam;
      c = saglam_olmayan;
      a = b + ";" + c;
      Serial.println(a);
      delay(100);
      //Serial.println(saglam_olmayan);
      yaziKontrolBitir(a);
      //delay(1000);
      //Serial.println(saglam_olmayan);
    }
    else if (serialListener == 'Y') {
      digitalWrite(LEDpin2, HIGH);
      b = saglam;
      c = saglam_olmayan;
      a = b + ";" + c;
      Serial.println(a);
      delay(100);
      //Serial.println(saglam_olmayan);
      yaziKontrolBitir(a);
      //delay(1000);
      //Serial.println(saglam_olmayan);
    }
    else if (serialListener == 'K') {
      digitalWrite(LEDpin2, HIGH);
      b = saglam;
      c = saglam_olmayan;
      a = b + ";" + c;
      Serial.println(a);
      delay(100);
      //Serial.println(saglam_olmayan);
      yaziKontrolBitir(a);

    }
    else if (serialListener == 'M') {
      digitalWrite(LEDpin2, HIGH);
      b = saglam;
      c = saglam_olmayan;
      a = b + ";" + c;
      Serial.println(a);
      delay(100);
      //Serial.println(saglam_olmayan);
      yaziKontrolBitir(a);
      //delay(1000);
      //Serial.println(saglam_olmayan);
    }
    else if (serialListener == 'U') {
      digitalWrite(LEDpin2, HIGH);
      b = saglam;
      c = saglam_olmayan;
      a = b + ";" + c;
      Serial.println(a);
      delay(100);
      //Serial.println(saglam_olmayan);
      yaziKontrolBitir(a);
      //delay(1000);
      //Serial.println(saglam_olmayan);
    }
    else if (serialListener == 'R') {
      digitalWrite(LEDpin2, HIGH);
      b = saglam;
      c = saglam_olmayan;
      a = b + ";" + c;
      Serial.println(a);
      delay(100);
      //Serial.println(saglam_olmayan);
      yaziKontrolBitir(a);
      //delay(1000);
      //Serial.println(saglam_olmayan);


    }

  }


}



void yaziKontrol(String gelenYazi, int sayac ) {
  lcd.setCursor(0, 0);
  lcd.print("MeyveKontrolu");
  delay(1000);
  lcd.clear(); // Clears the display
  lcd.setCursor(14, 1);
  lcd.print(sayac);
  delay(1000);
  lcd.clear(); // Clears the display
  lcd.setCursor(0, 1);
  lcd.print(gelenYazi);
  delay(1000);
  lcd.clear();
}

void yaziKontrolBitir(String sayac ) {

  lcd.setCursor(0, 0);
  lcd.print("Uygulama bitti!");
  lcd.setCursor(0, 1);
  lcd.print(sayac);
  //lcd.setCursor(9, 1);
  //lcd.print(sayac2);
}




