import json
import tkinter as tk
import scipy.io as sio
import skimage.io

from tkinter import filedialog



#sio.savemat(r"D:\UseTools\OneDrive\codes\New-Research\data\indianpines_ts.mat", {'imggt': imggt})



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.Menu = tk.Menu(self)
        self.top1 = tk.Menu(self.Menu)
        self.top2 = tk.Menu(self.Menu)

        self.data = dict()
        self.dict_count = dict()
        self.id_list = ["背景"]
        self.file = dict()
        self.label = tk.Label(self, text="")
        self.label.pack()

        self.config(menu=self.Menu)
        self.Menu.add_cascade(label="File", menu=self.top1)
        self.Menu.add_cascade(label="Json", menu=self.top2)
        self.top1.add_command(label="Open", command=self.select_file)
        #self.top1.add_command(label="Json", command=lambda:self.json_format(self.data,self.top2))
        self.top1.add_command(label="Count", command=lambda:self.label_count(self.data))
        self.top1.add_command(label="Id", command=lambda:self.generate_id(self.dict_count))
        self.top1.add_command(label="Combine", command=self.combine)
        self.top1.add_command(label="Open_tif", command=self.open_tif)
        self.top1.add_command(label="Save_mat", command=self.save_mat)
        self.top1.add_command(label="Exit", command=self.quit)

        # 显示根窗口
        self.deiconify()
    
    def save_mat(self):
        fold_path = filedialog.asksaveasfilename(filetypes=[("MATLAB", "*.mat")])
        sio.savemat(fold_path, {'imggt': self.imggt})
    def open_tif(self):
        imgpath = filedialog.askopenfilename()
        self.imggt = skimage.io.imread(imgpath)
        self.label.config(text=imgpath)

    def select_file(self):
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename()
        self.label.config(text=file_path)

        # 输出选择的文件路径
        print("Selected file:", file_path)

        # 打开并读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

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
        
        for _ in range(len(key_list)):
            idx = value_list.index(max(value_list))     #获取最大值索引
            self.id_list.append(key_list[idx])               #添加最大值索引对应键
            value_list[idx] = 0                         #将最大值索引对应值置零
        print(self.id_list)

    def combine(self):
        file_path = filedialog.askopenfilenames()
        file_path_list = list(file_path)

        with open(file_path_list[-1],'r', encoding='utf-8') as f:
            file_path_list.pop()
            self.file = json.load(f)
            print(len(self.file["shapes"]))


        while(True):
            if not file_path_list:
                break
            with open(file_path_list[-1],'r', encoding='utf-8') as f:
                file_path_list.pop()
                file_temp = json.load(f)
                for dict_temp in file_temp["shapes"]:
                    self.file["shapes"].append(dict_temp)
                print(len(self.file["shapes"]))
        
        fold_path = filedialog.asksaveasfilename(filetypes=[("JSON", "*.json")])
        with open(fold_path,'w', encoding='utf-8') as f:
            json.dump(self.file, f, indent=4)

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

    def run(self):
        self.mainloop()
    
    def quit(self):
        self.destroy()
app = App()
app.run()