import tkinter as tk
from PIL import Image, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import database
import mood_logic

# Initialize DB
database.init_db()

# Window
app = ttk.Window(themename="flatly")
app.title("Mood To-Do App")
app.geometry("600x700")

# -------------------------------
# GRADIENT BACKGROUND
# -------------------------------
gradient = tk.Canvas(app, width=600, height=700, highlightthickness=0)
gradient.place(x=0, y=0)

for i in range(700):
    color = f"#%02x%02x%02x" % (255, 240 - i // 4, 255 - i // 5)
    gradient.create_line(0, i, 600, i, fill=color)

# Optional Background Image
try:
    img = Image.open("background.jpg")
    img = img.resize((600, 700))
    bg_photo = ImageTk.PhotoImage(img)
    bg_label = tk.Label(app, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    pass

# --------------------------------
# MAIN CARD (solid white panel)
# --------------------------------
main_card = tk.Frame(app, bg="#ffffff", bd=2, relief="groove")
main_card.place(x=30, y=50, width=540, height=600)

title = ttk.Label(
    main_card,
    text="Mood-Based To-Do List",
    font=("Segoe UI", 20, "bold"),
    bootstyle="primary"
)
title.pack(pady=15)

# ---------------------------
# MOOD SELECTOR
# ---------------------------
def set_mood_bg(mood):
    color_map = {
        "happy": "#fff7cc",
        "stressed": "#ffdede",
        "tired": "#e0e7ff",
        "sad": "#f3e8ff"
    }
    bg = color_map.get(mood, "#ffffff")
    main_card.config(bg=bg)

mood_frame = ttk.Frame(main_card)
mood_frame.pack(pady=10)

ttk.Label(mood_frame, text="Your Mood").grid(row=0, column=0, padx=5)

mood_var = ttk.StringVar()
mood_dropdown = ttk.Combobox(
    mood_frame,
    textvariable=mood_var,
    values=list(mood_logic.MOOD_MAP.keys()),
    width=15,
    bootstyle=INFO
)
mood_dropdown.grid(row=0, column=1, padx=5)

def suggest_tasks():
    mood = mood_var.get()
    if not mood:
        messagebox.showinfo("Info", "Select a mood first.")
        return

    set_mood_bg(mood)

    categories = mood_logic.suggest_categories(mood)
    tasks = database.get_tasks_by_categories(categories)

    win = ttk.Toplevel(title="Suggestions")
    win.geometry("350x350")

    ttk.Label(win, text="Suggested Tasks", font=("Segoe UI", 14, "bold")).pack(pady=10)

    lb = tk.Listbox(win, width=45, height=12, bg="white", fg="black")
    lb.pack(pady=10)

    if not tasks:
        lb.insert(tk.END, "No matching tasks found.")
        return

    for t in tasks:
        icon = "✔" if t[4] else "•"
        lb.insert(tk.END, f"{t[0]}. {t[1]}  [{t[2]}] ({t[3]}) {icon}")

ttk.Button(mood_frame, text="Suggest Tasks", bootstyle=SUCCESS, command=suggest_tasks)\
    .grid(row=0, column=2, padx=10)

# ------------------------------------
# TASK LIST (TK Listbox)
# ------------------------------------
task_list = tk.Listbox(main_card, width=60, height=15, bg="white", fg="black")
task_list.pack(pady=15)

def load_tasks():
    task_list.delete(0, tk.END)
    for t in database.get_all_tasks():
        icon = "✔" if t[4] else "•"
        task_list.insert(tk.END, f"{t[0]}. {t[1]}  [{t[2]}] ({t[3]}) {icon}")

load_tasks()

# -----------------------------
# ADD TASK POPUP
# -----------------------------
def open_add_window():
    win = ttk.Toplevel(title="Add Task")
    win.geometry("350x330")

    ttk.Label(win, text="Title").pack(pady=5)
    title_entry = ttk.Entry(win, width=30)
    title_entry.pack()

    ttk.Label(win, text="Category").pack(pady=5)
    category_entry = ttk.Entry(win, width=30)
    category_entry.pack()

    ttk.Label(win, text="Mood Tag").pack(pady=5)
    mood_entry = ttk.Entry(win, width=30)
    mood_entry.pack()

    def save_task():
        t = title_entry.get()
        c = category_entry.get()
        m = mood_entry.get()

        if not t or not c or not m:
            messagebox.showwarning("Warning", "All fields required.")
            return

        database.add_task(t, c, m)
        load_tasks()
        win.destroy()

    ttk.Button(win, text="Save Task", bootstyle=SUCCESS, command=save_task).pack(pady=15)

# ---------------------------------
# BUTTONS
# ---------------------------------
btn_frame = ttk.Frame(main_card)
btn_frame.pack(pady=5)

def mark_done():
    s = task_list.curselection()
    if not s:
        return
    task_id = int(task_list.get(s).split(".")[0])
    database.mark_done(task_id)
    load_tasks()

def delete_task():
    s = task_list.curselection()
    if not s:
        return
    task_id = int(task_list.get(s).split(".")[0])
    database.delete_task(task_id)
    load_tasks()

ttk.Button(btn_frame, text="Add Task", width=15, bootstyle=PRIMARY, command=open_add_window)\
    .grid(row=0, column=0, padx=5)

ttk.Button(btn_frame, text="Mark Done", width=15, bootstyle=SUCCESS, command=mark_done)\
    .grid(row=0, column=1, padx=5)

ttk.Button(btn_frame, text="Delete Task", width=15, bootstyle=DANGER, command=delete_task)\
    .grid(row=0, column=2, padx=5)

# Run the app
app.mainloop()
