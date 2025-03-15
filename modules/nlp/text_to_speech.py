import pyttsx3

class TextToSpeech:
    def __init__(self, rate=150, volume=1.0, voice=None):
        """
        Initializes the text-to-speech engine with adjustable rate, volume, and voice selection.
        """
        self.engine = pyttsx3.init()
        self.set_rate(rate)
        self.set_volume(volume)
        self.set_voice(voice)
    
    def set_rate(self, rate):
        """Sets the speed of speech."""
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume):
        """Sets the volume level (0.0 to 1.0)."""
        self.engine.setProperty('volume', max(0.0, min(volume, 1.0)))
    
    def set_voice(self, voice=None):
        """Sets the voice based on available system voices."""
        voices = self.engine.getProperty('voices')
        if voice:
            for v in voices:
                if voice.lower() in v.name.lower():
                    self.engine.setProperty('voice', v.id)
                    return
        # Default to first available voice
        self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text):
        """Converts text to speech and speaks it aloud."""
        self.engine.say(text)
        self.engine.runAndWait()
    
if __name__ == "__main__":
    tts = TextToSpeech(rate=160, volume=1.0, voice="David")  # Adjust voice if needed
    
    sample_texts = [
        "Hello! How can I assist you today?",
        "The weather is sunny and 75 degrees.",
        "Your next appointment is at 3 PM.",
        "Goodbye! Have a great day!"
    ]
    
    for text in sample_texts:
        print(f"Speaking: {text}")
        tts.speak(text)