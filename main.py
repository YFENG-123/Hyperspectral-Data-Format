import json
import tkinter as tk
import scipy.io as sio
import skimage.io

from tkinter import filedialog

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # 变量名
        self.Menu = tk.Menu(self)
        self.top1 = tk.Menu(self.Menu)
        self.top2 = tk.Menu(self.Menu)
        self.top3 = tk.Menu(self.Menu)

        self.data = dict()
        self.count_dict = dict()
        self.id_list = ["背景"]
        self.file = dict()

        self.json = dict()
        self.imggt = None
        self.tif = None


        # 标签
        self.label_json = tk.Label(self, text="Json:")
        self.label_json.pack()
        self.label_count = tk.Label(self, text= "Count:")
        self.label_count.pack()
        self.label_id = tk.Label(self, text= "Id:")
        self.label_id.pack()
        self.label_tif = tk.Label(self, text= "Tif:")
        self.label_tif.pack()
        self.label_mat = tk.Label(self, text= "Mat:")
        self.label_mat.pack()

        # 菜单
        self.config(menu=self.Menu)
        self.Menu.add_cascade(label="File", menu=self.top1)
        self.Menu.add_cascade(label="Json", menu=self.top2)
        self.Menu.add_cascade(label="Mat", menu=self.top3)

        self.top1.add_command(label="Open", command=self.select_file)
        self.top1.add_command(label="Exit", command=self.quit)

        self.top2.add_command(label="Count", command=lambda:self.count_label)
        self.top2.add_command(label="Id", command=lambda:self.generate_id)
        self.top2.add_command(label="Combine", command=self.combine)

        self.top3.add_command(label="Save_mat", command=self.save_mat)

        # 显示根窗口
        self.deiconify()
    

    def save_mat(self):
        fold_path = filedialog.asksaveasfilename(filetypes=[("MATLAB", "*.mat")])
        sio.savemat(fold_path, {'imggt': self.imggt})

    def select_file(self):
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename()

        # 输出选择的文件路径
        print("Selected file:", file_path)

        
        # 打开并读取文件
        with open(file_path, 'r', encoding='utf-8') as file:
            file_type = file_path.split(".")[-1]
            if file_type == "json":
                self.json = json.load(file)
                self.label_json.config(text="Json: " + file_path)
            elif file_type == "mat":
                self.imggt = sio.loadmat(file_path)
                self.label_mat.config(text="Mat: " + file_path)
            elif file_type == "tif":
                self.imggt = skimage.io.imread(file_path)
                self.label_tif.config(text="Tif: " + file_path)

    def count_label(self):
        print(1)
        for x in self.json["shapes"]:
            if x["label"] in self.count_dict:
                self.count_dict[x["label"]] += 1
            else:
                self.count_dict[x["label"]] = 1
        print(self.count_dict)
        self.label_count.config(text="Count: " + str(self.count_dict))

    def generate_id(self):
        key_list = list(self.count_dict.keys())
        value_list = list(self.count_dict.values()) 
        
        for _ in range(len(key_list)):
            idx = value_list.index(max(value_list))     #获取最大值索引
            self.id_list.append(key_list[idx])               #添加最大值索引对应键
            value_list[idx] = 0                         #将最大值索引对应值置零
        print(self.id_list)
        self.label_id.config(text="Id: " + str(self.id_list))

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

    def run(self):
        self.mainloop()
    
    def quit(self):
        self.destroy()

app = App()
app.run()