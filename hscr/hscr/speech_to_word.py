import sounddevice as sd
from scipy.io.wavfile import write
import openai
import numpy as np
import threading
import time

def speech_to_word_main(fs):

    recording = np.array([])  #録音データを保存する配列
    is_recording = False #録音の開始と終了を制御するフラグ

    def record():
        """録音を行う関数"""
        global is_recording
        global recording
        while True:
            if is_recording:
                # 録音中の場合、0.5秒分の録音データを追加
                recording_chunk = sd.rec(int(0.5 * fs), samplerate=fs, channels=1)
                sd.wait()
                recording = np.append(recording, recording_chunk)
            else:
                # CPU負荷を下げるために1ミリ秒待機
                time.sleep(0.001)

    print("record thread start")
    # 録音スレッドの開始
    recording_thread = threading.Thread(target=record)
    recording_thread.start()

    def speech_to_text():
        """音声認識を行う関数"""
        global is_recording
        global recording
        input("Enterキーを押すと録音を開始します。\n")
        # 録音を開始
        is_recording = True
        print("録音を開始します。\n")
        input("録音中です。Enterを押すと録音を終了します。\n")
        # 録音を終了
        is_recording = False
        print("録音が終了しました。")

        if recording.size > 0:
            # 録音データが存在する場合、データをファイルに保存
            write('output.wav', fs, recording)

            # ファイルをバイナリモードで開く
            with open('output.wav', "rb") as audio_file:
                # Whisper APIを使用してオーディオファイルをテキストに変換
                transcript = openai.Audio.transcribe("whisper-1", audio_file)

            # 録音データをリセット
            recording = np.array([])

            # 音声からテキスト変換した結果を返す
            return transcript.text

    text = speech_to_text()
    f = open('/home/suzuki/CASH/CASH_2023/src/hscr/hscr/enter_voice_word.txt', 'w')
    f.write(text)
    print("\n音声認識結果: {}\n".format(text))

if __name__ == '__main__':
    # OpenAIのAPIキーを設定
    openai.api_key = ''

    # 録音のパラメータ
    fs = 44100  # サンプルレート
    recording = np.array([])  # 録音データを保存する配列

    # 録音の開始と終了を制御するフラグ
    is_recording = False
    speech_to_word_main(fs)
