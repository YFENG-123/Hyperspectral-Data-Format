import tkinter as tk


class JsonView(tk.Toplevel):
    def __init__(self, root: tk.Tk):
        super().__init__(root)
        self.title("Json")
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        print(self.width, self.height)
        self.geometry(
            str(int(self.width / 4))
            + "x"
            + str(int(self.height / 5))
            + "+"
            + str(int(self.width / 4))
            + "+"
            + str(int(self.height / 4))
        )
        """
        # 放置一个可以调节大小的显示图像矩阵的容器
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0, rowspan=6, columnspan=3)

        # 打开一张tif为ndarray
        self.tif = cv2.imread("D:\\Users\\YFENG\\Desktop\\json_convert_to_tif.tif")
        self.tif_ndarray = np.array(self.tif)
        self.tif_image = Image.fromarray(self.tif_ndarray)
        # 等比调整图像大小
        self.tif_image = self.tif_image.resize(
            (int(self.width / 4), int(self.height / 5)), Image.Resampling.LANCZOS
        )
        self.tif_imagetk = ImageTk.PhotoImage(self.tif_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tif_imagetk)
        """

        # 放置label询问x1坐标
        self.label_x1 = tk.Label(self, text="x1:")
        self.label_x1.grid(row=0, column=0, padx=15, pady=5)
        self.entry_x1 = tk.Entry(self)
        self.entry_x1.grid(row=0, column=1, padx=15, pady=5)
        self.label_unit_x1 = tk.Label(self, text="pixel")
        self.label_unit_x1.grid(row=0, column=2, padx=15, pady=5)

        # 放置label询问y1坐标
        self.label_y1 = tk.Label(self, text="y1:")
        self.label_y1.grid(row=1, column=0, padx=15, pady=5)
        self.entry_y1 = tk.Entry(self)
        self.entry_y1.grid(row=1, column=1, padx=15, pady=5)
        self.label_unit_y1 = tk.Label(self, text="pixel")
        self.label_unit_y1.grid(row=1, column=2, padx=15, pady=5)

        ## 放置label询问x2坐标
        self.label_x2 = tk.Label(self, text="x2:")
        self.label_x2.grid(row=2, column=0, padx=15, pady=5)
        self.entry_x2 = tk.Entry(self)
        self.entry_x2.grid(row=2, column=1, padx=15, pady=5)
        self.label_unit_x2 = tk.Label(self, text="pixel")
        self.label_unit_x2.grid(row=2, column=2, padx=15, pady=5)
        ## 放置label询问y2坐标
        self.label_y2 = tk.Label(self, text="y2:")
        self.label_y2.grid(row=3, column=0, padx=15, pady=5)
        self.entry_y2 = tk.Entry(self)
        self.entry_y2.grid(row=3, column=1, padx=15, pady=5)
        self.label_unit_y2 = tk.Label(self, text="pixel")
        self.label_unit_y2.grid(row=3, column=2, padx=15, pady=5)

        ## 放置button
        self.button_ok = tk.Button(self, text="OK")
        self.withdraw()

    def show(self) -> None:
        self.deiconify()

    def close(self) -> None:
        self.withdraw()

    def get_points(self) -> tuple[int, int, int, int]:
        x1 = self.entry_x1.get()
        y1 = self.entry_y1.get()
        x2 = self.entry_x2.get()
        y2 = self.entry_y2.get()
        return (int(x1), int(y1), int(x2), int(y2))

    def bind_ok(self, command: callable) -> None:
        self.button_ok.configure(command=command)
