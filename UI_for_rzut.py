import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from logic_for_rzut import start_animation, reset_animation, stop_animation

class RzutUkosnyApp:
    def __init__(self, master):
        self.master = master
        master.title("Symulacja Rzutu Ukośnego")

        # Etykiety i pola tekstowe
        tk.Label(master, text="Prędkość początkowa (m/s):").grid(row=0, column=0)
        self.v0_entry = tk.Entry(master)
        self.v0_entry.grid(row=0, column=1)
        self.v0_entry.insert(0, "20")

        tk.Label(master, text="Kąt wyrzutu (stopnie):").grid(row=1, column=0)
        self.angle_entry = tk.Entry(master)
        self.angle_entry.grid(row=1, column=1)
        self.angle_entry.insert(0, "45")

        tk.Label(master, text="Początkowa pozycja x:").grid(row=2, column=0)
        self.x0_entry = tk.Entry(master)
        self.x0_entry.grid(row=2, column=1)
        self.x0_entry.insert(0, "0")

        tk.Label(master, text="Początkowa pozycja y:").grid(row=3, column=0)
        self.y0_entry = tk.Entry(master)
        self.y0_entry.grid(row=3, column=1)
        self.y0_entry.insert(0, "0")

        # Przyciski
        self.start_button = tk.Button(master, text="Start", command=lambda: start_animation(self))
        self.start_button.grid(row=4, column=0)

        self.stop_button = tk.Button(master, text="Stop", command=lambda: stop_animation(self))
        self.stop_button.grid(row=4, column=1)

        self.reset_button = tk.Button(master, text="Reset", command=lambda: reset_animation(self))
        self.reset_button.grid(row=5, column=0)

        # Ustawienia wykresu
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_xlabel("Położenie X [m]")
        self.ax.set_ylabel("Położenie Y [m]")
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=6, column=0, columnspan=2)

        # Dodanie zdarzeni by aplikacja przestała działać po wyłączeniu GUI
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Inicjalizacja animacji
        self.ani = None

    def on_close(self):
        # Zatrzymaj animację, jeśli jest aktywna
        if self.ani is not None:
            self.ani.event_source.stop()

        # Zakończ działanie głównej pętli Tkinter
        self.master.quit()
        self.master.destroy()
