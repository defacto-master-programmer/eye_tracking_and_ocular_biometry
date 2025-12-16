import cv2
import numpy as np
import sys

def segment_iris_optimized(image, debug=False):
    """
    Segmentazione ottimizzata per iridi su sfondo nero
    """
    if image is None:
        raise ValueError("Immagine non valida")

    # Converti in scala di grigi
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Per iridi su sfondo nero, usa threshold inverso
    # Questo isola le parti chiare (l'iride) dallo sfondo nero
    _, binary = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

    if debug:
        cv2.imwrite('debug_binary.jpg', binary)
        print("   Salvato: debug_binary.jpg")

    # Trova i contorni
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        raise ValueError("Nessun contorno trovato")

    # Trova il contorno più circolare e grande
    best_contour = None
    best_score = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 100:  # Troppo piccolo
            continue

        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue

        # Calcola la circolarità
        circularity = 4 * np.pi * area / (perimeter * perimeter)

        # Combina area e circolarità
        score = area * circularity

        if score > best_score:
            best_score = score
            best_contour = cnt

    if best_contour is None:
        print("⚠️  Nessun contorno circolare trovato, uso il più grande")
        best_contour = max(contours, key=cv2.contourArea)

    # Calcola il cerchio che racchiude l'iride
    (x, y), radius = cv2.minEnclosingCircle(best_contour)

    if debug:
        debug_img = image.copy()
        cv2.circle(debug_img, (int(x), int(y)), int(radius), (0, 255, 0), 2)
        cv2.circle(debug_img, (int(x), int(y)), 3, (0, 0, 255), -1)
        cv2.drawContours(debug_img, [best_contour], -1, (255, 0, 0), 1)
        cv2.imwrite('debug_detection.jpg', debug_img)
        print("   Salvato: debug_detection.jpg")

    return (int(x), int(y)), int(radius)

