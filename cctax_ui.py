
#****************************************************************************************************
# File Start!
#***************************************************************************************************/

#*
 #
 #  Copyright (c) 2024-2025 by flechazo. All rights reserved.
 #
 # Author : CarlChai LinFeng Chai flechazo
 # Website: flechazo.mba
 #
 # Change Logs:
 # Date           Author       Notes
 # 2025-06-20     cc          the first version
 #
#/

#****************************************************************************************************
# Include
#***************************************************************************************************/

import os
import json
import tkinter as tk
from tkinter import ttk,messagebox
from cctax_calc import cctax_calc

#****************************************************************************************************
# Define
#***************************************************************************************************/

#****************************************************************************************************
# Type Define
#***************************************************************************************************/

class cctax_ui:
    # init #
    def __init__(self, root):
        self.root = root
        self.root.title("税后收入计算器")
        self.root.geometry("800x600")
        # database #
        self.calc_results = []
        self.calc_details = []
        self.path_database = "cctax_database.json"
        # create #
        self.calculator = cctax_calc()
        # operate frame #
        self.operate_frame_init()
        # table frame #
        self.table_frame_init()
        # detail frame #
        self.detail_frame_init()

        # load database #
        self.load_data()
        return

    #****************************************************************************************************
    # sub frame
    #***************************************************************************************************/
    # operate frame init #
    def operate_frame_init(self):
        self.operate_frame = ttk.LabelFrame(self.root, text="输入数据", padding="10")
        self.operate_frame.pack(fill="x", padx=10, pady=5)
        # salary input #
        ttk.Label(self.operate_frame, text="税前工资:").grid(row=0, column=0, padx=5, pady=5)
        self.operate_salary_input = ttk.Entry(self.operate_frame)
        self.operate_salary_input.grid(row=0, column=1, padx=5, pady=5)

        # insurance base #
        ttk.Label(self.operate_frame, text="社保基数:").grid(row=0, column=2, padx=5, pady=5)
        self.operate_insurance_base_input = ttk.Entry(self.operate_frame)
        self.operate_insurance_base_input.grid(row=0, column=3, padx=5, pady=5)

        # add button #
        ttk.Button(self.operate_frame, text="计算", command=self.calculate).grid(row=0, column=4, padx=5, pady=5)
        pass

    # table frame init #
    def table_frame_init(self):
        self.table_frame = ttk.LabelFrame(self.root, text="计算结果", padding="10")
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # title #
        columns = ("税前工资", "社保基数", "养老保险", "医疗保险", "失业保险", "公积金", "应纳税所得额", "个人所得税", "税后收入")
        self.table_frame_treeview = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.table_frame_treeview.heading(col, text=col)
            self.table_frame_treeview.column(col, width=80)
        
        # scroll bar #
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table_frame_treeview.yview)
        self.table_frame_treeview.configure(yscrollcommand=scrollbar.set)
        self.table_frame_treeview.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # click event #
        self.table_frame_treeview.bind("<ButtonRelease-1>", self.detail_text_show)
        pass

    # detail frame init #
    def detail_frame_init(self):
        self.detail_frame = ttk.LabelFrame(self.root, text="计算详情", padding="10")
        self.detail_frame.pack(fill="both", expand=True, padx=10, pady=5)
        # calc detail #
        self.detail_text = tk.Text(self.detail_frame, height=10, state='disabled')
        self.detail_text.pack(fill="x", padx=10, pady=5)
        pass

    #****************************************************************************************************
    # event
    #***************************************************************************************************/
    # click table item #
    def detail_text_show(self,event):
        # get selected #
        selected_item = self.table_frame_treeview.focus()
        if not selected_item:
            return
        # get index #
        item_index = self.table_frame_treeview.index(selected_item)
        # show detail #
        if 0 <= item_index < len(self.calc_details):
            detail = self.calc_details[item_index]
            self.detail_text.config(state='normal')
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(tk.END, detail)
            self.detail_text.config(state='disabled')
        pass

    # tax calc #
    def calculate(self):
        # get salary #
        salary = float(self.operate_salary_input.get())
        insurance_base = float(self.operate_insurance_base_input.get())
        # get calc result #
        result,detail,steps = self.calculator.calc(salary,insurance_base)
        # show detail #
        self.detail_text.config(state='normal')
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, detail)
        self.detail_text.config(state='disabled')
        # add table #
        self.table_frame_treeview.insert("", "end", values=result)
        # save #
        self.calc_details.append(detail)
        self.calc_results.append(result)
        if not hasattr(self, 'steps_list'):
            self.steps_list = []
        self.steps_list.append(steps)
        self.save_data()
        # clear input #
        self.operate_salary_input.delete(0, "end")
        self.operate_insurance_base_input.delete(0, "end")
        pass

    # save data #
    def save_data(self):
        # save #
        data = []
        steps_list = getattr(self, 'steps_list', [])
        for i, (result, detail) in enumerate(zip(self.calc_results, self.calc_details)):
            steps = steps_list[i] if i < len(steps_list) else []
            data.append({
                "result": result,
                "detail": detail,
                "steps": steps
            })
        with open(self.path_database, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        pass

    # load data #
    def load_data(self):
        # read database #
        if not os.path.exists(self.path_database):
            self.steps_list = []
            return
        try:
            with open(self.path_database, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.steps_list = []
            for item in data:
                result = tuple(item["result"])
                detail = item["detail"]
                steps = item.get("steps", [])
                self.table_frame_treeview.insert("", "end", values=result)
                self.calc_results.append(result)
                self.calc_details.append(detail)
                self.steps_list.append(steps)
        except Exception as e:
            messagebox.showerror("错误", f"读取历史数据失败: {e}")
        pass

#****************************************************************************************************
# Global Variable
#***************************************************************************************************/

#****************************************************************************************************
# Function Impletement
#***************************************************************************************************/

#****************************************************************************************************
# exports
#***************************************************************************************************/

#****************************************************************************************************
# File End!
#***************************************************************************************************/
