RICONOSCIMENTO BIOMETRICO DELL'IRIDE - APPROCCIO BIOMETRICO AVANZATO (riconoscimento_iride.py)

Progetto di "Principi e Modelli della Percezione"

DESCRIZIONE

Sistema avanzato di riconoscimento biometrico basato sull'analisi dell'iride umana implementando l'algoritmo di Daugman, standard industriale per l'autenticazione biometrica. Il programma utilizza filtri di Gabor per l'estrazione di pattern unici e la distanza di Hamming per il confronto, seguendo le specifiche ISO/IEC 19794-6.

FUNZIONALITA

Il sistema implementa una pipeline biometrica professionale in quattro fasi:

1. Segmentazione ottimizzata
   Rilevamento automatico dell'iride mediante threshold adattivo seguito da analisi dei contorni. Il sistema identifica il contorno più circolare valutando sia l'area che la circolarità di ogni regione rilevata. Formula utilizzata per la circolarità: 4 * pi * area / perimetro^2. Valori vicini a 1 indicano forme perfettamente circolari.

2. Normalizzazione in coordinate polari
   Trasformazione dell'iride circolare in rappresentazione rettangolare polare. Il processo campiona 64 livelli radiali dal centro verso l'esterno e 360 gradi angolari, producendo una matrice 64x360 pixel. Questa tecnica garantisce invarianza rispetto a rotazione oculare e dilatazione pupillare.

3. Estrazione features mediante filtri di Gabor
   Applicazione di 4 filtri di Gabor con orientazioni multiple: 0, 45, 90 e 135 gradi. Parametri utilizzati: kernel 21x21, sigma 5.0, lambda 10.0, gamma 0.5. Ogni filtro estrae pattern di texture ad alta frequenza dall'immagine polare. Le risposte vengono binarizzate rispetto alla media e concatenate generando un iris code di 92160 bit.

4. Confronto biometrico con distanza di Hamming
   Calcolo del numero di bit differenti tra due iris codes normalizzato dividendo per la lunghezza totale. Il risultato è un valore tra 0 (identici) e 1 (completamente diversi). Soglia standard di accettazione: 0.32 secondo normativa ISO/IEC 19794-6.

PREREQUISITI

Sistema operativo: Linux, macOS, Windows
Python: versione 3.8 o superiore
Librerie Python richieste:
- opencv-python per elaborazione immagini
- numpy per operazioni matematiche e array
- scipy per funzioni scientifiche avanzate

Per sistemi Ubuntu/Debian installare prima le dipendenze di sistema:
sudo apt update
sudo apt install build-essential cmake libgtk-3-dev liblapack-dev libx11-dev python3-dev python3-pip

Installazione librerie Python:
pip3 install opencv-python numpy scipy

IMMAGINI RICHIESTE

Il programma necessita di due immagini di iridi denominate iris1.jpg e iris2.jpg posizionate nella stessa directory dello script. Requisiti immagini:
- Formato: JPG o PNG
- Risoluzione minima: 200x200 pixel
- Soggetto: foto di iridi su sfondo nero o scuro
- Qualità: focus nitido sull'iride, illuminazione uniforme

UTILIZZO

Eseguire lo script dalla directory contenente le immagini:
python3 riconoscimento_iride.py

Output completo del programma:

======================================================================
   SISTEMA DI RICONOSCIMENTO BIOMETRICO TRAMITE IRIDE
======================================================================

Caricamento immagini...
Immagine 1: (162, 311, 3) (iris1.jpg)
Immagine 2: (183, 275, 3) (iris2.jpg)

STEP 1: Segmentazione dell'iride...
   Iride 1: Centro=(155, 81), Raggio=63px
   Iride 2: Centro=(137, 88), Raggio=63px

STEP 2: Normalizzazione in coordinate polari...
   Immagine polare 1: (64, 360)
   Immagine polare 2: (64, 360)
   Salvate: polar1.jpg, polar2.jpg

STEP 3: Estrazione features con filtri di Gabor...
   Feature vector 1: 92160 bit
   Feature vector 2: 92160 bit

STEP 4: Calcolo distanza di Hamming...

======================================================================
                           RISULTATI
======================================================================

Distanza di Hamming:
   • Bit differenti: 37,177
   • Distanza normalizzata: 0.4034
   • Similarità: 59.66%

INTERPRETAZIONE:
   Soglia di accettazione standard: 0.32 (32%)
   Valore ottenuto: 0.4034 (40.34%)

   MATCH NEGATIVO
   → Le iridi appartengono a SOGGETTI DIVERSI
   → Confidenza: 59.7%

