import rclpy                         # ROS2のPythonモジュール
from rclpy.node import Node          # rclpy.nodeモジュールからNodeクラスをインポート
from std_msgs.msg import String      # std_msgs.msgモジュールからStringクラスをインポート


class HscrPub(Node):  # "Happy World"とパブリッシュ並びに表示するクラス
    def __init__(self):  # コンストラクタ
        super().__init__('HSCR_Robot_pub_node')
        self.pub = self.create_publisher(String, 'topic', 10)   # パブリッシャの生成
        self.create_timer(1.0, self.callback)

    def callback(self):  # コールバック関数
        msg = String()
        msg.data = input()
        self.pub.publish(msg)
        self.get_logger().info(f'パブリッシュ: {msg.data}')


def main(args=None):  # main関数
    rclpy.init()
    node = HscrPub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()