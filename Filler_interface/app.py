import sys
from typing import List
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSize, QTimer, QEvent
from PyQt5.QtGui import QCursor

from Style_windows.style import Style


class App(QApplication):
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)

        self.styling = Style()

        self.window_size = QSize(720, 480)

        self.on_fullscreen = False
        self.cursor_move_2 = False

        self.lang_num = '0'
        self.color = 'green'

        self.lang = 0

        self.timer_datetime = QTimer()
        self.timer_datetime.timeout.connect(self.datetime)
        self.time_datetime = 210000
        self.timer_datetime.start(self.time_datetime)

        self.installEventFilter(self)

    
    def run(self):
        self.set_style()
        self.language()
        self.fullscreen()

        self.window_low.show()
        self.window_start.show_animation()

        sys.exit(app.exec_())
    

    def fullscreen(self):
        if self.on_fullscreen:
            self.window_start.fullscreen()
            self.window_datetime.fullscreen()
            self.window_low.fullscreen()
            self.window_main_filler.fullscreen()
            self.window_list1.fullscreen()
            self.window_statistic.fullscreen()
            self.window_settings1.fullscreen()
            self.window_settings2.fullscreen()
            self.window_prepare.fullscreen()
            self.window_view.fullscreen()
            self.window_filler.fullscreen()
            self.window_level.fullscreen()
            self.window_cip.fullscreen()
            self.window_robot.fullscreen()


    def eventFilter(self, obj, event):
        if self.cursor_move_2: 
            print(self.cursor_move_2)
            print('СОБЫЬТЕ')
            if event.type() == QEvent.MouseButtonRelease:  
                QCursor.setPos(5, 5)

        
        if event.type() == QEvent.MouseButtonPress:
            self.datetime_reset()
            self.window_datetime.hide()

        return super().eventFilter(obj, event)


    def datetime(self):
        app.window_datetime.show_window()
        

    def datetime_reset(self):
        self.timer_datetime.stop()
        self.timer_datetime.start(self.time_datetime)


    def language(self):
        lang_num = int(self.lang_num)

        self.window_main_filler.language(lang_num)
        self.window_list1.language(lang_num)
        self.window_statistic.language(lang_num)
        self.window_settings1.language(lang_num)
        self.window_settings2.language(lang_num)
        self.window_prepare.language(lang_num)
        self.window_filler.language(lang_num)
        self.window_cip.language(lang_num)
        self.window_robot.language(lang_num)
        self.window_pop_up.language(lang_num)
        self.window_level.language(lang_num)


    def set_style(self):
        self.recolor()
        self.icons_recolor()


    def icons_recolor(self):
        self.styling.recolor_icons()
        
        self.window_main_filler.set_icons()
        self.window_list1.set_icons()
        self.window_settings1.set_icons()
        self.window_settings2.set_icons()
        self.window_statistic.set_icons()
        self.window_cip.set_icons()
        self.window_robot.set_icons()


    def recolor(self):
        style = self.styling.style()
        #style.recolor(self, (42, 122, 96, 255))
        style = self.styling.recolor_css(style)
        self.setStyleSheet(style)


    def check_timer(self):
        print('timer window_datetime: ', self.window_datetime.timer.isActive())
        print('timer window_start: ', self.window_start.timer.isActive())
   

    def exit(self):
        sys.exit(self.exec_())
    

app = App(sys.argv)


from Window_start.start_conrtol import window_start
app.window_start = window_start

from Window_datetime.datetime_control import window_datetime
app.window_datetime = window_datetime

from Window_pop_up.pop_up_control import window_pop_up
app.window_pop_up = window_pop_up

from Window_low.low_control import window_low
app.window_low = window_low

from Window_main.main_filler_conrtol import main_filler_window
app.window_main_filler = main_filler_window 

from Window_list1.list1_control import window_list1
app.window_list1 = window_list1

from Window_statistic.statistic_control import window_statistic
app.window_statistic = window_statistic

from Window_settings1.settings_control import window_setting
app.window_settings1 = window_setting

from Window_settings2.settings2_control import window_setting2
app.window_settings2 = window_setting2

from Window_prepare.prepare_control import window_prepare
app.window_prepare = window_prepare

from Window_view.view_conrtol import window_view
app.window_view = window_view

from Window_filler.filler_conrtol import filler_window
app.window_filler = filler_window

from Window_level.level_conrtol import window_level
app.window_level = window_level

from Window_cip.cip_control import window_cip
app.window_cip = window_cip

from Window_robot.robot_control import window_robot
app.window_robot = window_robot

from Window_robot.robot_control import window_robot
app.window_robot = window_robot

