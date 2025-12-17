import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from typing import Optional
from jsonp.view import JsonView
from tif.view import TifView
from mat.view import MatView
from hdr.view import HdrView


class Views(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("数据格式化工具")
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        print(self.width, self.height)
        self.geometry(
            str(int(self.width / 3))
            + "x"
            + str(int(self.height / 4))
            + "+"
            + str(int(self.width / 4))
            + "+"
            + str(int(self.height / 4))
        )

        
        self.json = JsonView(self)
        self.tif = TifView(self)
        self.mat = MatView(self)
        self.hdr = HdrView(self)

        self.menu = tk.Menu(self, tearoff=False)
        self.config(menu=self.menu)

        self.json_menu = tk.Menu(self.menu, tearoff=False)
        self.mat_menu = tk.Menu(self.menu, tearoff=False)
        self.tif_menu = tk.Menu(self.menu, tearoff=False)
        self.hdr_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="Json", menu=self.json_menu)
        # self.menu.add_cascade(label="Mat", menu=self.mat_menu)
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

        # 配置列权重，使窗口可以自动调整大小
        self.columnconfigure(0, weight=1, minsize=300)
        self.rowconfigure(0, weight=1)
        
        # 创建可滚动的 Canvas 和 Scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        # 配置 Canvas 和 Scrollbar
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # 在 Canvas 中创建窗口
        self.canvas_window = self.canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )
        
        # 配置 Canvas 的滚动
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # 当 Canvas 大小改变时，更新内部窗口宽度
        def configure_canvas_window(event):
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        self.canvas.bind('<Configure>', configure_canvas_window)
        
        # 布局 Canvas 和 Scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # 配置可滚动框架的列权重
        self.scrollable_frame.columnconfigure(0, weight=1, minsize=300)
        
        # label - 设置自动换行和左对齐，使用动态 wraplength
        # wraplength 会在窗口大小改变时自动更新
        self.label_json = tk.Label(
            self.scrollable_frame, 
            text="Json:",
            anchor="w",
            justify="left",
            wraplength=350
        )
        self.label_json.grid(
            row=0,
            column=0,
            padx=15,
            pady=5,
            sticky="ew"
        )
        self.label_count = tk.Label(
            self.scrollable_frame, 
            text="Count: ",
            anchor="w",
            justify="left",
            wraplength=350
        )
        self.label_count.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        self.label_id = tk.Label(
            self.scrollable_frame, 
            text="Id: ",
            anchor="w",
            justify="left",
            wraplength=350
        )
        self.label_id.grid(row=2, column=0, padx=15, pady=5, sticky="ew")
        self.label_tif = tk.Label(
            self.scrollable_frame, 
            text="TIF:",
            anchor="w",
            justify="left",
            wraplength=350
        )
        self.label_tif.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
        self.label_mat = tk.Label(
            self.scrollable_frame, 
            text="Mat:",
            anchor="w",
            justify="left",
            wraplength=350
        )
        self.label_mat.grid(row=4, column=0, padx=15, pady=5, sticky="ew")
        self.label_hdr = tk.Label(
            self.scrollable_frame, 
            text="HDR:",
            anchor="w",
            justify="left",
            wraplength=350
        )
        self.label_hdr.grid(row=5, column=0, padx=15, pady=5, sticky="ew")
        
        # 设置窗口最小尺寸
        self.minsize(400, 200)
        
        # 绑定窗口大小改变事件，动态更新 wraplength 和 Canvas 窗口宽度
        self.bind("<Configure>", self._on_window_configure)
        
        # 绑定鼠标滚轮事件
        self._bind_mousewheel()

    # Error
    def show_error(self, message: str):
        messagebox.showerror("错误", message)

    # ask
    def ask_label(self, title: str, message: str) -> str:
        label = simpledialog.askstring(title, message)
        return label

    def ask_resize_coordinates(self) -> Optional[tuple[int, int, int, int]]:
        """
        弹窗输入裁剪坐标参数
        Returns:
            tuple[int, int, int, int] | None: (x1, y1, x2, y2) 或 None（如果用户取消）
        """
        dialog = tk.Toplevel(self)
        dialog.title("输入裁剪坐标")
        dialog.geometry("300x200")
        dialog.transient(self)
        dialog.grab_set()

        # 创建输入框
        tk.Label(dialog, text="x1:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_x1 = tk.Entry(dialog, width=15)
        entry_x1.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(dialog, text="y1:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_y1 = tk.Entry(dialog, width=15)
        entry_y1.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(dialog, text="x2:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_x2 = tk.Entry(dialog, width=15)
        entry_x2.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(dialog, text="y2:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        entry_y2 = tk.Entry(dialog, width=15)
        entry_y2.grid(row=3, column=1, padx=10, pady=5)

        result = [None]

        def confirm():
            try:
                x1 = int(entry_x1.get())
                y1 = int(entry_y1.get())
                x2 = int(entry_x2.get())
                y2 = int(entry_y2.get())
                
                # 验证坐标有效性（考虑对调：x1和y1对调，x2和y2对调）
                # 对调后：新的x1=原y1, 新的y1=原x1, 新的x2=原y2, 新的y2=原x2
                # 所以需要验证：y1 < y2（确保对调后x1 < x2）和 x1 < x2（确保对调后y1 < y2）
                if y1 >= y2 or x1 >= x2:
                    messagebox.showerror("输入错误", "坐标无效：y1 必须小于 y2，x1 必须小于 x2（坐标会对调）")
                    return
                
                result[0] = (x1, y1, x2, y2)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("输入错误", "请输入有效的整数坐标")

        def cancel():
            dialog.destroy()

        # 按钮
        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(btn_frame, text="确定", command=confirm, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="取消", command=cancel, width=10).pack(side=tk.LEFT, padx=5)

        # 等待对话框关闭
        dialog.wait_window()
        
        return result[0]

    def ask_open_path_list(self, file_type: str, suffix: str) -> list:
        file_path = filedialog.askopenfilenames(
            filetypes=[(file_type, "*" + suffix)], defaultextension=suffix
        )

        return file_path
    def ask_open_path(self, file_type: str, suffix: str) -> str:
        file_path = filedialog.askopenfilename(
            filetypes=[(file_type, "*" + suffix)], defaultextension=suffix
        )

        return file_path

    def ask_save_path(self, file_type: str, suffix: str, name: str) -> str:
        file_path = filedialog.asksaveasfilename(
            filetypes=[(file_type, "*" + suffix)],
            defaultextension=suffix,
            initialfile=name,
        )

        return file_path

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
        self._update_window_size()

    def set_count_label(self, text: str):
        self.label_count.config(text="Count: " + text)
        self._update_window_size()

    def set_id_label(self, text: str):
        self.label_id.config(text="Id: " + text)
        self._update_window_size()

    ## Tif
    def set_tif_label(self, text: str):
        self.label_tif.config(text="TIF: " + text)
        self._update_window_size()

    ## Mat
    def set_mat_label(self, text: str):
        self.label_mat.config(text="Mat: " + text)
        self._update_window_size()

    ## Hdr
    def set_hdr_label(self, text: str):
        self.label_hdr.config(text="HDR: " + text)
        self._update_window_size()
    
    def _on_window_configure(self, event=None):
        """窗口大小改变时，更新所有 label 的 wraplength 和 Canvas 窗口宽度"""
        if event and event.widget == self:
            # 获取窗口宽度
            window_width = self.winfo_width()
            # 计算合适的 wraplength（窗口宽度减去 padding 和滚动条宽度）
            wraplength = max(300, window_width - 70)
            
            # 更新所有 label 的 wraplength
            for label in [self.label_json, self.label_count, self.label_id, 
                         self.label_tif, self.label_mat, self.label_hdr]:
                label.config(wraplength=wraplength)
            
            # 更新 Canvas 窗口宽度，使其与 Canvas 宽度一致
            self.canvas.itemconfig(self.canvas_window, width=window_width - 20)
    
    def _bind_mousewheel(self):
        """绑定鼠标滚轮事件"""
        def _on_mousewheel(event):
            # 在 Windows 和 Linux 上使用不同的滚轮事件
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _on_mousewheel_linux(event):
            # Linux 上的滚轮事件
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
        
        # 绑定到 Canvas 和可滚动框架
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind_all("<Button-4>", _on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", _on_mousewheel_linux)
        
        # 当鼠标进入 Canvas 区域时，确保可以滚动
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())
    
    def _update_window_size(self):
        """更新窗口大小以适应内容"""
        try:
            # 更新窗口以计算实际需要的尺寸
            self.update_idletasks()
            
            # 更新 Canvas 的滚动区域
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # 获取当前窗口尺寸
            current_width = self.winfo_width()
            current_height = self.winfo_height()
            
            # 计算内容所需的最小宽度（考虑所有label）
            min_width = 400
            for label in [self.label_json, self.label_count, self.label_id, 
                         self.label_tif, self.label_mat, self.label_hdr]:
                label.update_idletasks()
                # 获取label的实际宽度需求
                req_width = label.winfo_reqwidth()
                if req_width > min_width:
                    min_width = min(req_width + 50, 800)  # 限制最大宽度为800
            
            # 如果当前宽度小于所需宽度，调整窗口大小
            if current_width < min_width:
                self.geometry(f"{min_width}x{current_height}")
                # 更新 wraplength 和 Canvas 窗口宽度
                self._on_window_configure()
            
            # 更新 Canvas 窗口宽度
            self.canvas.itemconfig(self.canvas_window, width=current_width - 20)
        except Exception:
            # 如果调整大小失败，忽略错误
            pass

    def run(self):
        self.mainloop()
