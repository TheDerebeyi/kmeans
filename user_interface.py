import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import k_means as km
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame()
df_cache = pd.DataFrame()
k_value = 3


def select_file():
    global df_cache
    file_path = filedialog.askopenfilename(
        title="Select .csv File",
        filetypes=[("CSV Files", "*.csv")],  # Only allow CSV files
    )
    file_entry.delete(0, tk.END)  # Clear any previous value
    file_entry.insert(0, file_path)  # Set the selected file path

    df_cache = pd.read_csv(file_path)

    listbox.delete(0, tk.END)

    for column in df_cache.columns:
        listbox.insert(tk.END, column)



def calculate():
    global df, k_value, plot_frame
    k_value = k_entry.get()
    file_path = file_entry.get()  # Replace with the actual path
    #df = pd.read_csv(file_path, index_col='Unnamed: 0')
    df['Cluster'] = km.kmeans(df, int(k_value))
    df.to_csv('results.csv')
    for widget in plot_frame.winfo_children():
        widget.destroy()
    result_label.config(text="Sonuçlar results.csv adlı dosyaya kaydedildi.", fg="red")
    root.after(3000, lambda: result_label.config(text="", fg="black"))
    plot_clusters()


def plot_clusters():
    global df, k_value
    for i in range(1, len(df.columns) - 1):
        # Create a Matplotlib figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))

        # Scatter plot
        scatter = ax.scatter(df.iloc[:, 0], df.iloc[:, i], c=df['Cluster'], cmap='viridis')
        ax.set_xlabel(df.columns[0])
        ax.set_ylabel(df.columns[i])

        # Add a legend
        legend = ax.legend(*scatter.legend_elements(), title='Clusters')
        ax.add_artist(legend)

        # Embed the Matplotlib plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)

        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side="top", fill="both", expand=True)

def preparation():
    global df_cache, df
    selected_indices = listbox.curselection()
    selected_items = [listbox.get(index) for index in selected_indices]
    df_cache.drop(columns=selected_items,inplace=True)
    df = df_cache
    result_label.config(text="Başarılı.", fg="red")
    root.after(3000, lambda: result_label.config(text="", fg="black"))
    listbox.delete(0, tk.END)


# Create the Tkinter window
root = tk.Tk()
root.title("K-Means Clustering")
# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size to be maximized
root.geometry(f"{screen_width}x{screen_height}+0+0")

labelt = tk.Label(root, text="")
labelt.pack()

lframe = ttk.Frame(root)
lframe.pack(side="left", padx=10)

rframe = ttk.Frame(root)
rframe.pack(side="left", padx=10)

# File Selection
select_button = tk.Button(lframe, text="Bir .csv Dosyası Seç", command=select_file)
select_button.pack(pady=10)

file_entry = tk.Entry(lframe, width=50)
file_entry.pack(pady=5)

columns_label = tk.Label(lframe, text="Hesaplamaya dahil etmek istemediğiniz sütunları seçiniz:")
columns_label.pack()

listbox = tk.Listbox(lframe, selectmode=tk.MULTIPLE)
listbox.pack(pady=10)

# File Selection
select_button = tk.Button(lframe, text="Verisetinden Seçili Sütunları Çıkar", command=preparation)
select_button.pack(pady=10)

# k Entry
k_label = tk.Label(rframe, text="K değeri:")
k_label.pack()

k_entry = tk.Entry(rframe, width=10)
k_entry.pack(pady=5)

# Calculate Button
calculate_button = tk.Button(rframe, text="Hesapla", command=calculate)
calculate_button.pack(pady=10)

# Result Label (for displaying messages or results)
result_label = tk.Label(root, text="")
result_label.pack()

# Create a canvas with a frame for scrollable plots
canvas = tk.Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")


def on_mouse_wheel(event):
    if event.delta:
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# Bind the mouse wheel event to control the scrollbar
canvas.bind("<MouseWheel>", on_mouse_wheel)

plot_frame = ttk.Frame(canvas)
plot_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=plot_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)


def start():
    root.mainloop()
