import numpy as np
from matplotlib.animation import FuncAnimation
import tkinter as tk


def start_animation(app):
    if app.ani is not None:
        app.ani.event_source.stop()
        reset_animation(app)
    # Pobieranie danych wejściowych
    try:
        v0 = float(app.v0_entry.get())
        angle = float(app.angle_entry.get())
        x0 = float(app.x0_entry.get())
        y0 = float(app.y0_entry.get())
    except ValueError:
        tk.messagebox.showerror("Błąd danych wejściowych", "Proszę wprowadzić poprawne wartości numeryczne.")
        return None

    # Obliczanie trajektorii i animacja
    x, y, vx, vy, t_flight = calculate_trajectory(v0, angle, x0, y0)
    app.ax.set_xlabel("Położenie X [m]")
    app.ax.set_ylabel("Położenie Y [m]")
    # Ustawienie zakresu osi
    max_x = max(x) * 1.1 if max(x) > 0 else 1
    max_y = max(y) * 1.1 if max(y) > 0 else 1
    app.ax.set_xlim(0, max_x)
    app.ax.set_ylim(0, max_y)

    # Obliczanie czasu trwania animacji w milisekundach
    animation_duration_ms = t_flight * 1000  # Przeliczamy sekundy na milisekundy
    frames = len(x)
    interval = animation_duration_ms / frames  # Czas na klatkę

    app.ani = FuncAnimation(app.fig, lambda i: animate(app, i, x, y, vx, vy), frames=frames, interval=interval)
    app.canvas.draw()


def stop_animation(app):
    if app.ani is not None:
        app.ani.event_source.stop()

    # Usuwanie wektorów prędkości, aby uniknąć konfliktów przy ponownym uruchomieniu animacji
    if hasattr(app, 'velocity_vector'):
        del app.velocity_vector
    if hasattr(app, 'horizontal_vector'):
        del app.horizontal_vector
    if hasattr(app, 'vertical_vector'):
        del app.vertical_vector


def reset_animation(app):
    if app.ani is not None:
        stop_animation(app)
    app.ax.clear()
    app.ax.set_xlim(0, 1)
    app.ax.set_ylim(0, 1)
    app.ax.set_xlabel("Położenie X [m]")
    app.ax.set_ylabel("Położenie Y [m]")
    app.line, = app.ax.plot([], [], lw=2)
    app.canvas.draw()

    # Usunięcie lub resetowanie wektorów prędkości
    if hasattr(app, 'velocity_vector'):
        del app.velocity_vector
    if hasattr(app, 'horizontal_vector'):
        del app.horizontal_vector
    if hasattr(app, 'vertical_vector'):
        del app.vertical_vector


def calculate_trajectory(v0, angle, x0, y0):
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


def animate(app, i, x, y, vx, vy):
    app.line.set_data(x[:i], y[:i])

    # Aktualizacja wektorów prędkości zamiast rysowania od nowa
    if i > 0 and y[i - 1] > 0:
        # Aktualizacja wektora całkowitej prędkości (czerwony)
        if hasattr(app, 'velocity_vector'):
            app.velocity_vector.set_offsets([x[i - 1], y[i - 1]])
            app.velocity_vector.set_UVC(vx[i - 1], vy[i - 1])
        else:
            app.velocity_vector = app.ax.quiver(x[i - 1], y[i - 1], vx[i - 1], vy[i - 1], color='red', scale=50,
                                                  scale_units='xy', angles='xy')

        # Aktualizacja składowej prędkości w poziomie (niebieski)
        if hasattr(app, 'horizontal_vector'):
            app.horizontal_vector.set_offsets([x[i - 1], y[i - 1]])
            app.horizontal_vector.set_UVC(vx[i - 1], 0)
        else:
            app.horizontal_vector = app.ax.quiver(x[i - 1], y[i - 1], vx[i - 1], 0, color='blue', scale=50,
                                                    scale_units='xy', angles='xy')

        # Aktualizacja składowej prędkości w pionie (zielony)
        if hasattr(app, 'vertical_vector'):
            app.vertical_vector.set_offsets([x[i - 1], y[i - 1]])
            app.vertical_vector.set_UVC(0, vy[i - 1])
        else:
            app.vertical_vector = app.ax.quiver(x[i - 1], y[i - 1], 0, vy[i - 1], color='green', scale=50,
                                                  scale_units='xy', angles='xy')

    return app.line