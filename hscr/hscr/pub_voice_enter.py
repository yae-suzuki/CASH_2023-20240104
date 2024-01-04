import rclpy                         # ROS2のPythonモジュール
from rclpy.node import Node          # rclpy.nodeモジュールからNodeクラスをインポート
from std_msgs.msg import String      # std_msgs.msgモジュールからStringクラスをインポート
import numpy as np
import sounddevice as sd
import threading
import time
from scipy.io.wavfile import write
import openai
from .record_test import record_main

class HscrPub(Node):  # "Happy World"とパブリッシュ並びに表示するクラス
    def __init__(self):  # コンストラクタ
        super().__init__('HSCR_Robot_pub_node')
        self.pub = self.create_publisher(String, 'topic', 10)   # パブリッシャの生成
        self.create_timer(1.0, self.callback)

    def callback(self):  # コールバック関数
        print("callback")
        record_main()

def main(args=None):  # main関数
    rclpy.init()
    node = HscrPub()
    # OpenAIのAPIキーを設定
    openai.api_key = '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'
    try:
        rclpy.spin_once(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()