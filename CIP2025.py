import tkinter as tk
import math
import random

G = 6.67430e-1 

class Star:
    def __init__(self, canvas, x, y, mass=5000, radius=30, color="yellow"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color

    def draw(self):
        for i in range(5, 0, -1):
            alpha = int(50 * (6 - i))
            fill_color = f"#{alpha:02x}{alpha:02x}00"
            self.canvas.create_oval(
                self.x - self.radius * i * 0.15,
                self.y - self.radius * i * 0.15,
                self.x + self.radius * i * 0.15,
                self.y + self.radius * i * 0.15,
                fill=fill_color, outline=""
            )
        self.canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill=self.color, outline=""
        )

class Planet:
    def __init__(self, canvas, x, y, vx, vy, mass=10, color="blue"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.color = color
        self.radius = max(4, int(math.log(mass + 1)*2))
        self.trail = []

    def update(self, star, dt):
        dx = star.x - self.x
        dy = star.y - self.y
        dist_sq = dx**2 + dy**2
        dist = math.sqrt(dist_sq) if dist_sq != 0 else 0.01

        a = G * star.mass / dist_sq
        ax = a * dx / dist
        ay = a * dy / dist

        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        self.trail.append((self.x, self.y))
        if len(self.trail) > 30:
            self.trail.pop(0)

    def draw(self):
        for i, (tx, ty) in enumerate(self.trail):
            size = max(1, int(self.radius * (i / len(self.trail))))
            self.canvas.create_oval(tx - size, ty - size, tx + size, ty + size,
                                    fill=self.color, outline="")
        self.canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill=self.color, outline=""
        )

class Universe:
    def __init__(self, root):
        self.width = 900
        self.height = 700

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.star = Star(self.canvas, self.width // 2, self.height // 2)
        self.planets = []

        self.canvas.bind("<Button-1>", self.add_planet)

        #RESET
        self.reset_btn = tk.Button(root, text="Reset", command=self.reset_simulation)
        self.reset_btn.pack(pady=5)

        self.update_frame()

    def add_planet(self, event):
        vx = random.uniform(-2, 2)
        vy = random.uniform(-2, 2)
        mass = random.uniform(5, 20)
        colors = ["#1f77b4", "#2ca02c", "#d62728", "#9467bd", "#ff7f0e"]
        color = random.choice(colors)
        planet = Planet(self.canvas, event.x, event.y, vx, vy, mass, color)
        self.planets.append(planet)

    def reset_simulation(self):
        self.planets = []  

    def update_frame(self):
        self.canvas.delete("all")
        self.star.draw()
        for planet in self.planets:
            planet.update(self.star, dt=0.5)
            planet.draw()
        self.canvas.after(30, self.update_frame)

def main():
    root = tk.Tk()
    root.title("Simple Solar Simulator")
    Universe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
