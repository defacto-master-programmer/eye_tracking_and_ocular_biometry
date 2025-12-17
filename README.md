CONFRONTO SEMPLIFICATO DELL'IRIDE (confrontoiride.py)

Progetto di "Principi e Modelli della Percezione"

DESCRIZIONE

Sistema base per il confronto di immagini di iridi utilizzando tecniche di visione artificiale. Questo approccio semplificato confronta direttamente i pixel delle immagini dopo una segmentazione e normalizzazione base, utilizzando la distanza euclidea come metrica di similarità. Il programma è progettato per scopi didattici e dimostrativi.

FUNZIONALITA

Il sistema implementa una pipeline di elaborazione in quattro fasi:

1. Segmentazione dell'iride
   Conversione dell'immagine in scala di grigi seguita da threshold binario inverso con soglia 50. Questo processo isola l'iride dallo sfondo separando le regioni chiare da quelle scure.

2. Normalizzazione semplificata
   Estrazione della regione centrale dell'immagine mediante crop rettangolare. Il sistema rimuove il 25% da ogni lato mantenendo il 50% centrale dell'immagine, che corrisponde approssimativamente alla zona dell'iride.

3. Estrazione delle caratteristiche
   Ridimensionamento dell'immagine normalizzata a 64x64 pixel seguito da appiattimento in un vettore unidimensionale di 4096 elementi. Ogni elemento rappresenta l'intensità di un singolo pixel.

4. Confronto tra iridi
   Calcolo della distanza euclidea tra i due vettori di caratteristiche. La formula applicata è la radice quadrata della somma dei quadrati delle differenze pixel per pixel.

PREREQUISITI

Sistema operativo: Linux, macOS, Windows
Python: versione 3.8 o superiore
Librerie Python richieste:
- opencv-python per elaborazione immagini
- numpy per operazioni matematiche
- scipy per calcolo distanze

Installazione dipendenze:
pip install opencv-python numpy scipy

IMMAGINI RICHIESTE

Il programma necessita di due immagini di iridi denominate iris1.jpg e iris2.jpg posizionate nella stessa directory dello script. Le immagini devono essere in formato JPG o PNG con risoluzione minima consigliata di 200x200 pixel.

UTILIZZO

Eseguire lo script dalla directory contenente le immagini:
python3 confrontoiride.py

Output atteso:
Distanza tra le due iridi: 2345.67

Il valore numerico rappresenta la distanza euclidea tra le due immagini. Valori più bassi indicano maggiore similarità.

INTERPRETAZIONE RISULTATI

Distanza minore di 1000: iridi molto simili, probabilmente stesso soggetto
Distanza tra 1000 e 5000: somiglianza moderata, verifica necessaria
Distanza maggiore di 5000: iridi diverse, soggetti diversi

Nota: questi valori sono indicativi e dipendono fortemente dalla qualità, dimensione e condizioni di acquisizione delle immagini.

STRUTTURA DEL CODICE

Funzione segment_iris(image)
Input: immagine BGR a colori
Output: immagine binaria
Processo: conversione in scala di grigi seguita da threshold binario inverso con soglia 50. I pixel sotto la soglia diventano bianchi (255), quelli sopra diventano neri (0).

