from Tkinter import *
import tkMessageBox

from utils.event_buffer import EventBuffer
from ui.button_kill import Kill
from ui.button_run import Run
from ui.button_refresh import Refresh
from ui.button_export_events import ExportEvents
from ui.text_events import Events
from ui.text_time_started import TimeStarted
from ui.text_title import Title
from ui.text_uptime import Uptime
from ui.text_status import Status
from bot import RedditBot


class GUI:
    def __init__(self):
        self.bot = RedditBot(self)
        self.bot_thread = None
        self.uptime_thread = None
        self.bot = RedditBot(self)
        self.buffer = EventBuffer(25)

        self.frame = Tk()
        self.frame.wm_title("Build A PC Sales Bot")
        self.frame.configure(background="#333333")

        self.title = Title(self)
        self.status = Status(self)
        self.uptime = Uptime(self)
        self.time_started = TimeStarted(self)
        self.run = Run(self)
        self.kill = Kill(self)
        self.refresh = Refresh(self)
        self.export_events = ExportEvents(self)
        self.event_list = Events(self)
        self.frame.protocol("WM_DELETE_WINDOW", self.on_closing)
        mainloop()

    def on_closing(self):
        if (self.bot_thread or self.uptime_thread) and \
                tkMessageBox.askokcancel("Quit", "Are you sure you want to quit? There are processes running"):

            self.frame.destroy()
        self.frame.destroy()

if __name__ == "__main__":
    gui = GUI()
