#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description : 自动实验
@Author      : LuckyQ
@version     : 1.0
'''
import json
from sys_operators import *


class AutoExper(object):
    def __init__(self, op_file, pos_file):
        with open(op_file, "r", encoding="utf-8") as f:
            self.op_list = json.load(f)
        with open(pos_file, "r", encoding="utf-8") as f:
            self.pos_dict = json.load(f)
            
        self.operator_dict = {
            "copy_file": CopyOperator(),
            "uncompressed": UncompressedOperator(),
            "file_search_by_suffix": FileSearchBySuffix(),
            "mouse": MouseOperator(self.pos_dict),
            "keyboard": KeyboardOperator(),
            "sleep": SleepOperator(),
            "test_case": TestCaseOperator()
        }
    
    def run(self):
        extend_args = None
        for op_item in self.op_list:
            op_name = op_item["op_name"]
            arg_dict = op_item["args"]
            if op_name not in self.operator_dict:
                print(f"[{op_name}] is not valid.")
                continue
            if extend_args is not None:
                for key, value in extend_args.items():
                    if key not in arg_dict:
                        arg_dict[key] = value
            operator = self.operator_dict[op_name]
            extend_args = operator.run(**arg_dict)
 
           
if __name__ == "__main__":
    op_file = "./configs/op.json"
    pos_file = "./configs/position.json"
    auto_exper = AutoExper(op_file, pos_file)
    auto_exper.run()          
        