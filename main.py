import json
import tkinter as tk


from tkinter import filedialog

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.Menu = tk.Menu(self)
        self.top1 = tk.Menu(self.Menu)
        self.top2 = tk.Menu(self.Menu)

        self.data = dict()
        self.dict_count = dict()

        self.config(menu=self.Menu)
        self.Menu.add_cascade(label="File", menu=self.top1)
        self.Menu.add_cascade(label="Json", menu=self.top2)
        self.top1.add_command(label="Open", command=self.select_file)
        #self.top1.add_command(label="Json", command=lambda:self.json_format(self.data,self.top2))
        self.top1.add_command(label="Count", command=lambda:self.label_count(self.data))
        self.top1.add_command(label="Id", command=lambda:self.generate_id(self.dict_count))
        self.top1.add_command(label="Exit", command=self.quit)

        # 显示根窗口
        self.deiconify()
        
    def select_file(self):
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename()
        self.label = tk.Label(self, text=file_path)
        self.label.pack()

        # 输出选择的文件路径
        print("Selected file:", file_path)

        # 打开并读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)


    def run(self):
        self.mainloop()
    
    def quit(self):
        self.destroy()

    def label_count(self, json_data):
        for x in json_data["shapes"]:
            if x["label"] in self.dict_count:
                self.dict_count[x["label"]] += 1
            else:
                self.dict_count[x["label"]] = 1
        print(self.dict_count)
        self.label = tk.Label(self, text=self.dict_count, wraplength=500)
        self.label.pack()

    def generate_id(self, dict_count):
        key_list = list(dict_count.keys())
        value_list = list(dict_count.values()) 
        id_list = ["背景"]
        for _ in range(len(key_list)):
            idx = value_list.index(max(value_list))   #获取最大值索引
            id_list.append(key_list[idx])       #添加最大值索引对应键
            value_list[idx] = 0                  #将最大值索引对应值置零
        print(id_list)

    def json_format(self,json_data,menu):
        for key, value in json_data.items():
            sub = tk.Menu(menu)
            menu.add_cascade(label=key, menu=sub)
            if isinstance(value, dict):
                self.json_format(value,sub)
                
            elif isinstance(value, list):
                for item in value:
                    sub.add_command(label=item)

            elif isinstance(value, str):
                sub.add_command(label=value)

            else:
                sub.add_command(label=value)



app = App()
app.run()