Funzione normalize_iris(iris_image)
Input: immagine binaria segmentata
Output: immagine normalizzata (crop centrale)
Processo: estrazione della regione centrale calcolata come iris_image[height//4 : 3*height//4, width//4 : 3*width//4]. Questa operazione rimuove i bordi esterni mantenendo solo la parte centrale.

Funzione extract_iris_features(image)
Input: immagine normalizzata
Output: vettore di caratteristiche (array 1D)
Processo: ridimensionamento a 64x64 pixel usando interpolazione bilineare, seguito da appiattimento della matrice 2D in un vettore 1D di 4096 elementi mediante flatten().

Funzione compare_irises(iris1_features, iris2_features)
Input: due vettori di caratteristiche
Output: distanza euclidea (numero reale)
Processo: calcolo della norma L2 usando np.linalg.norm che implementa la formula sqrt(sum((a-b)^2)).

Pipeline principale:
1. Caricamento immagini con verifica errori
2. Segmentazione di entrambe le immagini
3. Normalizzazione delle immagini segmentate
4. Estrazione features da immagini normalizzate
5. Calcolo distanza euclidea tra features
6. Stampa risultato

PROBLEMI COMUNI E SOLUZIONI

Errore: ImportError: No module named cv2
Causa: OpenCV non installato
Soluzione: eseguire pip install opencv-python

Errore: FileNotFoundError
Causa: immagini non trovate nella directory corretta
Soluzione: verificare che iris1.jpg e iris2.jpg siano nella stessa cartella dello script oppure modificare i percorsi alle righe 29-30 del codice con percorsi assoluti

Errore: image is None
Causa: impossibile leggere il file immagine
Soluzione: verificare che i file non siano corrotti, che siano in formato supportato (JPG, PNG) e che abbiano i permessi di lettura corretti

Distanza sempre molto elevata
Causa: immagini troppo diverse per dimensioni o illuminazione
Soluzione: utilizzare immagini della stessa dimensione e normalizzare la luminosità. È possibile aggiungere equalizzazione dell'istogramma dopo la conversione in scala di grigi con cv2.equalizeHist(gray)

Distanza sempre molto bassa
Causa: immagini identiche o molto simili
Soluzione: verificare che le immagini siano effettivamente diverse

LIMITAZIONI TECNICHE

Questo approccio presenta diverse limitazioni rispetto ai sistemi biometrici professionali:

- Confronto diretto di pixel grezzi senza estrazione di pattern biometrici significativi
- Alta sensibilità a traslazioni, rotazioni e variazioni di scala
- Sensibilità marcata a cambiamenti di illuminazione
- Soglia di threshold fissa che potrebbe non essere ottimale per tutte le immagini
- Normalizzazione tramite crop rettangolare inadeguata per compensare deformazioni
- Assenza di invarianza rispetto a dilatazione pupillare

Accuratezza stimata: 60-70 percento in condizioni ottimali
Non adatto per: sistemi di sicurezza, autenticazione biometrica, applicazioni critiche
Non conforme a standard: ISO/IEC 19794-6

CONFRONTO CON APPROCCIO PROFESSIONALE

Aspetto                  Sistema semplificato         Sistema professionale
Complessità codice       Circa 60 righe              Circa 300 righe
Segmentazione            Threshold semplice          Contorni circolari
Normalizzazione          Crop rettangolare           Coordinate polari
Estrazione features      Pixel grezzi                Filtri di Gabor
Metrica confronto        Distanza euclidea           Distanza di Hamming
Accuratezza             60-70 percento              95-99 percento
Velocità                Molto veloce                Moderata
Robustezza              Bassa                       Alta
Uso consigliato         Didattico                   Professionale

QUANDO USARE QUESTO SISTEMA

Appropriato per:
- Progetti didattici e comprensione concetti base
- Prototipazione rapida di pipeline biometrica
- Test di qualità e caratteristiche delle immagini
- Dimostrazione principi di elaborazione immagini

Non appropriato per:
- Sistemi di sicurezza e controllo accessi
- Autenticazione biometrica in ambito reale
- Applicazioni che richiedono conformità a standard
- Database con elevato numero di soggetti

MIGLIORAMENTI POSSIBILI

Per aumentare l'accuratezza del sistema si potrebbero implementare:

1. Segmentazione avanzata usando Canny edge detection e trasformata di Hough per individuare cerchi invece del semplice threshold

2. Normalizzazione in coordinate polari mediante unwrapping circolare dell'iride dal centro verso l'esterno invece del crop rettangolare

3. Estrazione features mediante filtri di Gabor con orientazioni multiple invece dell'uso diretto dei valori pixel

4. Utilizzo di distanza di Hamming su codici binari invece della distanza euclidea sui pixel grezzi

Per un sistema completo e professionale fare riferimento a riconoscimento_iride.py che implementa lo standard ISO/IEC 19794-6 con algoritmo di Daugman.

NOTE FINALI

Questo codice è stato sviluppato per illustrare i concetti fondamentali della pipeline biometrica: segmentazione, normalizzazione, estrazione caratteristiche e confronto. La distanza euclidea fornisce una misura grezza di similarità ma non cattura i pattern biometrici unici dell'iride come fanno tecniche più avanzate basate su analisi di texture e frequenza.

La semplicità del codice lo rende ideale per comprendere i passaggi base del processo ma inadeguato per applicazioni reali che richiedono robustezza e accuratezza elevate.

Autore: Rebecca Fulginiti
Corso: Principi e Modelli della Percezione
Data: Dicembre 2024
