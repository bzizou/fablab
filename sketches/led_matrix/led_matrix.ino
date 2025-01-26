#include "MD_Parola.h"
#include "MD_MAX72xx.h"
#include "SPI.h"
#include <WiFi.h>
#include <WebServer.h>
#include <uri/UriBraces.h>

/*Put your SSID & Password*/
const char* ssid = "Bbox-37BFA846";  // Enter SSID here
const char* password = "hh6CTA51Jnb2JGwmJX";  //Enter Password here

WebServer server(80);

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
//define HARDWARE_TYPE MD_MAX72XX::GENERIC_HW
#define MAX_DEVICES 16
#define CS_PIN 15
#define CLK_PIN 14
#define DATA_PIN 2

MD_Parola myDisplay = MD_Parola(HARDWARE_TYPE, DATA_PIN, CLK_PIN, CS_PIN, MAX_DEVICES);
String string_text="ESP32";
int Speed=100;
int Brightness=0;
int Mode=1;

String urlDecode(String encoded) {
    char decoded[encoded.length() * 2]; // Tableau pour stocker la chaîne décodée
    int decodedIndex = 0; // Index pour le tableau décodé
    
    for (int i = 0; i < encoded.length(); i++) {
        if (encoded[i] == '+') { // Si on trouve un '+', remplace par ' '
            decoded[decodedIndex++] = ' ';
        } else if (encoded[i] == '%') { // Si on trouve un '%', il faut décoder les 2 prochains caractères
            if (i + 2 < encoded.length()) {
                // Convertit les 2 caractères hexa en valeur numérique
                char high = encoded[i+1];
                char low = encoded[i+2];
                int value = (high >= 'A' ? high - 'A' + 0xA : high - '0') << 4;
                value += (low >= 'A' ? low - 'A' + 0xA : low - '0');
                
                // Ajoute le caractère correspondant à la valeur ASCII
                decoded[decodedIndex++] = (char)value;
                
                i += 2; // Passe les 2 prochains caractères déjà traités
            }
        } else {
            // Si aucun cas particulier, ajoute le caractère tel quel
            decoded[decodedIndex++] = encoded[i];
        }
    }
    
    // Termine la chaîne avec un caractère nul et retourne la chaîne
    decoded[decodedIndex] = '\0';
    return String(decoded);
}

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Bzizou Led Matrix</title>
    <style>
        body {
            background-color: #000;
            color: #0f0;
            font-family: 'Courier New', Courier, monospace;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
        }
        form {
            background-color: #000;
            color: #0f0;
            display: inline-block;
            margin-top: 20px;
        }
        input[type="text"] {
            background-color: #000;
            color: #0f0;
            width: 300px;
            border: 2px solid #0f0;
            font-family: 'Courier New', Courier, monospace;
            padding: 10px 20px;
            font-size: 16px;
        }
        button {
            background-color: #000;
            color: #0f0;
            padding: 10px 20px;
            border: 2px solid #0f0;
            font-family: 'Courier New', Courier, monospace;
            font-size: 16px;
            cursor: pointer;
        }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <h1>Bzizou Led Matrix</h1>
    <div id="result"></div>
    <br>
    Text:
    <form id="matrixForm">
        <input type="text" id="textInput" name="text" placeholder="Entrez votre texte (max 40 caractères)" maxlength="40">
        <button type="submit">Envoyer</button>
    </form>
    <br>
    Speed:
    <form id="speedForm">
        <input type="text" id="textSpeed" name="speed" placeholder="100" maxlength="3">
        <button type="submit">Envoyer</button>
    </form>
    <br>
    Brightness:
    <form id="brightnessForm">
        <input type="text" id="textBrightness" name="brightness" placeholder="0" maxlength="2">
        <button type="submit">Envoyer</button>
    </form>
    Mode:
    <form id="modeForm">
        <input type="text" id="textMode" name="mode" placeholder="0" maxlength="2">
        <button type="submit">Envoyer</button>
    </form>

    <script>
        document.getElementById('matrixForm').addEventListener('submit', function(e) {
            e.preventDefault();
            // Récupération du texte
            const text = document.getElementById('textInput').value;
            // Validation de la longueur
            if (text.length > 40 || text.trim() === '') {
                alert("Veuillez entrer un texte entre 1 et 40 caractères");
                return;
            }
            // Construction de l'URL
            const url = `/text/${encodeURIComponent(text)}`;
            // Appel GET à l'API
            fetch(url, {
                method: 'GET'
            })
            .then(response => {
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Erreur serveur');
                }
            })
            .then(data => {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `<strong>Réponse de l'API:</strong> ${data}`;
                
                // Masquer le résultat après 3 secondes
                setTimeout(() => {
                    resultDiv.innerHTML = '';
                }, 3000);
            })
            .catch(error => {
                alert("Erreur lors de la communication avec l'API: " + error.message);
            });
        });
        
        document.getElementById('speedForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const speed = document.getElementById('textSpeed').value;
            const url = `/speed/${speed}`;
            fetch(url, {
                method: 'GET'
            })
            .then(response => {
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Erreur serveur');
                }
            })
            .then(data => {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `<strong>Réponse de l'API:</strong> ${data}`;
                setTimeout(() => {
                    resultDiv.innerHTML = '';
                }, 3000);
            })
            .catch(error => {
                alert("Erreur lors de la communication avec l'API: " + error.message);
            });
        });

        document.getElementById('brightnessForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const brightness = document.getElementById('textBrightness').value;
            const url = `/brightness/${brightness}`;
            fetch(url, {
                method: 'GET'
            })
            .then(response => {
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Erreur serveur');
                }
            })
            .then(data => {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `<strong>Réponse de l'API:</strong> ${data}`;
                setTimeout(() => {
                    resultDiv.innerHTML = '';
                }, 3000);
            })
            .catch(error => {
                alert("Erreur lors de la communication avec l'API: " + error.message);
            });
        });


        document.getElementById('modeForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const mode = document.getElementById('textMode').value;
            const url = `/mode/${mode}`;
            fetch(url, {
                method: 'GET'
            })
            .then(response => {
                if (response.ok) {
                    return response.text();
                } else {
                    throw new Error('Erreur serveur');
                }
            })
            .then(data => {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `<strong>Réponse de l'API:</strong> ${data}`;
                setTimeout(() => {
                    resultDiv.innerHTML = '';
                }, 3000);
            })
            .catch(error => {
                alert("Erreur lors de la communication avec l'API: " + error.message);
            });
        });
        // Initialisation du focus sur le champ de saisie
        document.getElementById('textInput').focus();
    </script>
