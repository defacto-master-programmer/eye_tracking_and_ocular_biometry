BIOMETRIA OCULARE E EYE TRACKING - PRESENTAZIONE

Progetto di "Principi e Modelli della Percezione"

DESCRIZIONE

Presentazione completa sui sistemi di analisi oculare per biometria e tracciamento dello sguardo. Il materiale copre sia gli aspetti teorici (trasformata di Hough, algoritmo di Daugman, filtri di Gabor) sia implementazioni pratiche con analisi comparativa di approcci semplificati e professionali.

CONTENUTO PRESENTAZIONE

La presentazione è strutturata in 52 slide organizzate in quattro sezioni principali:

Sezione 1: Fondamenti Trasformata di Hough
Introduzione alla trasformata di Hough per rilevamento forme geometriche. Spiegazione del meccanismo di voto, spazio parametri e applicazioni per rilevamento rette e cerchi. Confronto tra approccio Hough classico e MediaPipe per localizzazione oculare in eye tracking.

Sezione 2: Eye Tracking con MediaPipe
Analisi dettagliata del sistema di tracciamento sguardo implementato. Descrizione della funzione run() con fasi di acquisizione video, pre-processing, analisi facciale tramite Face Mesh (478 landmark), calibrazione automatica e fase operativa. Presentazione dei grafici generati: andamento temporale movimento occhi e mappa dispersione 2D.

Sezione 3: Riconoscimento Biometrico Iride
Spiegazione algoritmo di Daugman per autenticazione biometrica. Pipeline completa: acquisizione immagine, localizzazione iride, unwrapping in coordinate polari, applicazione filtri di Gabor per estrazione pattern, generazione iris code binario, calcolo distanza di Hamming per matching. Include esempi pratici di iris code matching.

Sezione 4: Analisi Comparativa Implementazioni
Confronto tra due approcci implementati: sistema semplificato (threshold, crop rettangolare, distanza euclidea) e sistema professionale (contorni circolari, coordinate polari, filtri Gabor, distanza Hamming). Presentazione risultati ottenuti con immagini reali, discussione problemi nel matching, dispositivi di acquisizione, applicazioni reali e considerazioni sulla privacy.

STRUTTURA LOGICA

La presentazione segue un percorso logico dall'elaborazione immagini base (trasformata di Hough) alle applicazioni biometriche avanzate. Include sia teoria matematica che implementazioni pratiche con risultati reali. Ogni sezione contiene esempi visivi e codice commentato per facilitare la comprensione.

Slide chiave:
- Slide 8: Trasformata di Hough per cerchi
- Slide 15: Confronto metodologico Hough vs MediaPipe
- Slide 16-23: Funzionamento completo eye tracker
- Slide 27-38: Algoritmo Daugman passo per passo
- Slide 40-44: Risultati comparativi sistemi implementati
- Slide 47: Applicazioni reali autenticazione biometrica

ARGOMENTI TRATTATI

Trasformata di Hough: meccanismo di voto, spazio parametri, rilevamento rette e cerchi, variante generalizzata.

Eye Tracking: MediaPipe Face Mesh, calibrazione automatica, tracking binoculare, coordinate normalizzate, generazione grafici movimento.

Riconoscimento Iride: pattern unici iride, algoritmo Daugman, localizzazione tramite operatori integro-differenziali, unwrapping circolare (rubber sheet model), filtri di Gabor 2D per estrazione texture, iris code binario, distanza Hamming per matching, soglie FAR/FRR.

Implementazioni: confronto approccio base (60-70% accuratezza) vs professionale (95-99% accuratezza), analisi problemi reali, dispositivi acquisizione commerciali.

NOTE

Il materiale fa riferimento ai tre script Python sviluppati: confrontoiride.py (sistema base), riconoscimento_iride.py (sistema professionale) e eye_gaze_tracker.py (tracciamento sguardo). I risultati mostrati sono basati su test reali con immagini iris1.jpg e iris2.jpg fornite.

