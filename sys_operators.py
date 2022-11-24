#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description : 系统操作对象
@Author      : LuckyQ
@version     : 1.0
'''
import os
import time
import json

import shutil
import zipfile
import rarfile
import pyperclip as pclip
import pyautogui as pg

class SysOperator(object):
    def run(self, **kwargs):
        raise NotImplementedError()

'''Copy File from source to destination'''  
class CopyOperator(SysOperator):
    def run(self, **kwargs):
        try:
            src_file = kwargs["src"]
            dest_file = kwargs["dest"]
            suffix = src_file.split('.')[-1]
            if suffix not in ["zip", "rar"]:
                suffix = "zip"
            dest_file = dest_file + f".{suffix}"
            shutil.copy(src_file, dest_file)
            print(f"copy {src_file} to {dest_file}")
            return {"compress_file": dest_file}
        except Exception as e:
            print(f"Exception {e} raised in CopyOperator Running")
       
'''Delete File(include directory)'''           
class DeleteOperator(SysOperator):
    def run(self, **kwargs):
        try:
            file_path = kwargs["file_path"]
            shutil.rmtree(file_path)
            print(f"Delete file {file_path}")
        except Exception as e:
            print(f"Exception {e} raised in DeleteOperator Running")           

'''Mouse Operation'''
class MouseOperator(SysOperator):
    def __init__(self, pos_dict):
        self.pos_dict = pos_dict
        
    def run(self, **kwargs):
        try:
            op_name = kwargs["op_name"]
            if op_name == "left_click":
                pg.click()
            elif op_name == "right_click":
                pg.click(button="right")
            elif op_name == "double_click":
                pg.doubleClick()
            elif op_name == "move":
                dest_pos = kwargs["dest"]
                x, y = self.pos_dict[dest_pos]
                pg.moveTo(x, y, duration=0.5)
            elif op_name == "drag":
                dest_pos = kwargs["dest"]
                x, y = self.pos_dict[dest_pos]
                pg.dragTo(x, y, duration=1.0)
            else:
                raise Exception(f"operation [{op_name}] is not existed.")
        except Exception as e:
            print(f"Exception {e} raised in MouseOperator Running")

            
'''Keyboard Operation'''           
class KeyboardOperator(SysOperator):
    def run(self, **kwargs):
        try:
            op_name = kwargs["op_name"]
            if op_name == "press":
                key_name = kwargs["key_name"]
                if "+" in key_name:
                    pg.hotkey(tuple(key_name.split("+")))
                else:
                    pg.press(key_name)
                print(f"[{key_name}] {op_name}...")
            elif op_name == "key_down":
                key_name = kwargs["key_name"]
                pg.keyDown(key_name)
                print(f"[{key_name}] {op_name}...")
            elif op_name == "key_up":
                key_name = kwargs["key_name"]
                pg.keyUp(key_name)
                print(f"[{key_name}] {op_name}...")
            elif op_name == "input":
                content = kwargs["content"]
                pg.write(content)
                print(f"keyboard input content: {content}")
            else:
                raise Exception(f"operation [{op_name}] is not existed.")
        except Exception as e:
            print(f"Exception {e} raised in KeyboardOperator Running")
            
            
class ClipOperator(SysOperator):
    def run(self, **kwargs):
        try:
            op_name = kwargs["op_name"]
            if op_name == "copy":
                # copy content to clipboard
                content = kwargs["content"]
                pclip.copy(content)
            elif op_name == "paste":
                # get content from clipboard to content
                content = pclip.paste()
                return content
            else:
                raise Exception(f"operation [{op_name}] is not existed.")
        except Exception as e:
            print(f"Exception {e} raised in ClipOperator Running")
         
            
'''Uncompress Operation'''''
class UncompressedOperator(SysOperator):
    def run(self, **kwargs):
        try:
            compress_file = kwargs["compress_file"]
            save_path = kwargs["save_path"]
            suffix = compress_file.split('.')[-1]
            if suffix == "zip":
                with zipfile.ZipFile(compress_file) as zf:
                    for zip_file in zf.namelist():
                        zip_file = zip_file.encode("cp437").decode("gbk")
                    zf.extractall(save_path)
                print(f"zip file [{compress_file}] has extrated")
            elif suffix == "rar":
                with rarfile.RarFile(compress_file) as rf:
                    for rar_file in rf.namelist():
                        rar_file = rar_file.encode("cp437").decode("gbk")
                    rf.extractall(save_path)
                print(f"rar file [{compress_file}] has extrated")
            else:
                print(f"Unspupport compress type {suffix}")
        except Exception as e:
            print(f"Exception {e} raised in UncompressedOperator Running")
        
            
'''Search one file by suffix'''
class FileSearchBySuffix(SysOperator):
    def run(self, **kwargs):
        try:
            root_dir = kwargs["root_dir"]
            suffix = kwargs["suffix"]
            for root, dirs, files in os.walk(root_dir, topdown=True):
                for file_name in files:
                    if file_name.split('.')[-1] == suffix:
                        target_file = os.path.join(root, file_name)
                        return {"content": target_file}
        except Exception as e:
            print(f"Exception {e} raised in FileSearchBySuffix Running")
   
            
'''Sleep Operation'''
class SleepOperator(SysOperator):
    def run(self, **kwargs):
        try:
            sleep_time = kwargs["sleep_time"]
            time.sleep(sleep_time)
        except Exception as e:
            print(f"Exception {e} raised in SleepOperator Running")
            

'''TestCase Operation'''            
class TestCaseOperator(SysOperator):
    def run(self, **kwargs):
        try:
            test_file = kwargs["test_file"]
            with open(test_file, "r", encoding="utf-8") as f:
                test_dict = json.load(f)
            for test_name, test_content in test_dict.items():
                print(f"Testing {test_name}...")
                pg.write(test_content)
                pg.press("enter")
                time.sleep(1)
        except Exception as e:
            print(f"Exception {e} raised in TestCaseOperator Running")