
import tkinter as tk
from tkinter import ttk, messagebox
import requests

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
        self.currencies = self.get_currency_list()

        self.create_widgets()

    def get_currency_list(self):
        try:
            response = requests.get(self.api_url)
            data = response.json()
            return list(data["rates"].keys())
        except:
            messagebox.showerror("Error", "Unable to fetch currency data.")
            return []

    def convert(self):
        try:
            from_currency = self.from_currency_cb.get()
            to_currency = self.to_currency_cb.get()
            amount = float(self.amount_entry.get())

            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
            data = response.json()

            if to_currency in data["rates"]:
                converted_amount = amount * data["rates"][to_currency]
                self.result_label.config(
                    text=f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}"
                )
            else:
                self.result_label.config(text="Conversion failed. Try again.")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")

    def create_widgets(self):
        ttk.Label(self.root, text="Amount:").pack(pady=5)
        self.amount_entry = ttk.Entry(self.root)
        self.amount_entry.pack()

        ttk.Label(self.root, text="From Currency:").pack(pady=5)
        self.from_currency_cb = ttk.Combobox(self.root, values=self.currencies, state="readonly")
        self.from_currency_cb.set("USD")
        self.from_currency_cb.pack()

        ttk.Label(self.root, text="To Currency:").pack(pady=5)
        self.to_currency_cb = ttk.Combobox(self.root, values=self.currencies, state="readonly")
        self.to_currency_cb.set("INR")
        self.to_currency_cb.pack()

        ttk.Button(self.root, text="Convert", command=self.convert).pack(pady=10)
        self.result_label = ttk.Label(self.root, text="", font=("Helvetica", 12))
        self.result_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
