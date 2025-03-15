import speech_recognition as sr
import time
from intent_recognizer import IntentRecognizer
from response_generator import ResponseGenerator

class SpeechRecognizer:
    def __init__(self, recognition_engine="google"):
        self.recognizer = sr.Recognizer()
        self.intent_recognizer = IntentRecognizer()
        self.response_generator = ResponseGenerator()
        self.recognition_engine = recognition_engine  # Default to Google Speech Recognition
    
    def recognize_speech(self):
        """
        Captures audio from the microphone and converts it to text.
        Recognized speech is processed for intent recognition and response generation.
        """
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.process_audio(audio)
                
                if text:
                    print(f"Recognized: {text}")
                    intent = self.intent_recognizer.recognize_intent(text)
                    response = self.response_generator.generate_response(intent)
                    print(f"Response: {response}")
                    return response
                else:
                    return "I didn't catch that. Can you repeat?"
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand that."
            except sr.RequestError:
                return "Speech recognition service is unavailable."
            except sr.WaitTimeoutError:
                return "No speech detected. Please try again."
    
    def process_audio(self, audio):
        """
        Processes the audio using the selected recognition engine.
        """
        if self.recognition_engine == "google":
            try:
                return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                return None
        elif self.recognition_engine == "sphinx":  # Offline alternative
            try:
                return self.recognizer.recognize_sphinx(audio)
            except sr.UnknownValueError:
                return None
        return None

if __name__ == "__main__":
    recognizer = SpeechRecognizer()
    
    while True:
        print("Say something:")
        response = recognizer.recognize_speech()
        print(response)
        time.sleep(1)  # Short delay before listening again