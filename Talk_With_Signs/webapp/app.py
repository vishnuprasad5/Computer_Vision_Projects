from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import time
from gtts import gTTS
import pygame

app = Flask(__name__, template_folder='templates')

# Setting random seed
tf.random.set_seed(42)
np.random.seed(42)

# Loading model
loaded_model = tf.keras.models.load_model('../model/hand_signals_model.keras')

tts_language = 'en'

# Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Connection to the camera
cap = cv2.VideoCapture(0)

# Flag to control camera loop
camera_active = True

# MinMaxScaler
scaler = MinMaxScaler()

# Variables to store the recognized signs for the current word
current_word = []
previous_sign = None
word_separator = ''

# Initialize sentence variables
current_sentence = ""
sentence_separator = " "

current_word = ""
process_predictions = False


def generate_frames():
    global current_word
    last_input_letter = None
    global current_sentence

    while camera_active:
        ret, frame = cap.read()

        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        predicted_letter = predict_letters(results, frame)

        if predicted_letter is not None:
            current_word, word_completed = create_words(predicted_letter, current_word, last_input_letter)

            if word_completed:
                words = current_word.split()

                last_word = words[-1]

                if last_word == '.':
                    print("Dot detected. ")
                else:
                    play_text_speech(last_word)

            last_input_letter = predicted_letter

            yield f"data: {current_word}\n\n"

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


capture_interval = 2
capture_time = time.time() + 0.99

def predict_letters(results, frame):
    global capture_time

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())


    if time.time() >= capture_time:
        capture_time += capture_interval

        if process_predictions and results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                hand_landmarks = [(landmark.x, landmark.y) for landmark in landmarks.landmark]
                normalized_hand_landmarks = scaler.fit_transform(hand_landmarks)
                normalized_hand_landmarks_flat = np.array(normalized_hand_landmarks).flatten()
                normalized_hand_landmarks_flat = normalized_hand_landmarks_flat.reshape(1, -1)

                class_label = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
                               10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
                               19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'EOW', 27: 'EOS'}

                prediction = loaded_model.predict(normalized_hand_landmarks_flat)
                predicted_class = class_label[np.argmax(prediction)]

                return predicted_class

    return None


def create_words(input_letter, current_word, last_input_letter=None):
    word_completed = False
    dot_added = False

    if input_letter.upper() == 'EOW':
        if last_input_letter and last_input_letter.upper() == 'EOW':
            return current_word, word_completed
        else:
            word_completed = True
            return current_word + ' ', word_completed
    elif input_letter.upper() == 'EOS':
        if not dot_added:
            current_word += '. '
            dot_added = True

        word_completed = True
        return current_word, word_completed
    elif input_letter != last_input_letter:
        dot_added = False
        return current_word + input_letter, word_completed
    else:
        return current_word, word_completed


def play_text_speech(text):
    tts = gTTS(text, lang=tts_language, slow=False)
    tts.save('output.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('output.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

@app.route('/current_word')
def get_current_word():
    global current_word
    return Response(f"data: {current_word}\n\n", content_type="text/event-stream")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_predictions')
def start_predictions():
    global process_predictions
    process_predictions = True
    return jsonify(success=True)

@app.route('/pause_predictions')
def pause_predictions():
    global process_predictions
    process_predictions = False
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)

