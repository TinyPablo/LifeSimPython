import tkinter as tk
from tkinter import ttk
from functools import partial

def render_label(sim):
    return f"{sim.settings.name}: {'ON' if sim.render_enabled else 'OFF'}"

def toggle_render(sim, btn):
    sim.render_enabled = not sim.render_enabled
    btn.config(
        text=render_label(sim),
        style="Green.TButton" if sim.render_enabled else "Red.TButton"
    )

def launch_render_ui(simulations: list):
    root = tk.Tk()
    root.title("LifeSim Render Control")
    root.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.theme_use("clam")  

    
    style.configure("Red.TButton",
                    background="#e74c3c", foreground="white",
                    font=("Arial", 11), padding=6)
    style.map("Red.TButton",
              background=[("active", "#c0392b")])

    style.configure("Green.TButton",
                    background="#2ecc71", foreground="white",
                    font=("Arial", 11), padding=6)
    style.map("Green.TButton",
              background=[("active", "#27ae60")])

    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    for i, sim in enumerate(simulations):
        style_name = "Red.TButton"
        btn = ttk.Button(frame,
                         text=render_label(sim),
                         style=style_name,
                         width=36)
        btn.grid(row=i, column=0, padx=8, pady=4, sticky="ew")
        btn.config(command=partial(toggle_render, sim, btn))

    root.update_idletasks()
    root.minsize(300, frame.winfo_reqheight() + 20)
    root.resizable(False, False)
    root.mainloop()