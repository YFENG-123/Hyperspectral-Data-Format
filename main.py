import tkinter as tk
from tkinter import filedialog


from tools import File_tools
from json_tools import Json_tools
from tif_tool import Tif_tools
from mat_tools import Mat_tools

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # 变量名
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.file_tools = File_tools(self)
        self.json_tools = Json_tools(self)
        self.tif_tools = Tif_tools(self)
        self.mat_tools = Mat_tools(self)

        

        self.json = dict()
        self.imggt = None
        self.tif = None



        self.data = dict()
        self.count_dict = dict()
        self.id_list = ["背景"]
        self.file = dict()


        # 显示根窗口
        self.deiconify()

    def run(self):
        self.mainloop()
    
    def quit(self):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.run()