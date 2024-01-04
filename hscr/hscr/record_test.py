import numpy as np
import wave
import pyaudio
import sys
import time
 
class Record:
    def __init__(self, chunksize=1024, nchannels=1, fs=44100):
        self.CHUNK = chunksize
        self.FORMAT = pyaudio.paInt16
        self.NCHANNELS = nchannels
        self.RATE = fs
        self.rec_sig = []
        self.command = None
        self.p = pyaudio.PyAudio()
 
    def __del__(self):
        self.p.terminate()
 
    def callback(self, in_data, frame_count, time_info, status_flags):
        self.rec_sig.append(in_data)
        if self.command=="q":
            return None, pyaudio.paComplete
        return None, pyaudio.paContinue
 
    def recording(self, filename):
        stream = self.p.open(
            format=self.FORMAT,
            channels=self.NCHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.callback
            )

        stream.start_stream()
        
        while stream.is_active():
            a=input()
            self.command = input("&amp;gt;&amp;gt;")
            time.sleep(0.01)

        stream.stop_stream()
        stream.close()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.NCHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.rec_sig))
        wf.close()

def record_main():
    chunksize=1024
    nchannels=1
    fs=44100
    filename = "/home/suzuki/CASH/CASH_2023/src/hscr/output.wav"
    print("rec")
    rec = Record(chunksize, nchannels, fs)
    rec.recording(filename)

if __name__ ==  "__main__":
    record_main()