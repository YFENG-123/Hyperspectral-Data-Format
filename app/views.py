import tkinter as tk
from jsonp.view import JsonView
from tif.view import TifView
from mat.view import MatView
from hdr.view import HdrView


class Views(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("数据格式化工具")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        print(width, height)
        self.geometry(str(int(width/3))+"x"+str(int(height/4))+"+"+str(int(width/4))+"+"+str(int(height/4)))

        self.json = JsonView(self)
        self.tif = TifView(self)
        self.mat = MatView(self)
        self.hdr = HdrView(self)

        self.menu = tk.Menu(self,tearoff=False)
        self.config(menu=self.menu)

        self.json_menu = tk.Menu(self.menu,tearoff=False)
        self.mat_menu = tk.Menu(self.menu,tearoff=False)
        self.tif_menu = tk.Menu(self.menu,tearoff=False)
        self.hdr_menu = tk.Menu(self.menu,tearoff=False)
        self.menu.add_cascade(label="Json", menu=self.json_menu)
        self.menu.add_cascade(label="Mat", menu=self.mat_menu)
        self.menu.add_cascade(label="TIF", menu=self.tif_menu)
        self.menu.add_cascade(label="HDR", menu=self.hdr_menu)

        ## Json
        self.json_menu.add_command(label="Open")
        self.json_menu.add_command(label="Replace_label")
        self.json_menu.add_command(label="Delete_label")
        self.json_menu.add_command(label="Combine")
        self.json_menu.add_command(label="Convert_to_tif")
        self.json_menu.add_command(label="Convert_to_mat")
        self.json_menu.add_command(label="Convert_to_mat_resize")
        self.json_menu.add_command(label="Remove_overlap")

        ## Mat
        self.mat_menu.add_command(label="Open")
        self.mat_menu.add_command(label="Save_mat")

        ## Tif
        self.tif_menu.add_command(label="Open")
        self.tif_menu.add_command(label="Save_tif")
        self.tif_menu.add_command(label="Draw_label")

        ## Hdr
        self.hdr_menu.add_command(label="Open")
        self.hdr_menu.add_command(label="Convert_to_mat")
        self.hdr_menu.add_command(label="Convert_to_mat_resize")

        # label
        self.label_json = tk.Label(self, text="Json:")
        self.label_json.grid(row=0, column=0,padx=15, pady=5)
        self.label_count = tk.Label(self, text="Count: ")
        self.label_count.grid(row=1, column=0,padx=15, pady=5)
        self.label_id = tk.Label(self, text="Id: ")
        self.label_id.grid(row=2, column=0,padx=15, pady=5)
        self.label_tif = tk.Label(self, text="TIF:")
        self.label_tif.grid(row=3, column=0,padx=15, pady=5)
        self.label_mat = tk.Label(self, text="Mat:")
        self.label_mat.grid(row=4, column=0,padx=15, pady=5)
        self.label_hdr = tk.Label(self, text="HDR:")
        self.label_hdr.grid(row=5, column=0,padx=15, pady=5)

    # menu
    ## Json
    def bind_json_replace_label(self, command: callable):
        self.json_menu.entryconfig("Replace_label", command=command)

    def bind_json_delete_label(self, command: callable):
        self.json_menu.entryconfig("Delete_label", command=command)

    def bind_json_open(self, command: callable):
        self.json_menu.entryconfig("Open", command=command)

    def bind_json_combine(self, command: callable):
        self.json_menu.entryconfig("Combine", command=command)

    def bind_json_convert_to_tif(self, command: callable):
        self.json_menu.entryconfig("Convert_to_tif", command=command)

    def bind_json_remove_overlap(self, command: callable):
        self.json_menu.entryconfig("Remove_overlap", command=command)

    def bind_json_convert_to_mat(self, command: callable):
        self.json_menu.entryconfig("Convert_to_mat", command=command)
    
    def bind_json_convert_to_mat_resize(self, command: callable):
        self.json_menu.entryconfig("Convert_to_mat_resize", command=command)

    # Tif
    def bind_tif_open(self, command: callable):
        self.tif_menu.entryconfig("Open", command=command)

    def bind_tif_save(self, command: callable):
        self.tif_menu.entryconfig("Save_tif", command=command)

    def bind_tif_draw_label(self, command: callable):
        self.tif_menu.entryconfig("Draw_label", command=command)

    ## Mat
    def bind_mat_open(self, command: callable):
        self.mat_menu.entryconfig("Open", command=command)

    def bind_mat_save(self, command: callable):
        self.mat_menu.entryconfig("Save_mat", command=command)

    def bind_hdr_open(self, command: callable):
        self.hdr_menu.entryconfig("Open", command=command)

    def bind_hdr_convert_to_mat(self, command: callable):
        self.hdr_menu.entryconfig("Convert_to_mat", command=command)

    def bind_hdr_convert_to_mat_resize(self, command: callable):
        self.hdr_menu.entryconfig("Convert_to_mat_resize", command=command)

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

    ## Hdr
    def set_hdr_label(self, text: str):
        self.label_hdr.config(text="HDR: " + text)

    def run(self):
        self.mainloop()
