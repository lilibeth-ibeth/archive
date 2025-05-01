import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import pandas as pd  # Required for XLSX support
from google_play_scraper import app, reviews_all, reviews
from google_play_scraper.exceptions import NotFoundError

def scrape_app_data():
    try:
        app_id = entry_id.get().strip()
        if not app_id:
            messagebox.showerror("Error", "Please enter an application ID.")
            return

        # Scrape app data from Google Play
        try:
            app_data = app(app_id)
        except NotFoundError:
            messagebox.showerror("Error", "Application ID not found.")
            return
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching app data: {e}")
            return

        # Determine the number of reviews to scrape
        num_reviews_input = entry_num_reviews.get().strip()
        if num_reviews_input.lower() == "semua":
            num_reviews_input = None  # Fetch all reviews
        else:
            try:
                num_reviews_input = int(num_reviews_input)
                if num_reviews_input <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number or 'semua' for all reviews.")
                return

        # Scrape reviews
        all_reviews = reviews_all(app_id, lang="en", country="us", count=num_reviews_input)
        num_reviews = len(all_reviews)

        # Update progress
        label_progress.config(text=f"Total reviews being downloaded: {num_reviews}...")

        # Save file dialog for CSV and XLSX formats
        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        )
        if save_path:
            if save_path.endswith(".csv"):
                # Save app data to CSV
                app_data_copy = app_data.copy()
                app_data_copy.pop('reviews')  # Remove nested reviews before saving main data
                with open(save_path, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(app_data_copy.keys())
                    writer.writerow(app_data_copy.values())

                # Save reviews separately in CSV
                review_path = save_path.replace(".csv", "_reviews.csv")
                with open(review_path, "w", newline="", encoding="utf-8") as review_file:
                    review_writer = csv.writer(review_file)
                    review_writer.writerow(all_reviews[0].keys())  # Header
                    for review in all_reviews:
                        review_writer.writerow(review.values())
            elif save_path.endswith(".xlsx"):
                # Save app data to Excel
                app_df = pd.DataFrame([app_data])
                app_df.to_excel(save_path, index=False)

                # Save reviews to a separate sheet
                review_path = save_path.replace(".xlsx", "_reviews.xlsx")
                reviews_df = pd.DataFrame(all_reviews)
                reviews_df.to_excel(review_path, index=False)
            else:
                messagebox.showerror("Error", "Unsupported file format.")
                return

            messagebox.showinfo("Success", f"App data scraped and saved successfully!\n"
                                           f"Total reviews downloaded: {num_reviews}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

def copy_text():
    entry_id.event_generate("<<Copy>>")

def paste_text():
    entry_id.event_generate("<<Paste>>")

def cut_text():
    entry_id.event_generate("<<Cut>>")

# Create the GUI application
root = tk.Tk()
root.title("Google Play Scraper")
root.geometry("400x300")

label_id = tk.Label(root, text="Enter Application ID:")
label_id.pack(pady=5)

entry_id = tk.Entry(root, width=50)
entry_id.pack(pady=5)

label_num_reviews = tk.Label(root, text="Number of Reviews (or 'semua' for all):")
label_num_reviews.pack(pady=5)

entry_num_reviews = tk.Entry(root, width=50)
entry_num_reviews.pack(pady=5)

# Add context menu for copy, paste, cut
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Copy", command=copy_text)
context_menu.add_command(label="Paste", command=paste_text)
context_menu.add_command(label="Cut", command=cut_text)

entry_id.bind("<Button-3>", show_context_menu)  # Bind right-click to show context menu

btn_scrape = tk.Button(root, text="Scrape App Data", command=scrape_app_data)
btn_scrape.pack(pady=10)

label_progress = tk.Label(root, text="Total reviews being downloaded: 0...")
label_progress.pack(pady=10)

root.mainloop()
