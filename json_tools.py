import json
import tkinter as tk
from tkinter import filedialog


class Json_tools:
    def __init__(self,root):
        self.menu = tk.Menu(root.menu)
        root.menu.add_cascade(label="Json", menu=self.menu)

        self.menu.add_command(label="Open", command=lambda:self.load_json(root))
        self.menu.add_command(label="Combine", command=self.combine)
        self.menu.add_command(label="Count", command=lambda:self.count_label(root))
        self.menu.add_command(label="Id", command=lambda:self.generate_id(root))

        self.label = tk.Label(root, text="Json:")
        self.label_count = tk.Label(root, text="Count: ")
        self.label_id = tk.Label(root, text="Id: ")
        self.label.pack()
    def load_json(self,root): 
        file_path = filedialog.askopenfilename()
        with open(file_path, 'r', encoding='utf-8') as file:
            root.json = json.load(file)
        self.label.config(text="Json: " + file_path)

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

    def count_label(self,root):
        print(1)
        for x in root.json["shapes"]:
            if x["label"] in root.count_dict:
                root.count_dict[x["label"]] += 1
            else:
                root.count_dict[x["label"]] = 1
        print(root.count_dict)
        self.label_count.config(text="Count: " + str(root.count_dict))

    def generate_id(self,root):
        key_list = list(root.count_dict.keys())
        value_list = list(root.count_dict.values()) 
        
        for _ in range(len(key_list)):
            idx = value_list.index(max(value_list))     #获取最大值索引
            root.id_list.append(key_list[idx])               #添加最大值索引对应键
            value_list[idx] = 0                         #将最大值索引对应值置零
        print(root.id_list)
        self.label_id.config(text="Id: " + str(root.id_list))

if __name__ == "__main__":
    root = tk.Tk()
    Json_tools(root)
    root.mainloop()

    