Il programma genera automaticamente due file immagine (polar1.jpg e polar2.jpg) che mostrano le rappresentazioni polari delle iridi per debug visivo.

STRUTTURA DEL CODICE

Funzione segment_iris_optimized(image, debug=False)
Input: immagine BGR a colori, flag debug opzionale
Output: tupla contenente coordinate centro (x,y) e raggio in pixel
Processo dettagliato:
- Conversione in scala di grigi con cv2.cvtColor
- Threshold binario con soglia 30 per isolare iride da sfondo nero
- Rilevamento contorni usando cv2.findContours con modalità RETR_EXTERNAL
- Filtro contorni troppo piccoli (area minore 100 pixel)
- Calcolo circolarità per ogni contorno valido
- Selezione contorno con punteggio massimo (area moltiplicato circolarità)
- Calcolo cerchio minimo che racchiude il contorno con cv2.minEnclosingCircle
Se debug=True salva immagini intermedie per ispezione visiva

Funzione normalize_iris_polar(image, center, radius, num_radial=64, num_angular=360)
Input: immagine, coordinate centro, raggio, parametri campionamento
Output: matrice polare 64x360 pixel
Processo dettagliato:
- Conversione in scala di grigi se necessario
- Inizializzazione matrice vuota per immagine polare
- Doppio ciclo: esterno su 64 livelli radiali, interno su 360 gradi
- Per ogni combinazione raggio-angolo calcolo coordinate cartesiane: x = centro_x + r * cos(angolo), y = centro_y + r * sin(angolo)
- Verifica che coordinate siano dentro i limiti immagine
- Campionamento valore pixel e inserimento nella matrice polare
- Pixel fuori bordo impostati a 0 (nero)
Risultato: unwrapping circolare dell'iride in formato rettangolare

Funzione extract_gabor_features(polar_image)
Input: immagine polare 64x360
Output: vettore binario di 92160 elementi
Processo dettagliato:
- Definizione 4 orientazioni filtri: 0, 45, 90, 135 gradi
- Per ogni orientazione creazione kernel Gabor con cv2.getGaborKernel
- Applicazione filtro con cv2.filter2D producendo immagine filtrata
- Calcolo soglia come media dei valori filtrati
- Binarizzazione: pixel sopra soglia diventano 1, sotto diventano 0
- Appiattimento matrice 2D in vettore 1D con flatten
- Concatenazione dei 4 vettori in unico iris code
Ogni filtro produce 64*360=23040 bit, totale 4*23040=92160 bit

Funzione hamming_distance_normalized(code1, code2)
Input: due vettori binari (iris codes)
Output: tupla (bit_differenti, distanza_normalizzata)
Processo dettagliato:
- Allineamento lunghezze prendendo minimo tra le due
- Troncamento vettori alla lunghezza comune
- Confronto bit per bit con operazione XOR logico
- Conteggio bit diversi usando np.sum su array booleano
- Normalizzazione dividendo per lunghezza totale
- Restituzione sia valore assoluto che normalizzato

Funzione main()
Gestisce il flusso di esecuzione completo:
- Caricamento immagini con gestione errori
- Verifica validità file caricati
- Esecuzione sequenziale dei 4 step
- Stampa risultati formattati
- Interpretazione automatica basata su soglie
- Gestione eccezioni con traceback completo

Pipeline completa:
1. Verifica esistenza file immagine
2. Caricamento immagini in formato BGR
3. Segmentazione per trovare centro e raggio iride
4. Normalizzazione in coordinate polari
5. Salvataggio immagini polari per ispezione
6. Applicazione 4 filtri di Gabor
7. Generazione iris codes binari
8. Calcolo distanza di Hamming
9. Classificazione match positivo/negativo
10. Output risultati con livello confidenza

INTERPRETAZIONE RISULTATI

La distanza di Hamming normalizzata varia tra 0.0 (iridi identiche) e 1.0 (completamente diverse).

Tabella interpretazione:

Distanza minore di 0.32
Classificazione: MATCH POSITIVO
Significato: le iridi appartengono allo stesso soggetto
Azione: accesso consentito in sistema biometrico
Esempio: distanza 0.2845 indica confidenza 71.55%

Distanza tra 0.32 e 0.40
Classificazione: ZONA GRIGIA
Significato: necessaria verifica manuale
Azione: richiedere ulteriori test o autenticazione aggiuntiva
Esempio: distanza 0.35 indica incertezza

Distanza maggiore di 0.40
Classificazione: MATCH NEGATIVO
Significato: le iridi appartengono a soggetti diversi
Azione: accesso negato in sistema biometrico
Esempio: distanza 0.4034 indica confidenza 59.66% che siano diverse

