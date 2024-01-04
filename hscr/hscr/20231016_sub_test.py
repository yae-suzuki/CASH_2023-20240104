import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import datetime
from sensor_msgs.msg import Image
import time
#from timeout_decorator import timeout, TimeoutError


# Sring型メッセージをサブスクライブして端末に表示するだけの簡単なクラス
class HscrSub(Node):
    def __init__(self):  # コンストラクタ
        super().__init__('HSCR_Robot_sub_node')
        # サブスクライバの生成
        self.sub = self.create_subscription(String,'topic', self.callback, 10)
        self.publisher = self.create_publisher(Image,'result',10)

    def callback(self, msg):  # コールバック関数
        self.get_logger().info(f'サブスクライブ: {msg.data}')
    
    def movie_start(self):
        msg = String()
        
        br = CvBridge()
        cap0 =  cv2.VideoCapture(r"/home/suzuki/CASH/CASH_2023/src/hscr/hscr/movie/sample_movie.mp4")
        while True:
            ret1, frame1 = cap0.read()
            if ret1:               
                frame1 = cv2.resize(frame1, (1920, 1080))
                movie1_br =br.cv2_to_imgmsg(frame1,'bgr8')
                self.publisher.publish(movie1_br)
                cv2.waitKey(10)
            else:
                cap0.set(cv2.CAP_PROP_POS_FRAMES, 0)
                break
        
        print("end")


def main(args=None):  # main¢p
    try:
        rclpy.init()
        node = HscrSub()
        msg=String()      
        while True:           
            rclpy.spin_once(node)
            node.movie_start()
    except KeyboardInterrupt:
        pass    #ctl+C(KeyboardInterrupt) node finish

    """
    while True:       
        if msg.data==True:
            
            i = i+1
            print(i)
        else:
            print("wait_time")
            time.sleep(1)
    """
    
    """
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('Ctrl+Cが押されました')
    finally:
        rclpy.shutdown()
    """