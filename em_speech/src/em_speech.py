#!/usr/bin/env python
# -*- coding: utf-8 -*-

#tmc_talk_hoya_py: https://docs.hsr.io/manual/reference/packages/tmc_talk_hoya_py/PKGDOC.html#python

import rospy
from std_msgs.msg import String
from tmc_msgs.msg import Voice

#pythonライブラリをimportできないため、トピックで発話させている
#import tmc_talk_hoya_py

class Speech(object):

    def EnSpeechCallback(self, msg):
        #self.en_speaker.speak(msg.data)
        self.speech.language = 1
        self.speech.sentence = msg.data
        self.speech_pub.publish(self.speech)
        print 'HSR said "%s"' % msg.data

    def JaSpeechCallback(self, msg):
        #self.ja_speaker.speak(msg.data)
        self.speech.language = 0
        self.speech.sentence = msg.data
        self.speech_pub.publish(self.speech)
        print 'HSR said "%s"' % msg.data

    def __init__(self):
        #self.en_speaker = tmc_talk_hoya_py.VoiceTextSpeaker(voice='julie')
        #self.ja_speaker = tmc_talk_hoya_py.VoiceTextSpeaker(voice='haruka')

        rospy.Subscriber("/hsr/text2speech/en", String, self.EnSpeechCallback)
        rospy.Subscriber("/hsr/text2speech/ja", String, self.JaSpeechCallback)

        self.speech_pub = rospy.Publisher("/talk_request", Voice, queue_size=1)
        self.speech = Voice()
        self.speech.interrupting = False
        self.speech.queueing = False

if __name__ == '__main__':
    rospy.init_node('em_speech', anonymous=True)
    msg = Speech()
    rospy.spin()
