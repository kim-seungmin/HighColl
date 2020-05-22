# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
import moviepy.video

import sys
import time
import re
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 334)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(310, 280, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(60, 40, 261, 216))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.LE1 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.LE1.setObjectName("LE1")
        self.horizontalLayout.addWidget(self.LE1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.LE2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.LE2.setObjectName("LE2")
        self.horizontalLayout_3.addWidget(self.LE2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.CB = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.CB.setObjectName("CB")
        self.CB.addItem("")
        self.CB.addItem("")
        self.CB.addItem("")
        self.verticalLayout.addWidget(self.CB)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.LE3 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.LE3.setObjectName("LE3")
        self.horizontalLayout_2.addWidget(self.LE3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.RB1 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.RB1.setObjectName("RB1")
        self.verticalLayout.addWidget(self.RB1)
        self.RB2 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.RB2.setObjectName("RB2")
        self.verticalLayout.addWidget(self.RB2)
        self.RB3 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.RB3.setObjectName("RB3")
        self.verticalLayout.addWidget(self.RB3)
        self.RB4 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.RB4.setObjectName("RB4")
        self.verticalLayout.addWidget(self.RB4)
        self.RB5 = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.RB5.setObjectName("RB5")
        self.verticalLayout.addWidget(self.RB5)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "HighColl"))
        self.pushButton.setText(_translate("Dialog", "실행"))
        self.pushButton.clicked.connect(self.asd)
        self.label.setText(_translate("Dialog", "id:"))
        self.label_3.setText(_translate("Dialog", "영상수(최대20):"))
        self.CB.setItemText(0, _translate("Dialog", "모든 카테고리"))
        self.CB.setItemText(1, _translate("Dialog", "해당 카테고리만"))
        self.CB.setItemText(2, _translate("Dialog", "해당 카테고리 제외"))
        self.label_2.setText(_translate("Dialog", "카테고리:"))
        self.RB1.setText(_translate("Dialog", "영상합치기"))
        self.RB2.setText(_translate("Dialog", "오름차순(10~1위)"))
        self.RB3.setText(_translate("Dialog", "장면전환"))
        self.RB4.setText(_translate("Dialog", "인트로"))
        self.RB5.setText(_translate("Dialog", "아웃트로"))

    def asd(self):
        task=Thread(target=self.magic)
        task.run()

    def magic(self):
        #--------------------------
        streamer=self.LE1.text()             #twitch id
        game=self.CB.currentIndex()                 #0모두 1해당게임만 2해당게임 제외
        game_name=self.LE3.text()
        cf=self.RB1.isChecked()                    #combineflag
        ascsort=self.RB2.isChecked()               #ascending sort 오름차순
        top=int(self.LE2.text())                  #영상수
        transition=self.RB3.isChecked()            #장면전환
        intro=self.RB4.isChecked()                 #인트로
        outtro= self.RB5.isChecked()               #아웃트로
        #-------------------------- 
        st=3 #sleeptime
        sourcehtml=[]
        sourcetitle=[]
        sourcegamelist=[]
        #chromedriver
        url='https://www.twitch.tv/'+streamer+'/clips?filter=clips&range=7d'
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        driver = webdriver.Chrome('chromedriver' , chrome_options=options)
        print("드라이버ON")
            
        #cliplink
        driver.get(url)
        time.sleep(st)
        req = driver.page_source
        resource=BeautifulSoup(req, 'html.parser')
        i=0
        for anchor in resource.find_all('a', class_="tw-full-width tw-interactive tw-link tw-link--hover-underline-none tw-link--inherit"):
            sourcehtml.append(anchor.get('href', '/'))
            i+=1
        for title in resource.find_all('h3', class_="tw-ellipsis tw-font-size-5"):
            sourcetitle.append(title.get_text())
        for htmlgame in resource.find_all('div',attrs={"class":"tw-aspect tw-aspect--align-center"}):
             for htmlgame2 in htmlgame.find_all('img',attrs={"class":"tw-image"}):
                sourcegamelist.append(htmlgame2.get('alt'))
        j=0
        for j in range(len(sourcetitle)):
            sourcetitle[j] = re.sub('[^0-9a-zA-Zㄱ-힗]', '', sourcetitle[j])
        driver.quit()
        #게임정리
        if game==1:
            for i in reversed(range(len(sourcegamelist))):
                if sourcegamelist[i]!=game_name:
                    del sourcegamelist[i]
                    del sourcehtml[i]
                    del sourcetitle[i]
        elif game==2:
             for i in reversed(range(len(sourcegamelist))):
                if sourcegamelist[i]==game_name:
                    del sourcegamelist[i]
                    del sourcehtml[i]
                    del sourcetitle[i]
        i=len(sourcehtml)
        print("게임정리")
        #출력
        if i==0:
            print("클립이없음")
            driver.quit()
            sys.exit(1)
        if i<top:
            top=i
            print(str(i)+'개의 클립')
        print('클립주소: '+str(len(sourcehtml)))
        print(sourcehtml)
        print('클립이름: '+str(len(sourcetitle)))
        print(sourcetitle)
        if game!=0:
            print('게임:'+str(len(sourcegamelist)))
            print(sourcegamelist)

        #download clip
        i=0
        for i in range(top):
            print((str(i+1)+'번째 다운로드 시작'))
            url='https://www.twitch.tv'+sourcehtml[i]
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            driver = webdriver.Chrome('chromedriver' , chrome_options=options)
            driver.get(url)
            time.sleep(st)

            url_element = driver.find_element_by_tag_name('video')
            vid_url = url_element.get_attribute('src')
            if cf:
                urlretrieve( vid_url,'clips/'+str(i)+'.mp4')
            else:
                urlretrieve( vid_url,'clips/'+str(i)+'.'+sourcetitle[i]+'.mp4')
            print((str(i+1)+'번째 완료'))
            driver.quit()

        #클립합치기
        if cf:
            print('영상 합치는중...')
            clip=[]
            i=0
            for i in range(top):
                clip.append(VideoFileClip('clips/'+str(i)+'.mp4'))
            if ascsort:
                clip.reverse()
            if transition:
                for i in reversed(range(1,top)):
                    clip.insert(i,VideoFileClip('clips/transition.mp4'))
            if intro:
                 clip.insert(0,VideoFileClip('clips/intro.mp4'))
            if outtro:
                 clip.append(VideoFileClip('clips/outtro.mp4'))
            finalclip=concatenate_videoclips(clip)
            print('영상 저장(약10분소요)')
            finalclip.write_videofile('clips/highlight.mp4', threads=4, logger=None)
            print("완료")
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