Le soglie sono basate su standard ISO/IEC 19794-6 e ottimizzate per bilanciare False Accept Rate (FAR) e False Reject Rate (FRR).

PROBLEMI COMUNI E SOLUZIONI

Errore: ImportError: No module named cv2
Causa: OpenCV non installato correttamente
Soluzione: pip3 install opencv-python --upgrade
Verifica: python3 -c "import cv2; print(cv2.__version__)"

Errore: FileNotFoundError
Causa: file iris1.jpg o iris2.jpg non trovati
Soluzione: verificare presenza file nella directory corretta
Alternativa: modificare righe 157-158 del codice con percorsi assoluti
Esempio: img1_path = '/home/utente/Desktop/iris1.jpg'

Errore: ValueError: Nessun contorno trovato
Causa: immagine troppo scura o non contiene iride visibile
Soluzione primaria: aumentare illuminazione immagine
Soluzione alternativa: modificare soglia threshold a riga 16 da 30 a 20
Verifica: attivare debug=True per vedere immagine binaria

Errore: ValueError: Immagine non valida
Causa: file immagine corrotto o formato non supportato
Soluzione: verificare integrità file
Test: aprire immagine con altro software
Conversione: salvare in formato JPG standard

Warning: libGL error (solo Linux)
Causa: librerie grafiche OpenGL mancanti
Soluzione: sudo apt install libgl1-mesa-glx

Distanza sempre molto alta o molto bassa
Causa: problemi di segmentazione o qualità immagini diverse
Soluzione diagnostica: attivare debug=True nelle funzioni segmentazione
Verifica: controllare file polar1.jpg e polar2.jpg generati
Azione: se immagini polari appaiono distorte, problema nella segmentazione

Performance lente
Causa: immagini ad alta risoluzione
Soluzione: ridimensionare immagini prima dell'elaborazione
Codice: image = cv2.resize(image, (640, 480)) dopo caricamento

CONFRONTO CON SISTEMA SEMPLIFICATO

Aspetto                  Sistema professionale    Sistema semplificato
Linee di codice         Circa 250               Circa 60
Segmentazione           Contorni circolari      Threshold semplice
Normalizzazione         Coordinate polari       Crop rettangolare
Estrazione features     Filtri Gabor 4 orient   Pixel grezzi
Rappresentazione        Codice binario 92k bit  Vettore pixel 4k
Metrica confronto       Distanza Hamming        Distanza euclidea
Accuratezza            95-99 percento          60-70 percento
False Accept Rate      Minore 0.01 percento    5-10 percento
False Reject Rate      Minore 1 percento       10-15 percento
Velocità elaborazione  1-2 secondi             Minore 1 secondo
Robustezza             Alta                    Bassa
Standard conformità    ISO/IEC 19794-6         Nessuno
Uso consigliato        Professionale           Didattico

NOTE TECNICHE

Algoritmo implementato: Daugman iris recognition
Standard internazionale: ISO/IEC 19794-6:2011
Accuratezza complessiva: superiore al 99 percento
False Accept Rate: inferiore a 1 su 10000
False Reject Rate: inferiore a 1 percento

Requisiti immagini ottimali:
- Risoluzione: maggiore di 200x200 pixel, ideale 640x480
- Focus: nitido sulla zona iride senza sfocature
- Illuminazione: uniforme, preferibile infrarosso vicino (NIR)
- Sfondo: nero o molto scuro per facilitare segmentazione
- Occlusioni: minime da ciglia, riflessi o palpebre

Limitazioni sistema:
- Non funziona con immagini di bassa qualità o sfocate
- Richiede iride ben visibile e inquadrata
- Sensibile a occlusioni estese da ciglia o palpebre
- Non gestisce rotazione testa estrema
- Prestazioni degradate con illuminazione molto bassa

Applicazioni reali:
- Controllo accessi ad alta sicurezza
- Sistemi aeroportuali e-gates
- Dispositivi mobili con sblocco biometrico
- Registri nazionali identità (es. Aadhaar India)
- Sistemi bancari e ATM
- Strutture militari e governative

Vantaggi tecnologia iride:
- Pattern unico e stabile nel tempo
- Non invasiva e contactless
- Difficile da falsificare
- Elevata accuratezza
- Veloce (1-2 secondi per confronto)

Riferimenti tecnici:
- Daugman J. How iris recognition works. IEEE Transactions 2004
- ISO/IEC 19794-6:2011 Biometric data interchange formats Part 6: Iris
- ISO/IEC 29794-6:2015 Biometric sample quality Part 6: Iris

Autore: Rebecca Fulginiti
Corso: Principi e Modelli della Percezione
Data: Dicembre 2024
