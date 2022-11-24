#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description : 实时获取竖表位置
@Author      : LuckyQ
@version     : 1.0
'''
import time
import json
import os

import pyautogui as pg
import keyboard as kb
from threading import Thread, Condition

class PositionRecorder(object):
    def __init__(self, record_file):
        self.cursor_process = Thread(target=self.cursor_capture, args=())
        self.keyboard_process = Thread(target=self.keyboard_listen, args=())
        self.condition = Condition()
        self.pause = False
        self.records = {}
        self.output_file = record_file
        
    def run(self):
        self.cursor_process_run = True
        self.cursor_process.start()
        self.keyboard_process.start()

    def cursor_capture(self):
        while self.cursor_process_run:
            if self.pause:
                with self.condition:
                    self.condition.wait()
            curX, curY = pg.position()
            print(f"x: {str(curX).rjust(4)}, y: {str(curY).rjust(4)}")
            time.sleep(1)
         
    def _save_position(self):
        self.pause = True
        
        curX, curY = pg.position()
        position_title = input(f"Please input a title for this position([{curX}, {curY}]):")
        if position_title in self.records:
            print("Warning: This title is existed, it has been overwriteen.")
        self.records[position_title] = [curX, curY]
        print(f"Saved {position_title}=[{curX}, {curY}]")
        with self.condition:
            self.pause = False
            self.condition.notify()

    def _save_records(self):
        self.cursor_process_run = False
        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=True, indent=4)
            print(f"The position recorder has written to file {self.output_file}")
            os._exit(0)
        except Exception as e:
            print(e)
             
    def keyboard_listen(self):
        kb.add_hotkey("ctrl+alt", self._save_position)
        kb.add_hotkey("ctrl+c", self._save_records)
        kb.wait()
   
if __name__ == "__main__":
    position_recorder = PositionRecorder(record_file="position.json")
    position_recorder.run()