import cv2
import mediapipe as mp
import numpy as np
import math
import matplotlib.pyplot as plt
import time

class EyeGazeTracker:
    def __init__(self):
        # Inizializzazione MediaPipe Face Mesh
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,  # Importante per ottenere i punti dell'iride
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # --- INDICI LANDMARK MEDIAPIPE ---
        # Occhio SINISTRO (della persona)
        self.LEFT_EYE_INDICES = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.LEFT_IRIS = 473
        self.LEFT_CORNERS = [362, 263]  # Interno, Esterno

        # Occhio DESTRO (della persona)
        self.RIGHT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        self.RIGHT_IRIS = 468
        self.RIGHT_CORNERS = [133, 33]  # Interno, Esterno
        
        # Per la raccolta dati del grafico
        self.history_x = []
        self.history_y = []
        self.frame_indices = []
        self.frame_count = 0

        # Variabili per la calibrazione
        self.is_calibrated = False
        self.calibration_buffer_x = []
        self.calibration_buffer_y = []
        self.CALIBRATION_FRAMES = 60 # Numero di frame per la calibrazione (circa 2 secondi)
        self.center_offset_x = 0.0
        self.center_offset_y = 0.0

        # Soglie per i grafici
        self.LEFT_THRESH = 0.42
        self.RIGHT_THRESH = 0.58
        self.UP_THRESH = 0.38
        self.DOWN_THRESH = 0.62

    #Calcola la distanza euclidea tra due punti (x, y).
    def euclidean_distance(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    #Calcola i ratio per un singolo occhio.
    def get_eye_gaze_stats(self, landmarks, corner_indices, iris_index, frame_shape):

        h, w, _ = frame_shape
        
        p_inner = landmarks[corner_indices[0]]
        p_outer = landmarks[corner_indices[1]]
        p_iris = landmarks[iris_index]

        inner_coords = np.array([p_inner.x * w, p_inner.y * h])
        outer_coords = np.array([p_outer.x * w, p_outer.y * h])
        iris_coords = np.array([p_iris.x * w, p_iris.y * h])

        # --- Ratio Orizzontale ---
        eye_width = self.euclidean_distance(inner_coords, outer_coords)
        if eye_width == 0: return 0.5, 0.5

        x_min = min(inner_coords[0], outer_coords[0])
        x_max = max(inner_coords[0], outer_coords[0])
        
        current_x = iris_coords[0]
        ratio_x = (current_x - x_min) / (x_max - x_min)
        ratio_x = max(0.0, min(1.0, ratio_x))

        # --- Ratio Verticale (Migliorato) ---
        eye_center_y = (inner_coords[1] + outer_coords[1]) / 2
        diff_y = iris_coords[1] - eye_center_y
        ratio_y_norm = diff_y / eye_width 
        scaling_factor = 3.0
        ratio_y = 0.5 + (ratio_y_norm * scaling_factor)
        ratio_y = max(0.0, min(1.0, ratio_y))

        return ratio_x, ratio_y, iris_coords

    #Mappa i ratio medi in direzioni testuali.
    def determine_direction(self, x_ratio, y_ratio):
        
        text_x = "Centro"
        text_y = "Centro"

        # Logica orizzontale
        if x_ratio > self.RIGHT_THRESH:
            text_x = "Destra"
        elif x_ratio < self.LEFT_THRESH:
            text_x = "Sinistra"

        # Logica verticale
        if y_ratio < self.UP_THRESH:
            text_y = "Alto"
        elif y_ratio > self.DOWN_THRESH:
            text_y = "Basso"

        if text_x == "Centro" and text_y == "Centro":
            return "Centro"
        if text_x == "Centro": return text_y
        if text_y == "Centro": return text_x
        
        return f"{text_y} {text_x}"

    #Genera e salva i grafici finali
    def save_plots(self):
        
        if not self.frame_indices:
            print("Nessun dato raccolto.")
            return

        print("Generazione grafici in corso...")
        
        # --- Grafico 1: Andamento Temporale ---
        plt.figure(figsize=(12, 6))
        plt.plot(self.frame_indices, self.history_x, label='X (Orizzontale: 0=Sx, 1=Dx)', color='blue', alpha=0.7)
        plt.plot(self.frame_indices, self.history_y, label='Y (Verticale: 0=Alto, 1=Basso)', color='red', alpha=0.7)
        
        plt.axhline(y=0.5, color='black', linestyle='-', alpha=0.3, linewidth=1)
        plt.axhspan(self.LEFT_THRESH, self.RIGHT_THRESH, color='gray', alpha=0.1, label='Zona Centro X')
        plt.axhspan(self.UP_THRESH, self.DOWN_THRESH, color='red', alpha=0.05, label='Zona Centro Y')

        plt.title('Movimento Sguardo nel Tempo (Post-Calibrazione)')
        plt.xlabel('Frame')
        plt.ylabel('Posizione Normalizzata (0.5 = Centro)')
        plt.legend()
        # plt.grid(True, linestyle='--', alpha=0.5) # Rimosso griglia sfondo
        
        filename_time = 'grafico_movimenti_occhi_tempo.png'
        plt.savefig(filename_time)
        print(f"Grafico temporale salvato come '{filename_time}'")
        plt.close()

        # --- Grafico 2: Scatter Plot (Mappa dello Sguardo) ---
        plt.figure(figsize=(8, 8))
        # Crea il grafico a dispersione con punti semitrasparenti
        plt.scatter(self.history_x, self.history_y, color='purple', alpha=0.3, s=15, label='Punto Sguardo')
        
        # Imposta i limiti degli assi
        plt.xlim(0.0, 1.0)
        plt.ylim(1.0, 0.0) # Invertiamo l'asse Y per coerenza (0=Alto, 1=Basso)

        # Aggiungi linee e zone di riferimento
        plt.axhline(y=0.5, color='black', linestyle='--', alpha=0.5)
        plt.axvline(x=0.5, color='black', linestyle='--', alpha=0.5)
        
        # Linee di soglia
        plt.axvline(x=self.LEFT_THRESH, color='blue', linestyle=':', alpha=0.4)
        plt.axvline(x=self.RIGHT_THRESH, color='blue', linestyle=':', alpha=0.4)
        plt.axhline(y=self.UP_THRESH, color='red', linestyle=':', alpha=0.4)
        plt.axhline(y=self.DOWN_THRESH, color='red', linestyle=':', alpha=0.4)

        # Etichette per le zone (opzionale)
        plt.text(0.1, 0.1, 'Alto-Sx', color='gray', ha='center')
        plt.text(0.9, 0.1, 'Alto-Dx', color='gray', ha='center')
        plt.text(0.1, 0.9, 'Basso-Sx', color='gray', ha='center')
        plt.text(0.9, 0.9, 'Basso-Dx', color='gray', ha='center')
        plt.text(0.5, 0.5, 'Centro', color='black', ha='center')

        plt.title('Mappa di Dispersione dello Sguardo (X vs Y)')
        plt.xlabel('Posizione Orizzontale (0=Sinistra, 1=Destra)')
        plt.ylabel('Posizione Verticale (0=Alto, 1=Basso)')
        plt.legend()

        filename_scatter = 'grafico_dispersione_sguardo.png'
        plt.savefig(filename_scatter)
        print(f"Grafico a dispersione salvato come '{filename_scatter}'")
        plt.close()

    def run(self):
        cap = cv2.VideoCapture(0)
        print("Premi 'q' per terminare.")

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1) # Specchio
            h, w, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)

            direction_text = ""
            
            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                
                # Calcolo Occhio Destro Persona (Screen Left)
                rx, ry, r_iris_coords = self.get_eye_gaze_stats(
                    landmarks, self.RIGHT_CORNERS, self.RIGHT_IRIS, frame.shape
                )
                
                # Calcolo Occhio Sinistro Persona (Screen Right)
                lx, ly, l_iris_coords = self.get_eye_gaze_stats(
                    landmarks, self.LEFT_CORNERS, self.LEFT_IRIS, frame.shape
                )

                # --- MEDIA DEI DUE OCCHI (RAW) ---
                raw_avg_x = (rx + lx) / 2
                raw_avg_y = (ry + ly) / 2

                # --- GESTIONE CALIBRAZIONE ---
                if not self.is_calibrated:
                    # Accumula dati per la calibrazione
                    self.calibration_buffer_x.append(raw_avg_x)
                    self.calibration_buffer_y.append(raw_avg_y)
                    
                    # Feedback visivo durante calibrazione
                    progresso = len(self.calibration_buffer_x)
                    cv2.putText(frame, "CALIBRAZIONE: GUARDA AL CENTRO", (50, h//2 - 20), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    # Barra di progresso
                    cv2.rectangle(frame, (50, h//2 + 10), (50 + progresso * 4, h//2 + 30), (0, 255, 0), -1)
                    cv2.rectangle(frame, (50, h//2 + 10), (50 + self.CALIBRATION_FRAMES * 4, h//2 + 30), (255, 255, 255), 2)

                    if len(self.calibration_buffer_x) >= self.CALIBRATION_FRAMES:
                        # Calcolo offset: quanto dista il centro reale dell'utente da 0.5?
                        avg_center_x = np.mean(self.calibration_buffer_x)
                        avg_center_y = np.mean(self.calibration_buffer_y)
                        
                        # Se l'utente guarda al centro e legge 0.6, l'offset è +0.1
                        # Noi vogliamo sottrarre questo offset ai futuri calcoli per riportare 0.6 a 0.5
                        self.center_offset_x = avg_center_x - 0.5
                        self.center_offset_y = avg_center_y - 0.5
                        
                        self.is_calibrated = True
                        print(f"Calibrazione completata. Offset X: {self.center_offset_x:.3f}, Offset Y: {self.center_offset_y:.3f}")
                    
                    # Non salviamo dati durante la calibrazione per non sporcare i grafici
                    final_x, final_y = 0.5, 0.5
                    direction_text = "Calibrazione..."

                else:
                    # --- APPLICAZIONE CALIBRAZIONE ---
                    # Sottraiamo l'offset per centrare i dati su 0.5
                    final_x = raw_avg_x - self.center_offset_x
                    final_y = raw_avg_y - self.center_offset_y
                    
                    # Clamp per sicurezza tra 0 e 1
                    final_x = max(0.0, min(1.0, final_x))
                    final_y = max(0.0, min(1.0, final_y))
                    
                    # Salvataggio dati calibrati
                    self.history_x.append(final_x)
                    self.history_y.append(final_y)
                    self.frame_indices.append(self.frame_count)
                    self.frame_count += 1

                    direction_text = self.determine_direction(final_x, final_y)
                    
                    # Feedback Calibrazione OK
                    cv2.putText(frame, "Calibrazione OK", (10, h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                # --- Visualizzazione ---
                # Disegna iridi
                cv2.circle(frame, (int(r_iris_coords[0]), int(r_iris_coords[1])), 3, (0, 255, 0), -1)
                cv2.circle(frame, (int(l_iris_coords[0]), int(l_iris_coords[1])), 3, (0, 255, 0), -1)
                
                # Disegna box contorno occhi per feedback visivo
                mesh_points = np.array([np.multiply([p.x, p.y], [w, h]).astype(int) for p in landmarks])
                cv2.polylines(frame, [mesh_points[self.RIGHT_EYE_INDICES]], True, (200, 200, 200), 1, cv2.LINE_AA)
                cv2.polylines(frame, [mesh_points[self.LEFT_EYE_INDICES]], True, (200, 200, 200), 1, cv2.LINE_AA)

                # Info a schermo
                cv2.putText(frame, f"Sguardo: {direction_text}", (30, 50), 
                           cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 2)
                
                # Debug dati (Mostra dati calibrati se disponibile)
                if self.is_calibrated:
                     cv2.putText(frame, f"X: {final_x:.2f} | Y: {final_y:.2f}", (30, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 255, 50), 1)

            cv2.imshow('Gaze Tracking - Both Eyes', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.save_plots()

if __name__ == "__main__":
    tracker = EyeGazeTracker()
    tracker.run()