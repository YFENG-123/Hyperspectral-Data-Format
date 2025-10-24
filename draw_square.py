import matplotlib.pyplot as plt
import cv2


selected = False
selected_point = [0,0]
plt.gca().add_patch(plt.Rectangle((0, 0), 0, 0, fill=False, edgecolor='red', linewidth=2))


def onclick(event):
    global selected, selected_point
    if event.xdata and event.ydata is not None:

        if selected:
            pass
        else:
            selected_point = [event.xdata, event.ydata]
        selected = not selected
        print(selected)
        print(f"Clicked at: ({event.xdata}, {event.ydata})")

def update(event):
    global selected, selected_point
    if event.xdata and event.ydata is not None:
        if selected:
            #擦除上次绘制的方框
            plt.gca().patches[-1].remove()

            # 绘制新的方框
            plt.gca().add_patch(plt.Rectangle((selected_point[0], selected_point[1]), event.xdata - selected_point[0], event.ydata - selected_point[1], fill=False, edgecolor='red', linewidth=2))
            plt.draw()
        else:
            pass 
        
        print(selected)
        print(f"Clicked at: ({event.xdata}, {event.ydata})")
   
   
# 读取并显示图像
image_tif = cv2.imread("C:\\Users\\zzh\\Desktop\\1.tif")
plt.imshow(image_tif)

# 连接鼠标点击事件
plt.connect('button_press_event', onclick)
plt.connect('motion_notify_event', update)
plt.show()
