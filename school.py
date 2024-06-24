import os
import sys
import time
import json
import random
import threading


from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QLabel, QProgressBar, 
			QDesktopWidget, QMainWindow, QGridLayout, 
			QApplication, QStackedLayout, QVBoxLayout, 
			QHBoxLayout, QFrame, QSizePolicy)
from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QThread
from PyQt5.QtGui import QFont
from flask import Flask, jsonify, request, render_template, Response

from data import Screens, Times, Types, Lessons, Notice


class QHLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(20)
        self.setMinimumWidth(5)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.setCursor(Qt.BlankCursor)
        

class QVLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(20)
        self.setMinimumHeight(5)
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.setCursor(Qt.BlankCursor)



class ServerThraed(QThread):
    app = Flask(__name__)

    def __init__(self, notice, lessons, tt, data, parent=None):
        QThread.__init__(self, parent)
        self.notice_signal = notice
        self.lessons_signal = lessons
        self.tt = tt
        self.data = data

        self.app.route('/notice')(self.notice)
        self.app.route('/notice', methods=['POST'])(self.notice_emit)

        self.app.route('/lessons')(self.lessons)
        self.app.route('/lessons', methods=['POST'])(self.lessons_emit)

        self.app.route('/data')(self.view_data)

    def run(self) -> None:
        self.app.run(port=5000, debug=False)

    def notice(self):
        return render_template('notice.html')

    def notice_emit(self):
        text = request.form['text']
        self.notice_signal.emit(text)
        return f"change to {text}"

    def lessons(self):
        return render_template('lessons.html', tt=self.tt)

    def lessons_emit(self):
        text = request.form['text']
        self.lessons_signal.emit(text)
        return f"changed to {text}"

    def view_data(self):
        return f"<pre>{self.data}</pre>"