</body>
</html>
)rawliteral";

void setup() {

  Serial.begin(115200);
   
  // Intialize the object
  myDisplay.begin();

  // Set the intensity (brightness) of the display (0-15)
  myDisplay.setIntensity(0);

  // Clear the display
  myDisplay.displayClear();

  // Display a test
  string_text="                                                               ";
  myDisplay.setTextAlignment(PA_CENTER);
  myDisplay.setInvert(true);
  myDisplay.print(string_text.c_str());
  delay(1500);
  myDisplay.setInvert(false);
  myDisplay.displayClear();

  // Connecting...
  string_text="Connecting...";
  myDisplay.setTextAlignment(PA_LEFT);
  myDisplay.print(string_text.c_str());
 
  Serial.println("Connecting to ");
  Serial.println(ssid);

  //connect to your local wi-fi network
  WiFi.begin(ssid, password);
  delay(500);
  myDisplay.setTextAlignment(PA_RIGHT);
  myDisplay.print(string_text.c_str());
  delay(1000);

  //check wi-fi is connected to wi-fi network
  while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");  Serial.println(WiFi.localIP());

  // Home page
  server.on(F("/"), []() {
    server.send(200, "text/html", index_html);
  });

  // Text
  server.on(UriBraces("/text/{}"), []() {
    string_text = urlDecode(server.pathArg(0).c_str());
    server.send(200, "text/plain", "Text: '" + string_text + "'");
  });

  // Speed
  server.on(UriBraces("/speed/{}"), []() {
    Speed = server.pathArg(0).toInt();
    server.send(200, "text/plain", "Speed: "+ server.pathArg(0));
  });
  
  // Brightness
  server.on(UriBraces("/brightness/{}"), []() {
    Brightness = server.pathArg(0).toInt();
    if (Brightness>10) { Brightness = 10; }
    server.send(200, "text/plain", "Brightness: "+ server.pathArg(0));
  });

  // Mode
  server.on(UriBraces("/mode/{}"), []() {
    Mode = server.pathArg(0).toInt();
    server.send(200, "text/plain", "Mode: "+ server.pathArg(0));
  });

  server.begin();
  Serial.println("HTTP server started");

  myDisplay.displayClear();
  myDisplay.displayReset();
  string_text=WiFi.localIP().toString();
  
}

