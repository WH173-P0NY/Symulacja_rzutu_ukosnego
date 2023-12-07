import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

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
        self.start_button = tk.Button(master, text="Start", command=self.start_animation)
        self.start_button.grid(row=4, column=0)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_animation)
        self.stop_button.grid(row=4, column=1)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset_animation)
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

    def start_animation(self):
        if self.ani is not None:
            self.ani.event_source.stop()
            self.reset_animation()
        # Pobieranie danych wejściowych
        try:
            v0 = float(self.v0_entry.get())
            angle = float(self.angle_entry.get())
            x0 = float(self.x0_entry.get())
            y0 = float(self.y0_entry.get())
        except ValueError:
            tk.messagebox.showerror("Błąd danych wejściowych", "Proszę wprowadzić poprawne wartości numeryczne.")
            return None

        # Obliczanie trajektorii i animacja
        x, y, vx, vy, t_flight = self.calculate_trajectory(v0, angle, x0, y0)
        self.ax.set_xlabel("Położenie X [m]")
        self.ax.set_ylabel("Położenie Y [m]")
        # Ustawienie zakresu osi
        max_x = max(x) * 1.1 if max(x) > 0 else 1
        max_y = max(y) * 1.1 if max(y) > 0 else 1
        self.ax.set_xlim(0, max_x)
        self.ax.set_ylim(0, max_y)


        # Obliczanie czasu trwania animacji w milisekundach
        animation_duration_ms = t_flight * 1000  # Przeliczamy sekundy na milisekundy
        frames = len(x)
        interval = animation_duration_ms / frames  # Czas na klatkę

        self.ani = FuncAnimation(self.fig, self.animate, frames=frames, fargs=(x, y, vx, vy), interval=interval)
        self.canvas.draw()

    def stop_animation(self):
        if self.ani is not None:
            self.ani.event_source.stop()

        # Usuwanie wektorów prędkości, aby uniknąć konfliktów przy ponownym uruchomieniu animacji
        if hasattr(self, 'velocity_vector'):
            del self.velocity_vector
        if hasattr(self, 'horizontal_vector'):
            del self.horizontal_vector
        if hasattr(self, 'vertical_vector'):
            del self.vertical_vector

    def reset_animation(self):
        if self.ani is not None:
            self.ani.event_source.stop()
        self.ax.clear()
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_xlabel("Położenie X [m]")
        self.ax.set_ylabel("Położenie Y [m]")
        self.line, = self.ax.plot([], [], lw=2)
        self.canvas.draw()

        # Usunięcie lub resetowanie wektorów prędkości
        if hasattr(self, 'velocity_vector'):
            del self.velocity_vector
        if hasattr(self, 'horizontal_vector'):
            del self.horizontal_vector
        if hasattr(self, 'vertical_vector'):
            del self.vertical_vector

    def calculate_trajectory(self, v0, angle, x0, y0):
        g = 9.81  # przyspieszenie ziemskie
        angle = np.radians(angle)  # konwersja na radiany

        # Składowe prędkości początkowej
        v0x = v0 * np.cos(angle)
        v0y = v0 * np.sin(angle)

        if angle == 0:  # Przypadek dla kąta 0 stopni (rzut poziomy)
            t_flight = np.sqrt(2 * y0 / g)  # Przykładowy czas lotu, można dostosować
            t = np.linspace(0, t_flight, num=50)
            x = x0 + v0x * t
            y = y0 - 0.5 * g * t ** 2
        else:
            # Czas lotu dla rzutu ukośnego
            t_flight = 2 * v0y / g if v0y > 0 else 10
            t = np.linspace(0, t_flight, num=50)

            # Obliczenia trajektorii
            x = x0 + v0x * t
            y = y0 + v0y * t - 0.5 * g * t ** 2

        # Składowe prędkości w każdym punkcie trajektorii
        vx = np.full_like(t, v0x)
        vy = v0y - g * t

        return x, y, vx, vy, t_flight

    def animate(self, i, x, y, vx, vy):
        self.line.set_data(x[:i], y[:i])

        # Aktualizacja wektorów prędkości zamiast rysowania od nowa
        if i > 0 and y[i - 1] > 0:
            # Aktualizacja wektora całkowitej prędkości (czerwony)
            if hasattr(self, 'velocity_vector'):
                self.velocity_vector.set_offsets([x[i - 1], y[i - 1]])
                self.velocity_vector.set_UVC(vx[i - 1], vy[i - 1])
            else:
                self.velocity_vector = self.ax.quiver(x[i - 1], y[i - 1], vx[i - 1], vy[i - 1], color='red', scale=50,
                                                      scale_units='xy', angles='xy')

            # Aktualizacja składowej prędkości w poziomie (niebieski)
            if hasattr(self, 'horizontal_vector'):
                self.horizontal_vector.set_offsets([x[i - 1], y[i - 1]])
                self.horizontal_vector.set_UVC(vx[i - 1], 0)
            else:
                self.horizontal_vector = self.ax.quiver(x[i - 1], y[i - 1], vx[i - 1], 0, color='blue', scale=50,
                                                        scale_units='xy', angles='xy')

            # Aktualizacja składowej prędkości w pionie (zielony)
            if hasattr(self, 'vertical_vector'):
                self.vertical_vector.set_offsets([x[i - 1], y[i - 1]])
                self.vertical_vector.set_UVC(0, vy[i - 1])
            else:
                self.vertical_vector = self.ax.quiver(x[i - 1], y[i - 1], 0, vy[i - 1], color='green', scale=50,
                                                      scale_units='xy', angles='xy')

        return self.line

    def on_close(self):
        # Zatrzymaj animację, jeśli jest aktywna
        if self.ani is not None:
            self.ani.event_source.stop()

        # Zakończ działanie głównej pętli Tkinter
        self.master.quit()
        self.master.destroy()


root = tk.Tk()
app = RzutUkosnyApp(root)
root.mainloop()
