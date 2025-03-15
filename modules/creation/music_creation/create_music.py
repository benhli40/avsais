import os
import wave
import numpy as np
import random
from pydub import AudioSegment
from pydub.playback import play

class MusicCreator:
    def __init__(self, sample_rate=44100, duration=5):
        self.sample_rate = sample_rate  # Standard audio sample rate
        self.duration = duration  # Duration in seconds
    
    def generate_sine_wave(self, frequency=440.0, amplitude=0.5):
        """Generates a sine wave with given frequency and amplitude."""
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), False)
        wave_data = amplitude * np.sin(2 * np.pi * frequency * t)
        return np.int16(wave_data * 32767)
    
    def generate_drum_beat(self):
        """Generates a simple drum beat pattern using percussion sounds."""
        drum_sounds = ["kick.wav", "snare.wav", "hihat.wav"]
        beat_pattern = [random.choice(drum_sounds) for _ in range(4)]
        drum_track = sum([AudioSegment.from_wav(sound) for sound in beat_pattern])
        return drum_track
    
    def generate_melody(self):
        """Generates a random melody using sine waves."""
        melody_notes = [random.choice([261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]) for _ in range(self.duration)]
        wave_data = np.concatenate([self.generate_sine_wave(f, 0.5) for f in melody_notes])
        return np.int16(wave_data * 32767)
    
    def save_wave_file(self, filename, wave_data):
        """Saves generated wave data to a .wav file."""
        with wave.open(filename, 'w') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes(wave_data.tobytes())
        print(f"✅ Music file saved as: {filename}")
    
    def play_audio(self, audio_data):
        """Plays the generated audio using pydub."""
        if isinstance(audio_data, np.ndarray):
            filename = "temp_output.wav"
            self.save_wave_file(filename, audio_data)
            audio_data = AudioSegment.from_wav(filename)
        play(audio_data)
    
    def create_music(self, option="sine", frequency=440.0, amplitude=0.5, filename="output.wav"):
        """Generates, saves, and plays a sine wave, drum beat, or melody."""
        if option == "sine":
            wave_data = self.generate_sine_wave(frequency, amplitude)
        elif option == "drum":
            wave_data = self.generate_drum_beat()
        elif option == "melody":
            wave_data = self.generate_melody()
        else:
            print("❌ Invalid option. Choose 'sine', 'drum', or 'melody'.")
            return
        
        self.save_wave_file(filename, wave_data) if isinstance(wave_data, np.ndarray) else wave_data.export(filename, format="wav")
        self.play_audio(wave_data)
    
if __name__ == "__main__":
    creator = MusicCreator()
    option = input("Choose music type (sine/drum/melody): ").strip().lower()
    
    if option == "sine":
        freq = float(input("Enter frequency (Hz): "))
        amp = float(input("Enter amplitude (0 to 1): "))
        filename = input("Enter filename (default: output.wav): ") or "output.wav"
        creator.create_music(option, freq, amp, filename)
    else:
        filename = input("Enter filename (default: output.wav): ") or "output.wav"
        creator.create_music(option, filename=filename)