class Gui(QMainWindow):
    notice_signal = pyqtSignal(str)
    lessons_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setCursor(Qt.BlankCursor)

    def initUI(self):
        self.day = self.get_day()
        self.times = self.encode_times()
        self.font = QFont('AppleSDGothicNeoR', pointSize=80, weight=QFont.Medium)
        self.last_change = time.time()
        self.status = 0

        self.setWindowTitle('School Info')
        #self.showMaximized()
        self.setup()
        self.showFullScreen()

        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(1000)
        
        self.notice_signal.connect(self.set_notice)
        self.lessons_signal.connect(self.set_lessons)

        self.today_lessons = None
        self.today_lessons = self.get_today_lessons()

        self.app = ServerThraed(
            self.notice_signal, 
            self.lessons_signal, 
            json.dumps(self.get_today_lessons(), ensure_ascii=False),
            open("data.py", "rb").read().decode()
        )
        thread = threading.Thread(target=self.app.run, daemon=True)
        thread.start()

    def set_notice(self, text):
        self.notice.setText(text)

    def set_lessons(self, text):
        self.today_lessons = json.loads(text)

    def get_day(self):
        return datetime.now().strftime("%Y%m%d")

    def encode_times(self):
        encoded_times = []
        for info in Times:
            encoded_info = {**info}
            now = datetime.now()
            time_split  = encoded_info["time"].split("/")
            encoded_datetime = now.replace(hour=int(time_split[0]), minute=int(time_split[1]))
            encoded_info["datetime"] = encoded_datetime.strftime("%Y%m%d/%H%M")
            encoded_info["timestamp"] = str(encoded_datetime.timestamp())
            encoded_times.append(encoded_info)

        return encoded_times

    def get_info(self):
        if self.get_day() != self.day:
            self.day = self.get_day()
            self.encoded_times = self.encode_times()
        
        now = time.time()
        min_timestamp = 2147483647
        info = {}
        i = 0
        for i_, encoded_info in enumerate(self.times):
            timestamp = float(encoded_info["timestamp"])
            if now > timestamp:
                continue
            if min_timestamp > timestamp:
                min_timestamp = timestamp
                info = encoded_info
                i = i_
        
        return i, info


    def get_hdivider(self):
        divider_container = QWidget()
        divider_layout = QHBoxLayout()
        divider = QHLine()
        divider.setLineWidth(0)
        divider.setMidLineWidth(10)
        divider_layout.addSpacing(30)
        divider_layout.addWidget(divider)
        divider_layout.addSpacing(30)
        divider_container.setLayout(divider_layout)

        return divider_container


    def setup(self):
        container = QWidget()
        layout = QVBoxLayout()

        stacked_container = QWidget()
        self.layout = QStackedLayout()

        timeleft_container = QWidget()
        timeleft_layout = QVBoxLayout()

        timeleft_title = QLabel('◆ 남은 시간 ◆')
        timeleft_title.setFont(self.font)
        timeleft_title.setStyleSheet("font-size: 70px;")
        timeleft_title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)


        self.timeleft = QLabel('-')
        self.timeleft.setStyleSheet("font-size: 400px;")
        self.timeleft.setFont(self.font) 
        self.timeleft.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.timeleft_pbr = QProgressBar(self)
        self.timeleft_pbr.setMaximum(1000)

        timeleft_layout.addStretch(1)
        timeleft_layout.addWidget(timeleft_title)
        timeleft_layout.addWidget(self.get_hdivider())
        timeleft_layout.addStretch(1)
        timeleft_layout.addWidget(self.timeleft)
        timeleft_layout.addStretch(4)

        timeleft_container.setLayout(timeleft_layout)
        self.layout.addWidget(timeleft_container)
        
        lesson_container = QWidget()
        lesson_layout = QVBoxLayout()

        lesson_title = QLabel('◆ 이번 수업 ◆')
        lesson_title.setFont(self.font)
        lesson_title.setStyleSheet("font-size: 70px;")
        lesson_title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.lesson = QLabel('-')
        self.lesson.setStyleSheet("font-size: 300px;")
        self.lesson.setFont(self.font)
        self.lesson.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.lesson_teacher = QLabel('-')
        self.lesson_teacher.setFont(self.font)
        self.lesson_teacher.setStyleSheet("font-size: 100px;")
        self.lesson_teacher.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        lesson_layout.addStretch(1)
        lesson_layout.addWidget(lesson_title)
        lesson_layout.addWidget(self.get_hdivider())
        lesson_layout.addWidget(self.lesson)
        lesson_layout.addWidget(self.lesson_teacher)
        lesson_layout.addStretch(3)

        lesson_container.setLayout(lesson_layout)
        self.layout.addWidget(lesson_container)

        notice_container = QWidget()
        notice_layout = QVBoxLayout()

        notice_title = QLabel('◆ 수행 / 공지 ◆')
        notice_title.setFont(self.font)
        notice_title.setStyleSheet("font-size: 70px;")
        notice_title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.notice = QLabel(Notice)
        self.notice.setFont(self.font)
        self.notice.setStyleSheet("font-size: 80px;")
        self.notice.setAlignment(Qt.AlignLeft)

        notice_hcontainer = QWidget()
        notice_hlayout = QHBoxLayout()

        notice_hlayout.addStretch(1)
        notice_hlayout.addWidget(self.notice)
        notice_hlayout.addStretch(1)
        notice_hcontainer.setLayout(notice_hlayout)

        notice_layout.addStretch(1)
        notice_layout.addWidget(notice_title)
        notice_layout.addWidget(self.get_hdivider())
        notice_layout.addWidget(notice_hcontainer)
        notice_layout.addStretch(5)

        notice_layout.setAlignment(Qt.AlignTop)
        notice_container.setLayout(notice_layout)
        self.layout.addWidget(notice_container)

        timetable_container = QWidget()
        timetable_layout = QVBoxLayout()

        timetable_title = QLabel('◆ 시간표 ◆') 
        timetable_title.setFont(self.font)
        timetable_title.setStyleSheet("font-size: 80px;")
        timetable_title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.timetable = QLabel('-')
        self.timetable.setFont(self.font)
        self.timetable.setStyleSheet("font-size: 100px;")
        
        timetable_hcontainer = QWidget()
        timetable_hlayout = QHBoxLayout()

        timetable_hlayout.addStretch(1)
        timetable_hlayout.addWidget(self.timetable)
        timetable_hlayout.addStretch(1)
        timetable_hcontainer.setLayout(timetable_hlayout)

        timetable_layout.addStretch(1)
        timetable_layout.addWidget(timetable_title)
        timetable_layout.addWidget(self.get_hdivider())
        timetable_layout.addWidget(timetable_hcontainer)
        timetable_layout.addStretch(5)

        timetable_layout.setAlignment(Qt.AlignTop)
        timetable_container.setLayout(timetable_layout)
        self.layout.addWidget(timetable_container)

        stacked_container.setLayout(self.layout)
        layout.addWidget(self.timeleft_pbr)
        layout.addWidget(stacked_container)

        container.setLayout(layout)
        self.setCentralWidget(container)

        self.layout.setCurrentIndex(self.status)

    def get_infos(self):
        i, now_info = self.get_info()
        prev_info = self.times[i-1]

        try:
            next_info = self.times[i+1]
        except:
            next_info = self.times[0]

        return now_info, prev_info, next_info, i

    def next_status(self):
        self.status += 1
        if self.status >= len(self.layout):
            self.status = 0
        self.last_change = time.time()

    def next_screen(self, progress):
        now_info, _, _, _ = self.get_infos()

        now_time = time.time()
        if now_time - self.last_change >= 4:
            if self.status == Screens.TTABLE \
                    and now_time - self.last_change < 8:
                return
            self.next_status()
            
            if now_info["type"] == Types.LESSON \
                    and self.status == Screens.LESSON:
                if progress >= 300:
                    self.next_status()

            if self.status == Screens.TTABLE and random.randrange(0, 2) != 0:
                self.next_status()
            self.layout.setCurrentIndex(self.status)

    def get_today_lessons(self):
        if self.today_lessons != None:
            return self.today_lessons

        try:
            today_lessons = Lessons[datetime.now().strftime("%a")]
        except:
            today_lessons = Lessons['Wed']
        self.today_lessons = today_lessons

        return today_lessons

    def progress(self):
        now_info, prev_info, next_info, i = self.get_infos()

        now_info_time = float(now_info["timestamp"])
        prev_info_time = float(prev_info["timestamp"])

        duration = now_info_time - prev_info_time
        progress = time.time() - prev_info_time
        self.timeleft_pbr.setValue(int(1000.0 * progress / duration))
        
        remain_seconds = int(now_info_time - time.time())
        hours, remainder = divmod(remain_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        seconds = str(seconds).zfill(2)
        if hours == 0:
            self.timeleft.setText(f"{minutes}:{seconds}")
        else:
            minutes = str(minutes).zfill(2)
            self.timeleft.setText(f"{hours}:{minutes}:{seconds}")

        self.next_screen(progress)
        today_lessons = self.get_today_lessons()

        if self.status == Screens.TTABLE:
            items = list(today_lessons.values())
            if time.time() - self.last_change < 4:
                r = range(4)
            else:
                r = range(4, len(items))
            text = "<table>"
            for i in r:
                text += f"<tr><td>{items[i]['subject']}</td> <td style='padding-left: 80px; vertical-align: middle; font-size: 50px;'>{items[i]['teacher']}</td>"
            text += "</table>"
            self.timetable.setText(text)
        
        lesson_info = None
        match now_info["type"]:
            case Types.RECESS:
                lesson_info = next_info
            case Types.LESSON:
                lesson_info = now_info
            case Types.S_INFO:
                lesson_info = next_info
            case Types.S_NODP:
                lesson_info = None
        
        if lesson_info != None:
            try:
                lesson = today_lessons[lesson_info["name"]]
            except:
                print("Error")
            else:
                self.lesson.setText(lesson["subject"])
                self.lesson_teacher.setText(lesson["teacher"])

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



if __name__ == '__main__':
    os.chdir(os.getcwd())
    window = QApplication(sys.argv)
    gui = Gui()
    sys.exit(window.exec_())
