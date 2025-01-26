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

// Uncomment according to your hardware type
#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
//define HARDWARE_TYPE MD_MAX72XX::GENERIC_HW

// Defining size, and output pins
#define MAX_DEVICES 16
#define CS_PIN 15
#define CLK_PIN 14
#define DATA_PIN 2

MD_Parola myDisplay = MD_Parola(HARDWARE_TYPE, DATA_PIN, CLK_PIN, CS_PIN, MAX_DEVICES);
#define  BUF_SIZE  75
String string_text="ESP32";

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
    <form id="matrixForm">
        <input type="text" id="textInput" name="text" placeholder="Entrez votre texte (max 40 caractères)" maxlength="40">
        <button type="submit">Envoyer</button>
    </form>
    <div id="result"></div>

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

  server.on(F("/"), []() {
    server.send(200, "text/html", index_html);
  });
  
  server.on(UriBraces("/text/{}"), []() {
    string_text = urlDecode(server.pathArg(0).c_str());
    server.send(200, "text/plain", "Text: '" + string_text + "'");
  });

  server.begin();
  Serial.println("HTTP server started");

  myDisplay.displayClear();
  myDisplay.displayReset();
  string_text=WiFi.localIP().toString();
  
}

void loop() {
  server.handleClient();
  if (myDisplay.displayAnimate()) {
    myDisplay.displayReset();
    const char *text = string_text.c_str();
    myDisplay.displayScroll(text, PA_CENTER, PA_SCROLL_LEFT, 100);
  }
}