def normalize_iris_polar(image, center, radius, num_radial=64, num_angular=360):
    """
    Normalizzazione migliorata in coordinate polari
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    height, width = gray.shape

    # Crea la rappresentazione polare
    polar_image = []

    # Campiona dall'interno verso l'esterno dell'iride
    for r_idx in range(num_radial):
        r = int((radius * r_idx) / num_radial)  # Raggio progressivo
        row = []
        for theta in range(num_angular):
            angle = (theta * 2 * np.pi) / num_angular
            x = int(center[0] + r * np.cos(angle))
            y = int(center[1] + r * np.sin(angle))

            if 0 <= x < width and 0 <= y < height:
                row.append(gray[y, x])
            else:
                row.append(0)  # Pixel nero se fuori bordo
        polar_image.append(row)

    return np.array(polar_image, dtype=np.uint8)

def extract_gabor_features(polar_image):
    """
    Estrae features usando filtri di Gabor multipli
    """
    features = []

    # Parametri Gabor: diverse orientazioni
    orientations = [0, np.pi/4, np.pi/2, 3*np.pi/4]

    for orientation in orientations:
        gabor_kernel = cv2.getGaborKernel(
            ksize=(21, 21),
            sigma=5.0,
            theta=orientation,
            lambd=10.0,
            gamma=0.5,
            psi=0,
            ktype=cv2.CV_32F
        )

        filtered = cv2.filter2D(polar_image, cv2.CV_32F, gabor_kernel)

        # Binarizza la risposta del filtro
        threshold = np.mean(filtered)
        binary = (filtered > threshold).astype(np.uint8)
        features.append(binary.flatten())

    # Concatena tutte le features
    return np.concatenate(features)

def hamming_distance_normalized(code1, code2):
    """
    Calcola la distanza di Hamming normalizzata
    """
    # Assicurati che abbiano la stessa lunghezza
    min_len = min(len(code1), len(code2))
    code1 = code1[:min_len]
    code2 = code2[:min_len]

    # Conta i bit diversi
    different_bits = np.sum(code1 != code2)

    # Normalizza tra 0 e 1
    normalized_distance = different_bits / min_len

    return different_bits, normalized_distance

def main():
    print("="*70)
    print("   SISTEMA DI RICONOSCIMENTO BIOMETRICO TRAMITE IRIDE")
    print("="*70)

    # Percorsi delle immagini
    img1_path = 'iris1.jpg'
    img2_path = 'iris2.jpg'

    print(f"\n Caricamento immagini...")
    image1 = cv2.imread(img1_path)
    image2 = cv2.imread(img2_path)

    if image1 is None:
        print(f" ERRORE: Impossibile caricare '{img1_path}'")
        sys.exit(1)

    if image2 is None:
        print(f" ERRORE: Impossibile caricare '{img2_path}'")
        sys.exit(1)

    print(f" Immagine 1: {image1.shape} ({img1_path})")
    print(f" Immagine 2: {image2.shape} ({img2_path})")

    try:
        # STEP 1: Segmentazione
        print(f"\n STEP 1: Segmentazione dell'iride...")
        center1, radius1 = segment_iris_optimized(image1, debug=False)
        print(f"   Iride 1: Centro=({center1[0]}, {center1[1]}), Raggio={radius1}px")

        center2, radius2 = segment_iris_optimized(image2, debug=False)
        print(f"   Iride 2: Centro=({center2[0]}, {center2[1]}), Raggio={radius2}px")

        # STEP 2: Normalizzazione polare
        print(f"\n STEP 2: Normalizzazione in coordinate polari...")
        polar1 = normalize_iris_polar(image1, center1, radius1)
        polar2 = normalize_iris_polar(image2, center2, radius2)
        print(f"   Immagine polare 1: {polar1.shape}")
        print(f"   Immagine polare 2: {polar2.shape}")

        # Salva le immagini polari per debug
        cv2.imwrite('polar1.jpg', polar1)
        cv2.imwrite('polar2.jpg', polar2)
        print(f" Salvate: polar1.jpg, polar2.jpg")

        # STEP 3: Estrazione features con Gabor
        print(f"\n  STEP 3: Estrazione features con filtri di Gabor...")
        features1 = extract_gabor_features(polar1)
        features2 = extract_gabor_features(polar2)
        print(f"   Feature vector 1: {len(features1)} bit")
        print(f"   Feature vector 2: {len(features2)} bit")

        # STEP 4: Confronto con distanza di Hamming
        print(f"\n  STEP 4: Calcolo distanza di Hamming...")
        diff_bits, norm_distance = hamming_distance_normalized(features1, features2)

        # RISULTATI
        print("\n" + "="*70)
        print("                           RISULTATI")
        print("="*70)
        print(f"\n Distanza di Hamming:")
        print(f"   • Bit differenti: {diff_bits:,}")
        print(f"   • Distanza normalizzata: {norm_distance:.4f}")
        print(f"   • Similarità: {(1-norm_distance)*100:.2f}%")

        # INTERPRETAZIONE
        print(f"\n INTERPRETAZIONE:")
        print(f"   Soglia di accettazione standard: 0.32 (32%)")
        print(f"   Valore ottenuto: {norm_distance:.4f} ({norm_distance*100:.2f}%)")
        print()

        if norm_distance < 0.32:
            print("  MATCH POSITIVO")
            print("   → Le iridi appartengono probabilmente ALLO STESSO soggetto")
            confidence = (1 - norm_distance) * 100
            print(f"   → Confidenza: {confidence:.1f}%")
        elif norm_distance < 0.40:
            print("    ZONA GRIGIA")
            print("   → Necessaria verifica manuale o ulteriori test")
            confidence = (1 - norm_distance) * 100
            print(f"   → Confidenza: {confidence:.1f}%")
        else:
            print("  MATCH NEGATIVO")
            print("   → Le iridi appartengono a SOGGETTI DIVERSI")
            confidence = (1 - norm_distance) * 100
            print(f"   → Confidenza: {confidence:.1f}%")


    except Exception as e:
        print(f"\n ERRORE durante l'elaborazione:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
