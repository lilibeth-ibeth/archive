import tkinter as tk
from tkinter import filedialog, messagebox

def remove_line_breaks(text):
    """Menghapus line break dan menggabungkan teks."""
    return text.replace('\n', ' ').strip()

def open_file():
    """Membuka file teks untuk diproses."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, file.read())

def process_text():
    """Memproses teks input dan menampilkan hasil."""
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Peringatan", "Teks input tidak boleh kosong!")
        return
    result = remove_line_breaks(text)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

def show_context_menu(event, text_widget):
    """Menampilkan menu klik kanan."""
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Cut", command=lambda: text_widget.event_generate("<<Cut>>"))
    context_menu.add_command(label="Copy", command=lambda: text_widget.event_generate("<<Copy>>"))
    context_menu.add_command(label="Paste", command=lambda: text_widget.event_generate("<<Paste>>"))
    context_menu.add_command(label="Select All", command=lambda: text_widget.event_generate("<<SelectAll>>"))
    context_menu.tk_popup(event.x_root, event.y_root)

# Membuat GUI menggunakan Tkinter
root = tk.Tk()
root.title("Line Break Remover")
root.geometry("700x500")

# Frame Input
input_frame = tk.LabelFrame(root, text="Input Teks", padx=10, pady=10)
input_frame.pack(fill="both", expand=True, padx=10, pady=5)

input_text = tk.Text(input_frame, wrap="word", height=10)
input_text.pack(fill="both", expand=True)
input_text.bind("<Button-3>", lambda event: show_context_menu(event, input_text))

# Tombol untuk Input
input_buttons_frame = tk.Frame(root)
input_buttons_frame.pack(pady=5)

open_button = tk.Button(input_buttons_frame, text="Buka File", command=open_file)
open_button.pack(side="left", padx=5)

process_button = tk.Button(input_buttons_frame, text="Proses", command=process_text)
process_button.pack(side="left", padx=5)

# Frame Output
output_frame = tk.LabelFrame(root, text="Output Teks (Hasil)", padx=10, pady=10)
output_frame.pack(fill="both", expand=True, padx=10, pady=5)

output_text = tk.Text(output_frame, wrap="word", height=10)
output_text.pack(fill="both", expand=True)
output_text.bind("<Button-3>", lambda event: show_context_menu(event, output_text))

# Tombol untuk Output
output_buttons_frame = tk.Frame(root)
output_buttons_frame.pack(pady=5)

exit_button = tk.Button(output_buttons_frame, text="Keluar", command=root.quit)
exit_button.pack(side="left", padx=5)

root.mainloop()
