import cv2
import numpy as np
from scipy.spatial.distance import hamming

# Funzione per segmentare l'iride (usando un semplice thresholding)
def segment_iris(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    return binary
# Funzione per normalizzare l'iride (unwrapping)
def normalize_iris(iris_image):
    # Normalizzazione dell'immagine in un formato plano (unwrapped)
    # In questo esempio, usiamo un approccio semplificato basato su un wrapping circolare.
    height, width = iris_image.shape
    normalized_iris = iris_image[height // 4 : 3 * height // 4, width // 4 : 3 * width // 4]
    return normalized_iris

# Funzione per estrarre la "firma" dell'iride (hash o vettore)
def extract_iris_features(image):
    # Estrarre una rappresentazione unica (es. hash) dell'iride
    image = cv2.resize(image, (64, 64))  # Ridimensiona l'immagine
    features = image.flatten()  # Appiattisci l'immagine per ottenere un vettore
    return features

# Funzione per calcolare la distanza tra due immagini di iridi
def compare_irises(iris1_features, iris2_features):
    # Usa la distanza Euclidea per confrontare le caratteristiche estratte
    distance = np.linalg.norm(iris1_features - iris2_features)
    return distance

# Carica le due immagini di iride
image1 = cv2.imread('/Users/rebeccafulginiti/Desktop/RiconoscimentoIride/iris1.jpg')  # Cambia il percorso del file
image2 = cv2.imread('/Users/rebeccafulginiti/Desktop/RiconoscimentoIride/iris2.jpg')  # Cambia il percorso del file

image1 = cv2.imread('iris1.jpg')
if image1 is None:
    print("Errore nel caricare l'immagine 1")

image2 = cv2.imread('iris2.jpg')
if image2 is None:
    print("Errore nel caricare l'immagine 2")

# Segmentazione delle immagini
segmented_iris1 = segment_iris(image1)
segmented_iris2 = segment_iris(image2)

# Normalizzazione (unwrapping) delle iridi
normalized_iris1 = normalize_iris(segmented_iris1)
normalized_iris2 = normalize_iris(segmented_iris2)

# Estrazione delle caratteristiche (firma)
iris1_features = extract_iris_features(normalized_iris1)
iris2_features = extract_iris_features(normalized_iris2)

# Confronto delle iridi
similarity = compare_irises(iris1_features, iris2_features)
print(f'Distanza tra le due iridi: {similarity}')
