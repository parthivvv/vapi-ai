import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import speech_recognition as sr
from audio.capture import record_audio
from audio.play import play_audio
from utils.openai_api import transcribe_audio, generate_response, text_to_speech

class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.listening = False
        self.context = []

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.start_button = tk.Button(root, text="Start Listening", command=self.start_listening)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.stop_button = tk.Button(root, text="Stop Listening", command=self.stop_listening)
        self.stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def start_listening(self):
        self.listening = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.listen_thread = Thread(target=self.listen)
        self.listen_thread.start()

    def stop_listening(self):
        self.listening = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def listen(self):
        with self.microphone as source:
            while self.listening:
                audio = self.recognizer.listen(source)
                self.process_audio(audio)

    def process_audio(self, audio):
        try:
            text = self.recognizer.recognize_google(audio)
            self.context.append({"role": "user", "content": text})
            self.text_area.insert(tk.END, f"You: {text}\n")
            self.generate_response(text)
        except sr.UnknownValueError:
            self.text_area.insert(tk.END, "Sorry, I didn't catch that.\n")
        except sr.RequestError as e:
            self.text_area.insert(tk.END, f"Could not request results; {e}\n")

    def generate_response(self, prompt):
        response_text = generate_response(prompt)
        self.context.append({"role": "assistant", "content": response_text})
        self.text_area.insert(tk.END, f"Assistant: {response_text}\n")

        response_audio_path = "response.wav"
        text_to_speech(response_text, response_audio_path)
        play_audio(response_audio_path)

def main():
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
