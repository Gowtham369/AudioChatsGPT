import tkinter as tk
from tkinter import ttk
import threading
import requests
import json
from audio_recorder import AudioRecorder
import time

class App:
    def __init__(self, root):
        self.audio_recorder = AudioRecorder()

        self.start_pause_button = ttk.Button(root, text="Start", command=self.start_pause)
        self.start_pause_button.grid(column=0, row=0, padx=10, pady=10)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop)
        self.stop_button.grid(column=1, row=0, padx=10, pady=10)

        self.transcription_label = ttk.Label(root, text="Transcription:")
        self.transcription_label.grid(column=0, row=1, padx=10, pady=10, sticky="w")

        self.transcription_text = tk.Text(root, wrap="word", width=40, height=10)
        self.transcription_text.grid(column=0, row=2, padx=10, pady=10, columnspan=2)

    def start_pause(self):
        if not self.audio_recorder.recording:
            self.audio_recorder.start_recording()
            self.start_pause_button.config(text="Pause")
        else:
            self.audio_recorder.pause_recording()
            if self.audio_recorder.pausing:
                self.start_pause_button.config(text="Resume")
            else:
                self.start_pause_button.config(text="Pause")
        if not self.audio_recorder.recording and not self.audio_recorder.pausing:
            self.start_pause_button.config(text="Start")

    def stop(self):
        self.audio_recorder.stop_recording()
        self.start_pause_button.config(text="Start")
        self.transcribe_audio()

    def transcribe_audio(self):
        self.transcription_text.delete(1.0, tk.END)
        self.transcription_text.insert(tk.END, "Transcribing...")

        def transcribe():
            audio_stream = self.audio_recorder.record_audio()
            while True:
                data = next(audio_stream)
                response = requests.post(
                    "https://speech.googleapis.com/v1/speech:transcribe",
                    headers={
                        "Authorization": "Bearer AIzaSyBCnqH-zz-orwJhXbk1-SEqEaepLf83v8E",
                        "Content-Type": "audio/x-raw,format=S16LE,channels=1,rate=16000",
                    },
                    body=data,
                )
                print("Sending Transcribe Request")
                transcript_id = response.json()["id"]

                while True:
                    response = requests.get(
                        f"https://speech.googleapis.com/v1/speech:transcript/{transcript_id}",
                        headers={
                            "Authorization": "Bearer AIzaSyBCnqH-zz-orwJhXbk1-SEqEaepLf83v8E",
                        },
                    )
                    print("Trying to get Transcribe Request Status",response.json()["status"])
                    transcript_status = response.json()["status"]
                    if transcript_status == "completed":
                        break
                    time.sleep(5)

                transcript_text = response.json()["results"][0]["alternatives"][0]["transcript"]
                self.transcription_text.delete(1.0, tk.END)
                self.transcription_text.insert(tk.END, transcript_text)

        threading.Thread(target=transcribe).start()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Audio Recorder")
    app = App(root)
    root.mainloop()
