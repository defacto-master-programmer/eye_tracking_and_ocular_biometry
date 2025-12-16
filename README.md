Eye Tracker con MediaPipe

Questo progetto implementa un sistema di tracciamento dello sguardo in tempo reale utilizzando Python, OpenCV e MediaPipe Face Mesh. Il software rileva la posizione delle iridi per determinare la direzione dello sguardo (Centro, Sinistra, Destra, Alto, Basso) e genera grafici statistici al termine della sessione.

Funzionalità

* Rilevamento Facciale: Utilizza MediaPipe per tracciare i landmark del volto e dell'iride.  
* Calibrazione Automatica: I primi 60 frame vengono utilizzati per calibrare il "centro" soggettivo dell'utente.  
* Analisi in Tempo Reale: Feedback visivo a schermo con direzione dello sguardo e coordinate.  
* Reportistica Grafica: Generazione automatica di grafici (andamento temporale e dispersione) alla chiusura del programma.

Prerequisiti e Installazione

Le librerie richieste sono elencate di seguito. Puoi installarle eseguendo questo comando nel terminale:

pip install opencv-python mediapipe numpy matplotlib

Librerie utilizzate nel dettaglio:

* opencv-python: Per l'acquisizione video e l'elaborazione delle immagini.  
* mediapipe: Per il rilevamento dei landmark facciali (Face Mesh).  
* numpy: Per operazioni matematiche e gestione degli array.  
* matplotlib: Per la generazione dei grafici finali.

Utilizzo

1. Assicurati che la webcam sia collegata.  
2. Esegui lo script da terminale:  
   python eyetrack.py

3. **Fase di Calibrazione:** Appena avviato, guarda fisso al **centro** dello schermo per circa 2 secondi (fino al riempimento della barra verde).  
4. Una volta calibrato, muovi gli occhi per testare il rilevamento.  
5. Premi il tasto **q** sulla tastiera per terminare la sessione.  
6. Attendere qualche istante per il salvataggio dei grafici nella cartella del progetto.

## **Configurazione e Parametri**

È possibile modificare il comportamento del tracker agendo direttamente sulle variabili all'interno della classe EyeGazeTracker nel file.

1\. Soglie di Attivazione (Thresholds)**

Le soglie determinano quanto l'utente deve spostare lo sguardo affinché venga rilevato come "Destra", "Sinistra", ecc. I valori sono normalizzati tra 0.0 e 1.0 (dove 0.5 è il centro).

Puoi modificare queste variabili nel metodo \_\_init\_\_:

| Variabile | Valore Default | Descrizione |
| :---- | :---- | :---- |
| self.LEFT\_THRESH | **0.42** | Valori inferiori a questo indicano "Sinistra". |
| self.RIGHT\_THRESH | **0.58** | Valori superiori a questo indicano "Destra". |
| self.UP\_THRESH | **0.38** | Valori inferiori a questo indicano "Alto". |
| self.DOWN\_THRESH | **0.62** | Valori superiori a questo indicano "Basso". |

* Consiglio: Se il sistema è troppo sensibile (rileva movimenti anche stando fermi), allarga il range (es. abbassa LEFT a 0.40 e alza RIGHT a 0.60).

2\. Path e Nomi Immagini di Output**

I nomi dei file generati vengono definiti nel metodo save\_plots. Puoi modificarli se desideri salvare i file in una sottocartella o con nomi diversi.

* **Grafico Temporale:**  
  * Cerca la riga: filename\_time \= 'grafico\_movimenti\_occhi\_tempo.png'  
  * Esempio modifica: filename\_time \= 'output/sessione\_tempo.png' (assicurati che la cartella esista).  
* **Grafico Dispersione:**  
  * Cerca la riga: filename\_scatter \= 'grafico\_dispersione\_sguardo.png'

3\. Durata Calibrazione**

Per modificare la durata della fase iniziale di calibrazione, modifica la variabile CALIBRATION\_FRAMES nel metodo \_\_init\_\_:

self.CALIBRATION\_FRAMES \= 60

Output Generato

Alla chiusura del programma, verranno creati due file PNG nella stessa directory dello script:

1. **grafico\_movimenti\_occhi\_tempo.png**: Mostra come le coordinate X (blu) e Y (rosso) sono cambiate durante la sessione rispetto al tempo (frame). Le aree colorate indicano la "zona centro".  
2. **grafico\_dispersione\_sguardo.png**: Una "mappa di calore" (scatter plot) che mostra dove si è concentrato maggiormente lo sguardo dell'utente (es. in alto a destra, al centro, ecc.).

Nota: L'illuminazione ambientale influisce sulla precisione di MediaPipe. Per risultati ottimali, assicurati che il volto sia ben illuminato.
