import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class FittsLawFromScreenshot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Закон Фиттса")
        self.root.geometry("900x700")

        # Переменные для изображения
        self.image_path = None
        self.original_image = None
        self.tk_image = None
        self.image_on_canvas = None
        self.canvas = tk.Canvas(self.root, bg='gray', cursor='cross')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Переменные для выделения кнопки
        self.rect_id = None
        self.start_x = None
        self.start_y = None
        self.button_bbox = None
        self.button_width = None
        self.button_height = None
        self.button_center = None
        self.S = None
        self.W = None

        # Данные эксперимента
        self.data = []
        self.start_point = None

        # Интерфейсные кнопки
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(control_frame, text="Загрузить скриншот", command=self.load_image).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(control_frame, text="Сбросить выделение кнопки", command=self.reset_button_selection).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Сбросить все опыты", command=self.reset_data).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Аппроксимировать", command=self.fit).pack(side=tk.LEFT, padx=5)

        self.info_label = tk.Label(control_frame, text="Загрузите скриншот и выделите кнопку (зажмите левую кнопку мыши, растяните прямоугольник).", fg="blue")
        self.info_label.pack(side=tk.LEFT, padx=10)

        self.counter_label = tk.Label(control_frame, text="Опытов: 0")
        self.counter_label.pack(side=tk.RIGHT, padx=10)

        # Привязка событий для выделения кнопки
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # Привязка для эксперимента (клики по canvas)
        self.canvas.bind("<Button-1>", self.on_click_for_experiment, add='+')


    def load_image(self):
        """Загрузка изображения"""
        file_path = filedialog.askopenfilename(
            title="Выберите скриншот",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if not file_path:
            return
        self.image_path = file_path
        self.original_image = Image.open(file_path)
        self.display_image()
        self.reset_button_selection()
        self.reset_data()
        self.info_label.config(text="Изображение загружено. Выделите область кнопки (зажмите и растяните).")


    def display_image(self):
        """Отображение загруженной картинки"""
        if self.original_image is None:
            return
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 800, 600
        img_width, img_height = self.original_image.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        resized = self.original_image.resize((new_width, new_height), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)
        self.canvas.delete("all")
        self.image_on_canvas = self.canvas.create_image(
            canvas_width//2, canvas_height//2, anchor=tk.CENTER, image=self.tk_image
        )
        self.img_x0 = (canvas_width - new_width) // 2
        self.img_y0 = (canvas_height - new_height) // 2
        self.img_width = new_width
        self.img_height = new_height
        self.scale = ratio


    def reset_button_selection(self):
        """Удаляет прямогульник после опыта"""
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            self.rect_id = None
        self.button_bbox = None
        self.button_width = None
        self.button_height = None
        self.button_center = None
        self.S = None
        self.W = None
        self.info_label.config(text="Выделите кнопку (зажмите и растяните прямоугольник).")


    def on_mouse_down(self, event):
        """Обработчик лкм запоминает началью позицию лкм, если он попал в область изображения"""
        # Проверяем, попал ли клик в область изображения
        if not (self.img_x0 <= event.x <= self.img_x0 + self.img_width and
                self.img_y0 <= event.y <= self.img_y0 + self.img_height):
            return
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y,
                                                    outline='red', width=2, dash=(4,2))


    def on_mouse_move(self, event):
        """Обработчик для рисования прямоугольника(область кнопки)"""
        if self.start_x is None:
            return
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)


    def on_mouse_up(self, event):
        """Обработчик который расчитывает параметры кнопки"""
        if self.start_x is None:
            return
        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x, event.y
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if x2 - x1 < 5 or y2 - y1 < 5:
            self.canvas.delete(self.rect_id)
            self.rect_id = None
            self.start_x = None
            return
        self.button_bbox = (x1, y1, x2, y2)
        self.button_width = x2 - x1
        self.button_height = y2 - y1
        self.S = self.button_width * self.button_height
        self.W = math.sqrt(self.S)
        self.button_center = ((x1 + x2)//2, (y1 + y2)//2)
        self.info_label.config(text=f"Кнопка выделена: ширина={self.button_width}px, высота={self.button_height}px, S={self.S}px², W={self.W:.1f}px. Теперь проводите опыты: кликните вне кнопки → затем кликните внутри кнопки.")
        self.start_x = None
        self.canvas.create_oval(self.button_center[0]-3, self.button_center[1]-3,
                                self.button_center[0]+3, self.button_center[1]+3,
                                fill='green', tags='center_marker')
        self.root.after(2000, lambda: self.canvas.delete('center_marker'))


    def on_click_for_experiment(self, event):
        """Обработчик для опыта"""
        # Обработка кликов для опытов
        if self.button_bbox is None:
            self.info_label.config(text="Сначала выделите кнопку!")
            return
        x, y = event.x, event.y
        x1, y1, x2, y2 = self.button_bbox
        if x1 <= x <= x2 and y1 <= y <= y2:
            # Клик внутри кнопки – завершаем опыт
            if self.start_point is not None:
                x0, y0, t0 = self.start_point
                t1 = time.time()
                D = math.hypot(x0 - self.button_center[0], y0 - self.button_center[1])
                T = t1 - t0
                self.data.append((D, T))
                self.counter_label.config(text=f"Опытов: {len(self.data)}")
                self.info_label.config(text=f"Опыт {len(self.data)}: D={D:.1f} px, T={T:.3f} с. Продолжайте.")
                self.start_point = None
            else:
                self.info_label.config(text="Сначала задайте начальную точку (клик вне кнопки).")
        else:
            # Клик вне кнопки – задаём начальную точку
            if self.start_point is None:
                self.start_point = (x, y, time.time())
                self.info_label.config(text=f"Начальная точка ({x},{y}). Теперь кликните внутри кнопки.")
            else:
                self.info_label.config(text="Начальная точка уже задана. Кликните внутри кнопки, чтобы завершить опыт.")


    def reset_data(self):
        """Сброс всех данных об экспереметах"""
        self.data = []
        self.start_point = None
        self.counter_label.config(text="Опытов: 0")
        self.info_label.config(text="Данные опытов сброшены. Продолжайте эксперимент.")


    def fit(self):
        """Аппроксимация собранных данных"""
        if len(self.data) < 2:
            messagebox.showwarning("Недостаточно данных", "Нужно хотя бы 2 опыта.")
            return
        IDs = []
        Ts = []
        for D, T in self.data:
            ID = math.log2(D / self.W + 1)
            IDs.append(ID)
            Ts.append(T)
        slope, intercept, r_value, _, _ = stats.linregress(IDs, Ts)
        a, b = intercept, slope
        r2 = r_value**2
        result_text = (f"Результаты аппроксимации (n={len(self.data)}):\n"
                       f"a = {a:.4f} с\nb = {b:.4f} с/бит\n"
                       f"R² = {r2:.4f}\n"
                       f"T = {a:.3f} + {b:.3f} * log₂(D/{self.W:.1f} + 1)")
        self.info_label.config(text=result_text)
        # График
        plt.figure(figsize=(6,4))
        plt.scatter(IDs, Ts, label='Экспериментальные данные')
        x_line = np.array([min(IDs), max(IDs)])
        y_line = a + b * x_line
        plt.plot(x_line, y_line, 'r', label=f'Аппроксимация: T = {a:.3f} + {b:.3f}·ID')
        plt.xlabel('Индекс сложности ID = log₂(D/W+1) (бит)')
        plt.ylabel('Время движения T (с)')
        plt.title('Закон Фиттса по данным эксперимента')
        plt.legend()
        plt.grid(True)
        plt.show()


    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = FittsLawFromScreenshot()
    app.run()