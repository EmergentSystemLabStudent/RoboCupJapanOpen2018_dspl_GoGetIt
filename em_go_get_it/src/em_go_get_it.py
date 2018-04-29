#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped
import actionlib
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import random

class Go_Get_It(object):

    #actionでゴールを与える
    def ReturnMove(self):
        cli = actionlib.SimpleActionClient('/move_base/move', MoveBaseAction)
        cli.wait_for_server()
        self.start_pos.header.stamp = rospy.Time.now()
        self.start_pos.header.frame_id = "map"
        goal = MoveBaseGoal()
        goal.target_pose = self.start_pos
        cli.send_goal(goal)
        cli.wait_for_result()
        action_state = cli.get_state()
        if action_state == GoalStatus.SUCCEEDED:
            rospy.loginfo("Navigation Succeeded.")
            if self.test_count == 1:
                self.Text2Speech("I arrive at start position and can start test phase..")
            elif self.test_count >= 2:
                self.Text2Speech("Please give me the next command.")


    #音声認識結果の処理をする
    def Speech2TextCallback(self, msg):
        text = msg.data
        print '\tYou said "%s"' % text

        #小文字に変換
        text = text.lower()

        #ピリオド除去
        text = text.replace(".", "")

        #誤認識処理
        text = text.replace("for me", "follow me")





        #未知な場所の名前を既知な名前に変換
        text = text.replace("", "")





        self.Speech2Text(text)


    #誤認識処理済みの音声認識結果
    def Speech2Text(self, text):
        print '\t=======> "%s"' % text

        #Traning PhaseのFollow me
        if self.follow_me == True:
            #Follow me開始
            if text.find("follow") != -1:
                self.follow_me_pub.publish(True)
                self.Text2Speech("I'm following you.")
                self.training = True
            #Follow me一時停止
            elif text.find("stop") != -1:
                self.follow_me_pub.publish(False)
                self.Text2Speech("I stop following you.")

        #Traning Phaseの場所概念学習
        if self.training == True:
            #Test Phaseの開始位置を記憶
            if text.find("start") != -1 or text.find("position") != -1:
                self.start_pos = self.current_pos
                self.Text2Speech("OK, I remember.")
            #教示された場所の名前をオペレータに確認する発話
            elif text.find("here is ") != -1:
                self.vocab = text.replace("here is ", "")
                self.Text2Speech("Here is " + self.vocab + "? Yes or No.")
                self.check_vocab = True
            #教示した場所の名前が正しい
            elif text.find("yes") != -1 and self.check_vocab == True:
                self.vocab_list.append(self.vocab)
                self.spco_vocab_pub.publish(self.vocab)
                self.Text2Speech("OK, I remember " + self.vocab + ".")
                self.check_vocab = False
            #教示した場所の名前が間違っている
            elif text.find("no") != -1 and self.check_vocab == True:
                self.Text2Speech("Please say one more time.")
                self.check_vocab = False
            #学習を開始
            elif text.find("finish") != -1:
                self.spco_finish_pub.publish(1)
                #self.Text2Speech("I'm learning spatial concept now.")
            #Follow me終了、Test Phaseの開始位置に移動
            elif text.find("return") != -1:
                self.training = False
                self.test = True
                self.follow_me_pub.publish(False)
                self.follow_me = False
                self.Text2Speech("I return to start position.")
                self.ReturnMove()

        #Test Phase
        elif self.test == True:
            if text.find("bring me") != -1:
                self.vocab_pub = False
                for i in range(len(self.vocab_list)):
                    #場所の名前リストにあれば、その場所に移動する
                    if text.find(self.vocab_list[i]) != -1:
                        self.spco_name = self.vocab_list[i]
                        self.Text2Speech("I go to " + self.spco_name + " .")
                        self.spco_name_pub.publish(self.spco_name)
                        self.vocab_pub = True
                        break
                #場所の名前リストになければ（ランダムに）ひとつずつ選んで、ここでいいかYes or Noで聞き返す
                if self.vocab_pub == False:
                    self.random_list = random.sample(self.vocab_list, len(self.vocab_list))
                    self.Text2Speech("Can I go to " + self.random_list[self.check_place] + " ? Yes or No.")
                    self.check_place += 1
            #Yes or No
            elif self.check_place > 0:
                if text.find("yes") != -1:
                    self.spco_name = self.random_list[self.check_place]
                    self.check_place = 0
                    self.Text2Speech("I go to " + self.spco_name + " .")
                    self.spco_name_pub.publish(self.spco_name)
                elif text.find("no") != -1:
                    self.check_place += 1
                    self.Text2Speech("Can I go to " + self.random_list[self.check_place] + " ? Yes or No.")


    #HSR発話（英語）
    def Text2Speech(self, text):
        print '\tHSR said "%s"' % text
        msg = String()
        msg.data = text
        self.hsr_en_pub.publish(msg)

    #ヘッドセットで再生(日本語)
    def HeadSetPlayJa(self, text):
        print '\trospeex said "%s"' % text
        msg = String()
        msg.data = text
        self.inner_ja_pub.publish(msg)

    #ヘッドセットで再生(英語)
    def HeadSetPlayEn(self, text):
        print '\trospeex said "%s"' % text
        msg = String()
        msg.data = text
        self.inner_en_pub.publish(msg)

    #ActiveSLAM開始
    def ActiveStartCallback(self, msg):
        if msg.data == True:
            self.Text2Speech("Start generating the map.")

    #ActiveSLAM終了
    def ActiveFinishCallback(self, msg):
        if msg.data == True:
            self.slam_finish = True

    #ActiveSLAM終了後、原点に戻った
    def ActiveGoalCallback(self, msg):
        if msg.data == True and self.slam_finish == True:
            self.Text2Speech("Finish generating the map.")
            self.HeadSetPlayJa("地図生成終わったよ")
            self.follow_me = True

    #Test Phaseで物体の場所まで移動完了、start positionまで戻る
    def SpcoGoalCallback(self, msg):
        #Test Phaseで物体の場所まで移動完了、start positionまで戻る
        if msg.data == True and self.test == True:
            self.Text2Speech("I cannot take object, so I return to start position.")
            self.test_count += 1
            self.ReturnMove()
        #Test Phaseで移動失敗、再度移動命令を出す
        elif mag.data == False and self.test == True:
            self.spco_name_pub.publish(self.spco_name)

    #自己位置を取得
    def GlobalPoseCallback(self, msg):
        self.current_pos.pose = msg.pose

    #場所概念学習終了
    def LearnedCallback(self, msg):
        if msg.data == True:
            self.Text2Speech("I finish learning spatial concept.")

    def __init__(self):
        self.slam_finish = False
        self.follow_me = False
        self.training = False
        self.vocab_list = []
        self.check_vocab = False
        self.test = False
        self.vocab_pub = False
        self.check_place = 0
        self.test_count = 1
        self.start_pos = PoseStamped()
        self.current_pos = PoseStamped()

        self.hsr_en_pub = rospy.Publisher("/hsr/text2speech/en", String, queue_size=1)
        self.inner_en_pub = rospy.Publisher("/rospeex/text2speech/en", String, queue_size=1)
        self.inner_ja_pub = rospy.Publisher("/rospeex/text2speech/ja", String, queue_size=1)
        self.follow_me_pub = rospy.Publisher("/em/follow_me", Bool, queue_size=1)
        self.spco_finish_pub = rospy.Publisher("/em/spco_formation/finish", Int32, queue_size=1)
        self.spco_vocab_pub = rospy.Publisher("/em/spco_formation/vocab", String, queue_size=1)
        self.spco_name_pub = rospy.Publisher("/em/spco/name_sub", String, queue_size=1)

        rospy.Subscriber("/rospeex/speech2text/en", String, self.Speech2TextCallback)
        rospy.Subscriber("/active/start", Bool, self.ActiveStartCallback)
        rospy.Subscriber("/active/finish", Bool, self.ActiveFinishCallback)
        rospy.Subscriber("/goal/flag", Bool, self.ActiveGoalCallback)
        rospy.Subscriber("/spco/goal/flag", Bool, self.SpcoGoalCallback)
        rospy.Subscriber("/global_pose", PoseStamped, self.GlobalPoseCallback)
        rospy.Subscriber("/em/spco_formation/learned", Bool, self.LearnedCallback)

if __name__ == '__main__':
    rospy.init_node('em_go_get_it_main', anonymous=True)
    msg = Go_Get_It()
    rospy.spin()
