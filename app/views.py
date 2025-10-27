import tkinter as tk
from jsonp.view import JsonView
from tif.view import TifView
from mat.view import MatView


class Views(tk.Tk):
    def __init__(self):
        super().__init__()
        self.json = JsonView(self)
        self.tif = TifView(self)
        self.mat = MatView(self)

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)

        self.json_menu = tk.Menu(self.menu)
        self.mat_menu = tk.Menu(self.menu)
        self.tif_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Json", menu=self.json_menu)
        self.menu.add_cascade(label="Mat", menu=self.mat_menu)
        self.menu.add_cascade(label="TIF", menu=self.tif_menu)

        self.json_menu.add_command(label="Replace_label")
        self.json_menu.add_command(label="Combine")
        self.json_menu.add_command(label="Open")
        self.json_menu.add_command(label="Count")
        self.json_menu.add_command(label="Id")

        self.mat_menu.add_command(label="Open")
        self.mat_menu.add_command(label="Save_mat")

        self.tif_menu.add_command(label="Open")
        self.tif_menu.add_command(label="Save_tif")


        self.label_json = tk.Label(self, text="Json:", wraplength=300)
        self.label_json.pack()
        self.label_count = tk.Label(self, text="Count: ", wraplength=300)
        self.label_count.pack()
        self.label_id = tk.Label(self, text="Id: ", wraplength=300)
        self.label_id.pack()
        self.label_tif = tk.Label(self, text="TIF:", wraplength=300)
        self.label_tif.pack()
        self.label_mat = tk.Label(self, text="Mat:", wraplength=300)
        self.label_mat.pack()

    # menu
    ## Json
    def bind_json_replace_label(self, command: callable):
        self.json_menu.entryconfig("Replace_label", command=command)
    def bind_json_open(self, command: callable):
        self.json_menu.entryconfig("Open", command=command)

    def bind_json_combine(self, command: callable):
        self.json_menu.entryconfig("Combine", command=command)

    def bind_json_count(self, command: callable):
        self.json_menu.entryconfig("Count", command=command)

    def bind_json_id(self, command: callable):
        self.json_menu.entryconfig("Id", command=command)

    # Tif
    def bind_tif_open(self, command: callable):
        self.tif_menu.entryconfig("Open", command=command)
    
    def bind_tif_save(self, command: callable):
        self.tif_menu.entryconfig("Save_tif", command=command)

    ## Mat
    def bind_mat_open(self, command: callable):
        self.mat_menu.entryconfig("Open", command=command)
    def bind_mat_save(self, command: callable):
        self.mat_menu.entryconfig("Save_mat", command=command)


    # label
    ## Json
    def set_json_label(self, text: str):
        self.label_json.config(text="Json: " + text)

    def set_count_label(self, text: str):
        self.label_count.config(text="Count: " + text)

    def set_id_label(self, text: str):
        self.label_id.config(text="Id: " + text)
    ## Tif
    def set_tif_label(self, text: str):
        self.label_tif.config(text="TIF: " + text)
    
    ## Mat
    def set_mat_label(self, text: str):
        self.label_mat.config(text="Mat: " + text)

    def run(self):
        self.mainloop()

    def Json_View(self):
        pass
