import pyaudio
import wave
import time

class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.pausing = False
        self.stream = None

    def start_recording(self):
        self.recording = True
        self.pausing = False
        self.stream = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
        self.channels = 2
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.stream = self.stream.open(format=self.format,
                             channels=self.channels,
                             rate=self.rate,
                             input=True,
                             frames_per_buffer=self.frames_per_buffer)

    def pause_recording(self):
        self.pausing = not self.pausing

    def stop_recording(self):
        self.recording = False
        self.stream.stop_stream()
        self.stream.close()
        pyaudio.terminate()

    def record_audio(self):
        while self.recording:
            if not self.pausing:
                data = self.stream.read(self.frames_per_buffer)
                yield data

