import sys
from typing import List
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSize, QTimer, QEvent
from PyQt5.QtGui import QCursor, QFontDatabase

from Filler_interface.Style_windows.style import Style


try:
    raspberry = True
except ImportError:
    raspberry = False


class App(QApplication):
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)

        self.styling = Style()

        self.window_size = QSize(720, 480)

        self.on_fullscreen = False
        self.cursor_move_2 = True

        if raspberry:
            font_id = QFontDatabase.addApplicationFont("/usr/share/fonts/truetype/siemens_ad_vn.ttf")
            self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            self.font_family = 'Siemens AD Sans'

        self.lang_num = 0
        self.color = 'green'

        self.lang = 0

        self.window_focus = ''

        self.timer_datetime = QTimer()
        self.timer_datetime.timeout.connect(self.datetime)
        self.time_datetime = 210000
        self.timer_datetime.start(self.time_datetime)

        self.installEventFilter(self)

        self.ready = False

    
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
            self.window_error.fullscreen()
            self.window_cip.fullscreen()
            self.window_robot.fullscreen()


    def eventFilter(self, obj, event):
        # if self.cursor_move_2: 
        #     if event.type() == QEvent.MouseButtonRelease:
        #         QCursor.setPos(5, 5)

        #         # focus_widget = self.focusWidget()
                
        #         # if focus_widget:
        #         #     focus_widget.clearFocus()

        
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
        lang_num = self.lang_num

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
        self.window_error.language(lang_num)


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
   
    
    def close_windows(self):
        if self.window_focus != self.window_start.window_name:
            self.window_start.hide()
            print(f'close: {self.window_start.window_name}')
        
        if self.window_focus != self.window_datetime.window_name:
            self.window_datetime.hide()
            print(f'close: {self.window_datetime.window_name}')
        
        if self.window_focus != self.window_main_filler.window_name:
            self.window_main_filler.hide()
            print(f'close: {self.window_main_filler.window_name}')

        if self.window_focus != self.window_list1.window_name:
            self.window_list1.hide()
            print(f'close: {self.window_list1.window_name}')
        
        if self.window_focus != self.window_statistic.window_name:
            self.window_statistic.hide()
            print(f'close: {self.window_statistic.window_name}')

        if self.window_focus != self.window_settings1.window_name:
            self.window_settings1.hide()
            print(f'close: {self.window_settings1.window_name}')

        if self.window_focus != self.window_settings2.window_name:
            self.window_settings2.hide()
            print(f'close: {self.window_settings2.window_name}')

        if self.window_focus != self.window_prepare.window_name:
            self.window_prepare.hide()
            print(f'close: {self.window_prepare.window_name}')

        if self.window_focus != self.window_view.window_name:
            self.window_view.close()
            print(f'close: {self.window_view.window_name}')

        if self.window_focus != self.window_filler.window_name:
            self.window_filler.hide()
            print(f'close: {self.window_filler.window_name}')

        if self.window_focus != self.window_error.window_name:
            self.window_error.hide()
            print(f'close: {self.window_error.window_name}')

        if self.window_focus != self.window_cip.window_name:
            self.window_cip.hide()
            print(f'close: {self.window_cip.window_name}')

        if self.window_focus != self.window_robot.window_name:
            self.window_robot.hide()
            print(f'close: {self.window_robot.window_name}')


    def show_windows(self):
        match self.window_focus:
            case self.window_start.window_name:
                self.window_start.hide()
                self.window_start.show()

            case self.window_main_filler.window_name:
                self.window_main_filler.hide()
                self.window_main_filler.show()
            
            case self.window_list1.window_name:
                self.window_list1.show()

            case self.window_statistic.window_name:
                self.window_statistic.hide()
                self.window_statistic.show()
            
            case self.window_settings1.window_name:
                self.window_settings1.hide()
                self.window_settings1.show()
                
            case self.window_settings2.window_name:
                self.window_settings2.hide()
                self.window_settings2.show()

            case self.window_prepare.window_name:
                self.window_prepare.hide()
                self.window_prepare.show()
            
            case self.window_view.window_name:
                self.window_view.close(1)
                self.window_view.show()

            case self.window_filler.window_name:
                self.window_filler.hide()
                self.window_filler.show()

            case self.window_error.window_name:
                self.window_error.hide()
                self.window_error.show()

            case self.window_cip.window_name:
                self.window_cip.hide()
                self.window_cip.show()

            case self.window_robot.window_name:
                self.window_robot.hide()
                self.window_robot.show()


    def exit(self):
        sys.exit(self.exec_())
    

app = App(sys.argv)


from Filler_interface.Window_start.start_conrtol import window_start
app.window_start = window_start

from Filler_interface.Window_datetime.datetime_control import window_datetime
app.window_datetime = window_datetime

from Filler_interface.Window_pop_up.pop_up_control import window_pop_up
app.window_pop_up = window_pop_up

from Filler_interface.Window_low.low_control import window_low
app.window_low = window_low

from Filler_interface.Window_main.main_filler_conrtol import main_filler_window
app.window_main_filler = main_filler_window 

from Filler_interface.Window_list1.list1_control import window_list1
app.window_list1 = window_list1

from Filler_interface.Window_statistic.statistic_control import window_statistic
app.window_statistic = window_statistic

from Filler_interface.Window_settings1.settings_control2 import window_setting1
app.window_settings1 = window_setting1

from Filler_interface.Window_settings2.settings2_control import window_setting2
app.window_settings2 = window_setting2

from Filler_interface.Window_prepare.prepare_control import window_prepare
app.window_prepare = window_prepare

from Filler_interface.Window_view.view_conrtol import window_view
app.window_view = window_view

from Filler_interface.Window_error.error_conrtol import window_error
app.window_error = window_error

from Filler_interface.Window_cip.cip_control3 import window_cip
app.window_cip = window_cip

from Filler_interface.Window_robot.robot_control import window_robot
app.window_robot = window_robot

from Filler_interface.Window_filler.filler_control2 import window_filler
app.window_filler = window_filler


app.ready = True

from Filler_interface.threads import Thread
app.threads = Thread()