void loop() {
  server.handleClient();
  myDisplay.setIntensity(Brightness);
  myDisplay.setSpeed(Speed);
  if (myDisplay.displayAnimate()) {
    myDisplay.setIntensity(Brightness);
    myDisplay.displayReset();
    const char *text = string_text.c_str();
    switch (Mode) {
      case 0:
        myDisplay.setTextAlignment(PA_CENTER);
        myDisplay.print(text);
        break;
      case 1:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCROLL_LEFT, Speed);
        break;
      case 2:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCROLL_RIGHT, Speed);
        break;
      case 3:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCROLL_UP, Speed);
        break;
      case 4:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCROLL_DOWN, Speed);
        break;
      case 5:
        myDisplay.displayScroll(text, PA_CENTER, PA_FADE, Speed);
        break;
      case 6:
        myDisplay.displayScroll(text, PA_CENTER, PA_SLICE, Speed);
        break;
      case 7:
        myDisplay.displayScroll(text, PA_CENTER, PA_MESH, Speed);
        break;
      case 8:
        myDisplay.displayScroll(text, PA_CENTER, PA_DISSOLVE, Speed);
        break;
      case 9:
        myDisplay.displayScroll(text, PA_CENTER, PA_BLINDS, Speed);
        break;
      case 10:
        myDisplay.displayScroll(text, PA_CENTER, PA_RANDOM, Speed);
        break;
      case 11:
        myDisplay.displayScroll(text, PA_CENTER, PA_WIPE, Speed);
        break;
      case 12:
        myDisplay.displayScroll(text, PA_CENTER, PA_WIPE_CURSOR, Speed);
        break;
      case 13:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCAN_HORIZ, Speed);
        break;
      case 14:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCAN_HORIZX, Speed);
        break;
      case 15:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCAN_VERT, Speed);
        break;
      case 16:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCAN_VERTX, Speed);
        break;
      case 17:
        myDisplay.displayScroll(text, PA_CENTER, PA_OPENING, Speed);
        break;
      case 18:
        myDisplay.displayScroll(text, PA_CENTER, PA_OPENING_CURSOR, Speed);
        break;
      case 19:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCROLL_UP_LEFT, Speed);
        break;
      case 20:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCROLL_UP_RIGHT, Speed);
        break;
      case 21:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCROLL_DOWN_LEFT, Speed);
        break;
      case 22:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCROLL_DOWN_RIGHT, Speed);
        break;
      case 23:
        myDisplay.displayScroll(text, PA_CENTER, PA_GROW_UP, Speed);
        break;
      case 24:
        myDisplay.displayScroll(text, PA_CENTER, PA_GROW_DOWN, Speed);
        break;
      default:
        myDisplay.displayScroll(text, PA_CENTER, PA_SCROLL_LEFT, Speed);
        break;
    }
  }
}
