# Talk with Signs Project

## Overview

The "Talk with Signs" project is a real-time model that enables the creation and vocalization of words and sentences using hand signals. This innovative project is based on American Sign Language (ASL), where each sign represents a corresponding letter in the English alphabet. Additionally, two unique signs, EOW (End of Word) and EOS (End of Sentence), have been introduced to enhance the communication capabilities.

https://www.linkedin.com/posts/vishnu-prasad-447048261_talkwithsigns-computervision-innovation-activity-7155558352859623424-kWOd?utm_source=share&utm_medium=member_desktop

## Features

- **Real-time Word and Sentence Creation:** The model dynamically generates words and sentences based on hand signals captured in real-time.

- **ASL Integration:** Utilizes American Sign Language to represent each letter, allowing for a seamless transition from signs to written words.

- **Extended Signs:** Introduces EOW and EOS signs for improved sentence structure.

- **Speech Synthesis:** Integrates Google Text-to-Speech (gTTS) and Pygame for the audible representation of the created words.

- **Web Interface with Flask:** Implements a Flask web application to provide a user-friendly interface for interacting with the model.

## How it's Made

1. **Data Collection:**
   - Captured 100 images for each class using OpenCV, ensuring a diverse dataset.

2. **Data Augmentation:**
   - Applied the Image Data Generator to increase the dataset size and incorporate data augmentation techniques.

3. **Hand Landmarks Extraction:**
   - Utilized the Mediapipe library to extract hand landmarks, providing essential input features for the model.

4. **Model Creation:**
   - Developed a Keras model to interpret hand signals and generate corresponding words and sentences.

5. **Word Creation Functions:**
   - Implemented functions to facilitate the dynamic creation of words, considering the unique nature of ASL signs.

6. **Speech Output:**
   - Integrated gTTS for converting the created words into speech and Pygame for audio playback.

7. **Flask Web Application:**
   - Created a web interface using Flask to enhance user interaction with the model.

8. **Real-time Video Streaming:**
   - Implemented video streaming with Flask to visualize hand signals and the recognized words in real-time.

9. **Control Prediction Process:**
   - Implemented routes (`/start_predictions` and `/pause_predictions`) to control the prediction process.

## How to Use

1. **Installation:**
   - Clone the repository and install the required dependencies.

2. **Run the Flask App:**
   - Start the Flask web application to access the user interface.

3. **Interact with Signs:**
   - Use hand signals through the webcam to dynamically create words and sentences.

4. **Audio Output:**
   - Experience the audible representation of the created words through the integrated speech synthesis.

## Future Enhancements

- Incorporate a larger ASL vocabulary.
- Improve the design and user experience of the Flask web interface.
- Explore additional features for enhanced communication.

## Contributors

- Vishnu Prasad K P

Feel free to contribute, report issues, or provide feedback to make the "Talk with Signs" project even more impactful and accessible.
