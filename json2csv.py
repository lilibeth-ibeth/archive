import json
import csv
from tkinter import filedialog, messagebox, Tk, Button

def convert_json_to_csv():
    try:
        # Pilih file JSON
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return

        # Baca file
        with open(file_path, 'r', encoding='utf-8') as f:
            first_char = f.read(1)
            f.seek(0)  # Kembali ke awal file
            if first_char == '[':
                # JSON array biasa
                data = json.load(f)
            else:
                # NDJSON (newline-delimited JSON)
                data = [json.loads(line) for line in f if line.strip()]

        # Pastikan data list
        if not isinstance(data, list):
            messagebox.showerror("Error", "File JSON harus berisi list data.")
            return

        # Tentukan nama file output
        output_file = file_path.replace('.json', '.csv')

        # Tulis ke CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

        messagebox.showinfo("Sukses", f"File CSV sudah disimpan di:\n{output_file}")
    except json.JSONDecodeError as e:
        messagebox.showerror("Error", f"File JSON tidak valid: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengonversi file:\n{str(e)}")

# GUI
root = Tk()
root.title("JSON to CSV Converter")
root.geometry("400x200")

button = Button(root, text="Klik di sini untuk Convert", command=convert_json_to_csv)
button.pack(pady=50)

root.mainloop()
