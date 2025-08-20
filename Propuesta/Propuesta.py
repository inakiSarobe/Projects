import tkinter as tk
import random
import math

BG_COLOR = "#FFEFF6"
PANEL_COLOR = "#FFF5FB"
ACCENT = "#FF6FA3"
TEXT_COLOR = "#4A2A3A"
FONT_TITLE = ("Helvetica", 26, "bold")
FONT_SUB = ("Helvetica", 14)
FONT_BTN = ("Helvetica", 12, "bold")

WINDOW_WIDTH = 520
WINDOW_HEIGHT = 340

MIN_DISTANCE = 120

person_name = "Yera"  # Nombre de la persona a la que se le propone


class PropuestaApp:
    def __init__(self, root):
        self.root = root
        root.title(f"Propuesta a {person_name}!")
        root.configure(bg=BG_COLOR)
        root.resizable(False, False)

        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        x = (screen_w - WINDOW_WIDTH) // 2
        y = (screen_h - WINDOW_HEIGHT) // 2
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        self.panel = tk.Frame(root, bg=PANEL_COLOR, bd=0, relief=tk.FLAT)
        self.panel.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=480, height=300)

        self.canvas = tk.Canvas(self.panel, bg=PANEL_COLOR, highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._draw_decor()

        self.label = tk.Label(self.panel, text="¿Quieres ser mi novia?", bg=PANEL_COLOR,
                              fg=TEXT_COLOR, font=FONT_TITLE)
        self.label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

        subtext = "Te prometo muchas risas, apoyo y abrazos. 🌸💖"
        self.sub = tk.Label(self.panel, text=subtext, bg=PANEL_COLOR, fg=TEXT_COLOR, font=FONT_SUB)
        self.sub.place(relx=0.5, rely=0.37, anchor=tk.CENTER)

        self.btn_yes = tk.Button(self.panel, text="Sí 💕", font=FONT_BTN, bg=ACCENT, fg="white",
                                 activebackground="#ff7fb3", activeforeground="white",
                                 bd=0, padx=14, pady=8, command=self.she_said_yes)
        self.btn_yes.place(relx=0.33, rely=0.72, anchor=tk.CENTER)

        self.btn_no = tk.Button(self.panel, text="No 😅", font=FONT_BTN, bg="#F3C6D6", fg=TEXT_COLOR,
                                bd=0, padx=14, pady=8)
        self.no_relx = 0.67
        self.no_rely = 0.72
        self.btn_no.place(relx=self.no_relx, rely=self.no_rely, anchor=tk.CENTER)

        self.btn_no.bind('<Enter>', self._on_no_enter)
        self.panel.bind('<Motion>', self._panel_motion_check)
        self.btn_no.bind('<Button-1>', self._on_no_click)

        self.celebrate_running = False

    def _draw_decor(self):
        positions = [(30, 30), (440, 20), (420, 80), (50, 240), (430, 240)]
        for (x, y) in positions:
            self._draw_heart(x, y, size=12, fill="#FF9AC2")
        self._draw_flower(240, 70, size=22)

    def _draw_heart(self, x, y, size=10, fill="#FF8DB0"):
        s = size
        self.canvas.create_oval(x - s, y - s, x, y, fill=fill, outline=fill)
        self.canvas.create_oval(x, y - s, x + s, y, fill=fill, outline=fill)
        points = [x - s, y, x + s, y, x, y + s + s // 2]
        self.canvas.create_polygon(points, fill=fill, outline=fill)

    def _draw_flower(self, x, y, size=20):
        for i in range(6):
            ang = math.radians(i * 60)
            dx = math.cos(ang) * size
            dy = math.sin(ang) * size
            self.canvas.create_oval(x + dx - size/2, y + dy - size/2,
                                    x + dx + size/2, y + dy + size/2, fill="#FFD8EA", outline="")
        self.canvas.create_oval(x - size/3, y - size/3, x + size/3, y + size/3, fill="#FFB6D5", outline="")

    def _on_no_enter(self, event=None):
        self.move_no_button()

    def _on_no_click(self, event=None):
        self.move_no_button()
        return "break"

    def _panel_motion_check(self, event):
        try:
            x_root = event.x_root
            y_root = event.y_root
            bx1 = self.btn_no.winfo_rootx()
            by1 = self.btn_no.winfo_rooty()
            bx2 = bx1 + self.btn_no.winfo_width()
            by2 = by1 + self.btn_no.winfo_height()
            if bx1 <= x_root <= bx2 and by1 <= y_root <= by2:
                self.move_no_button()
        except Exception:
            pass

    def move_no_button(self, event=None):
        self.panel.update_idletasks()

        pw = self.panel.winfo_width()
        ph = self.panel.winfo_height()
        bw = self.btn_no.winfo_reqwidth()
        bh = self.btn_no.winfo_reqheight()

        bsw = self.btn_yes.winfo_reqwidth()
        bsh = self.btn_yes.winfo_reqheight()
        bx = self.btn_yes.winfo_x()
        by = self.btn_yes.winfo_y()

        pointer_x_root = self.root.winfo_pointerx()
        pointer_y_root = self.root.winfo_pointery()
        panel_root_x = self.panel.winfo_rootx()
        panel_root_y = self.panel.winfo_rooty()
        pointer_x = pointer_x_root - panel_root_x
        pointer_y = pointer_y_root - panel_root_y

        min_x = 8
        min_y = int(ph * 0.55)
        max_x = max(min_x, pw - bw - 8)
        max_y = max(min_y, ph - bh - 8)

        attempts = 0
        chosen = None
        while attempts < 300:
            attempts += 1
            nx = random.randint(min_x, max_x)
            ny = random.randint(min_y, max_y)
            cx = nx + bw / 2
            cy = ny + bh / 2
            dx = cx - pointer_x
            dy = cy - pointer_y
            dist = math.hypot(dx, dy)
            si_x1 = bx - 40
            si_x2 = bx + bsw + 40
            si_y1 = by - 20
            si_y2 = by + bsh + 20
            inside_si = (si_x1 <= nx <= si_x2 and si_y1 <= ny <= si_y2)
            if dist >= MIN_DISTANCE and not inside_si:
                chosen = (nx, ny)
                break

        if chosen is None:
            cur_x = int(self.btn_no.winfo_x())
            cur_y = int(self.btn_no.winfo_y())
            nx = max(min_x, min(max_x, pw - cur_x - bw))
            ny = max(min_y, min(max_y, ph - cur_y - bh))
            chosen = (nx, ny)

        nx, ny = chosen
        relx = nx / pw
        rely = ny / ph
        relx = max(0.08, min(0.92, relx))
        rely = max(0.55, min(0.92, rely))

        self.btn_no.place_configure(relx=relx, rely=rely, anchor=tk.CENTER)

    def she_said_yes(self):
        if self.celebrate_running:
            return
        self.celebrate_running = True

        for w in (self.label, self.sub, self.btn_yes, self.btn_no, self.canvas):
            try:
                w.place_forget()
            except Exception:
                try:
                    w.place_forget()
                except Exception:
                    pass

        lbl = tk.Label(self.panel, text="¡Sabía que dirías que sí! 💕", font=("Helvetica", 20, "bold"),
                       bg=PANEL_COLOR, fg=TEXT_COLOR)
        lbl.place(relx=0.5, rely=0.18, anchor=tk.CENTER)

        message = (
            f"{person_name}, desde que te conozco mi mundo es más brillante.\n"
            "Prometo escucharte, cuidarte y llenarte de abrazos.\n"
            "Te quiero con todo mi corazón. 💖🌸"
        )
        txt = tk.Label(self.panel, text=message, font=("Helvetica", 12), bg=PANEL_COLOR, fg=TEXT_COLOR, justify=tk.CENTER)
        txt.place(relx=0.5, rely=0.33, anchor=tk.CENTER)

        anim = tk.Canvas(self.panel, width=420, height=140, bg=PANEL_COLOR, highlightthickness=0)
        anim.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        particles = []
        for i in range(28):
            x = random.randint(10, 390)
            y = random.randint(10, 120)
            size = random.randint(6, 14)
            kind = random.choice(["heart", "dot"])
            color = random.choice(["#FF6FA3", "#FFD1E6", "#FFB3D1", "#FF7BA9"])
            if kind == "heart":
                pid = self._create_tiny_heart(anim, x, y, size, color)
            else:
                pid = anim.create_oval(x, y, x + size, y + size, fill=color, outline=color)
            dx = random.uniform(-1.6, 1.6)
            dy = random.uniform(-2, 0.4)
            particles.append([pid, x, y, dx, dy])

        def animate():
            alive = False
            for p in particles:
                pid, x, y, dx, dy = p
                y += dy
                x += dx
                dy += 0.12
                anim.move(pid, dx, dy)
                p[1], p[2], p[3], p[4] = x, y, dx, dy
                if y < 160:
                    alive = True
            if alive:
                self.root.after(30, animate)
            else:
                self._show_final_heart_on_panel()

        animate()

    def _create_tiny_heart(self, canvas, x, y, size, color):
        s = size // 2
        o1 = canvas.create_oval(x - s, y - s, x, y, fill=color, outline=color)
        o2 = canvas.create_oval(x, y - s, x + s, y, fill=color, outline=color)
        p = canvas.create_polygon([x - s, y, x + s, y, x, y + s], fill=color, outline=color)
        return p

    def _show_final_heart_on_panel(self):
        for child in self.panel.winfo_children():
            pass
        c = tk.Canvas(self.panel, width=220, height=160, bg=PANEL_COLOR, highlightthickness=0)
        c.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        x = 110
        y = 70
        size = 60
        s = size
        c.create_oval(x - s, y - s, x, y, fill=ACCENT, outline=ACCENT)
        c.create_oval(x, y - s, x + s, y, fill=ACCENT, outline=ACCENT)
        points = [x - s, y, x + s, y, x, y + s + s // 2]
        c.create_polygon(points, fill=ACCENT, outline=ACCENT)

        lbl = tk.Label(self.panel, text=f"Te Amo, {person_name} 💞", font=("Helvetica", 16, "bold"), bg=PANEL_COLOR, fg=TEXT_COLOR)
        lbl.place(relx=0.5, rely=0.72, anchor=tk.CENTER)

        btn_close = tk.Button(self.panel, text="Cerrar", command=self.root.destroy, bg="#F6A3C3", fg="white", bd=0, padx=12, pady=6)
        btn_close.place(relx=0.5, rely=0.92, anchor=tk.CENTER)


if __name__ == '__main__':
    root = tk.Tk()
    app = PropuestaApp(root)
    root.mainloop()
