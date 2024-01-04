import rclpy
import openai
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import datetime
from sensor_msgs.msg import Image
import time
import requests
from playsound import playsound
import requests
from playsound import playsound

#from timeout_decorator import timeout, TimeoutError


# Sring型メッセージをサブスクライブして端末に表示するだけの簡単なクラス
class HscrSub(Node):
    def __init__(self): # コンストラクタ
        super().__init__('HSCR_Robot_sub_node')
        # サブスクライバの生成
        self.sub = self.create_subscription(String,'topic', self.callback, 10)#topicっていう名前の箱のサブスクライブ、Stringは形　受け取る
        self.publisher = self.create_publisher(Image,'result',10)#大事！resultっていう名前の箱にパブリッシュしてる。送ってる。rqtは通信を見えるようにする。動画をresultに送ってrqtでみてる。

    def callback(self, msg):  # コールバック関数 送られたときに起動
        self.get_logger().info(f'サブスクライブ: {msg.data}')
        path = '/home/suzuki/CASH/CASH_2023/src/hscr/hscr/enter_voice_word.txt'
        f = open(path)
        text = f.read()
        f.close()
        # OpenAIのAPIキーを設定
        openai.api_key = ''

        # テンプレートの準備
        template = """あなたは猫のキャラクターとして振る舞うチャットボットです。
        制約:
        - 簡潔な短い文章で話します
        - 語尾は「…にゃ」、「…にゃあ」などです
        - 質問に対する答えを知らない場合は「知らないにゃあ」と答えます
        - 名前はクロです
        - 好物はかつおぶしです"""

        # メッセージの初期化
        messages = [
            {
            "role": "system",
            "content": template
            }
        ]

        # ユーザーからのメッセージを受け取り、それに対する応答を生成
        #while True:
        user_message = text
        print("あなたのメッセージ: \n{}".format(user_message))
        messages.append({
        "role": "user",
        "content": user_message
        })
        #GPTによる回答の生成
        response_answer = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
        bot_message = response_answer['choices'][0]['message']['content']
        print("チャットボットの回答: \n{}".format(bot_message))
        
        messages_emotional_judgement= [
            {
            "role": "system",
            "content": template
            }
        ]
        
        ##メッセージから気分の判定を行う
        #メッセージの格納
        emotional_judgment = " ' " + text + " 'このメッセージを以下のステータスルールで表してください。喜び:0~5,怒り:0~5,悲しい:0~5,楽しい:0~5 "
        print(emotional_judgment)
        #emotional_judgment.join(text)
        #emotional_judgment.join("'このメッセージを以下のステータスルールで表してください。　楽しい:0~5,悲しい:0~5,怒り:0~5")
        
        messages_emotional_judgement.append({
        "role": "user",
        "content": emotional_judgment
        })

        response_emotional_judgment = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages_emotional_judgement
        )

        #print("チャットボットへの送信メッセージ: \n{}".format(emotional_judgment))
        bot_message_emotional_judgement = response_emotional_judgment['choices'][0]['message']['content']
        print("チャットボットの回答: \n{}".format(bot_message_emotional_judgement))

        ##GPTの点数回答を抽出
        #変数定義
        joy,anger,sad,fun = 0,0,0,0
        target_emottion = []
        #回答を格納
        char=bot_message_emotional_judgement
        #格納した回答から"チャットボットの回答:"の文言を削除する
        char = char.replace('チャットボットの回答：','')
        print("char入力文字",char)

        #GPTの回答を変数に格納
        for n_char in range(4):
            char_num = ["喜び","怒り","悲しい","楽しい"]
            print(char_num[n_char])
            target = char_num[n_char]+': '
            idx_1 = char.find(target)
            r1 = char[idx_1+len(target):]
            target = ','
            idx_2 = r1.find(target)
            r2 = r1[:idx_2]
            target_emottion.append(r2)

        #それぞれの感情の点数を関数に代入
        joy,anger,sad,fun = target_emottion
        joy,anger,sad,fun = int(joy),int(anger),int(sad),int(fun)

        ##テキストを音声に変換して再生
        # VOICEVOX EngineのURL
        VOICEVOX_URL = "http://localhost:50021"

        # 音声合成のためのクエリを生成
        response_answer = requests.post(
        f"{VOICEVOX_URL}/audio_query",
        params={
                "text": bot_message,
                "speaker": 58,
                },
            )

        audio_query = response_answer.json()

    # 音声合成を行う
        response_answer = requests.post(
            f"{VOICEVOX_URL}/synthesis",
        headers={
            "Content-Type": "application/json",
        },
        params={
            "speaker": 58,
        },
        json=audio_query,
            )

        # ステータスコードが200以外の場合はエラーメッセージを表示
        if response_answer.status_code != 200:
            print("エラーが発生しました。ステータスコード: {}".format(response_answer.status_code))
            print(response_answer.text)
        else:
    # 音声データを取得
            audio = response_answer.content
    # 音声データをファイルに保存
            with open("output.wav", "wb") as f:
                f.write(audio)
    # 音声データを再生
            playsound("output.wav")

            messages.append({
            "role": "assistant",
            "content": bot_message
            })

def main(args=None): # main¢p
    try:
        rclpy.init()#初期化
        node = HscrSub()#nodeにHscrを
        msg=String()#stringは文字列いれれる
        while True:
            rclpy.spin(node)#一回ノードを起動する？
    except KeyboardInterrupt:
        pass#ctl+C(KeyboardInterrupt) node finish
