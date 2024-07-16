import sys
from typing import List
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSize

from Style_windows.style import style


class App(QApplication):
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)

        self.window_size = QSize(640, 420)

        self.lang_num = {'Русский': 0, 'English': 1, 'Deutsch': 2, '中国人': 3}

        self.lang = 'Русский'
        self.color = 'green'
    
    
    def run(self):
        self.style(self.color)
        self.language(self.lang)
        self.fullscreen(True)

        self.window_low.show()
        self.window_start.show_window()
    

    def fullscreen(self, on):
        if on:
            self.window_low.fullscreen()
            self.window_main_filler.fullscreen()
            self.window_settings1.fullscreen()


    def language(self, language):
        lang = self.lang_num[language]
        
        self.window_main_filler.language(lang)
        self.window_settings1.language(lang)


    def style(self, color):
        style_text = style(color)

        self.setStyleSheet(style_text)
    

    def check_timer(self):
        print('timer window_datetime: ', self.window_datetime.timer.isActive())
        print('timer window_start: ', self.window_start.timer.isActive())
        print('timer window_main_filler: ', self.window_main_filler.timer.isActive())
   

    def exit(self):
        sys.exit(self.exec_())
    

app = App(sys.argv)

from Window_start.start_conrtol import window_start
app.window_start = window_start

from Window_datetime.datetime_conrtol import window_datetime
app.window_datetime = window_datetime

from Window_low.low_control import window_low
app.window_low = window_low

from Window_main.main_filler_conrtol import main_filler_window
app.window_main_filler = main_filler_window 

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
