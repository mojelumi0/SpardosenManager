import os
import sys
import json
import tkinter as tk
from tkinter import messagebox, simpledialog, Menu
import xml.etree.ElementTree as ET
from datetime import datetime

# Base directory (same folder where the script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BALANCE_FILE = os.path.join(BASE_DIR, "spardose.txt")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
DEPOSIT_HISTORY_FILE = os.path.join(BASE_DIR, "deposit_history.xml")
WITHDRAW_HISTORY_FILE = os.path.join(BASE_DIR, "withdraw_history.xml")

# Default settings for the application
DEFAULT_SETTINGS = {
    "language": "de",
    "currency": "€",
    "theme": "light",         # Options: "light" or "dark"
    "window_mode": "normal"   # Options: "normal", "fullscreen", "maximized", "minimized"
}

def load_balance():
    """Lädt den Kontostand aus der Datei. Gibt 0.0 zurück, falls die Datei nicht existiert oder ein Fehler auftritt."""
    if os.path.exists(BALANCE_FILE):
        try:
            with open(BALANCE_FILE, "r") as f:
                return float(f.read().strip())
        except ValueError:
            return 0.0
    return 0.0

def save_balance(balance):
    """Speichert den aktuellen Kontostand in der Datei."""
    with open(BALANCE_FILE, "w") as f:
        f.write(str(balance))

def load_settings():
    """Lädt die Anwendungseinstellungen aus einer JSON-Datei und füllt fehlende Werte mit den Standardwerten."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
            for key in DEFAULT_SETTINGS:
                if key not in settings:
                    settings[key] = DEFAULT_SETTINGS[key]
            return settings
        except Exception:
            return DEFAULT_SETTINGS.copy()
    else:
        return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Speichert die aktuellen Einstellungen in einer JSON-Datei."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def record_deposit_transaction(amount, new_balance):
    """Speichert eine Einzahlungstransaktion in der XML-Datei (inkl. Zeitstempel, aber nur in der XML)."""
    timestamp = datetime.now().isoformat()
    if os.path.exists(DEPOSIT_HISTORY_FILE):
        try:
            tree = ET.parse(DEPOSIT_HISTORY_FILE)
            root = tree.getroot()
        except ET.ParseError:
            root = ET.Element("Deposits")
            tree = ET.ElementTree(root)
    else:
        root = ET.Element("Deposits")
        tree = ET.ElementTree(root)
    transaction = ET.Element("Transaction")
    transaction.set("amount", f"{amount:.2f}")
    transaction.set("new_balance", f"{new_balance:.2f}")
    transaction.set("timestamp", timestamp)
    root.append(transaction)
    tree.write(DEPOSIT_HISTORY_FILE, encoding="utf-8", xml_declaration=True)

def record_withdraw_transaction(amount, new_balance):
    """Speichert eine Auszahlungstransaktion in der XML-Datei (inkl. Zeitstempel, aber nur in der XML)."""
    timestamp = datetime.now().isoformat()
    if os.path.exists(WITHDRAW_HISTORY_FILE):
        try:
            tree = ET.parse(WITHDRAW_HISTORY_FILE)
            root = tree.getroot()
        except ET.ParseError:
            root = ET.Element("Withdrawals")
            tree = ET.ElementTree(root)
    else:
        root = ET.Element("Withdrawals")
        tree = ET.ElementTree(root)
    transaction = ET.Element("Transaction")
    transaction.set("amount", f"{amount:.2f}")
    transaction.set("new_balance", f"{new_balance:.2f}")
    transaction.set("timestamp", timestamp)
    root.append(transaction)
    tree.write(WITHDRAW_HISTORY_FILE, encoding="utf-8", xml_declaration=True)

# Übersetzungswörterbuch für Deutsch und Englisch
translations = {
    'de': {
        'settings': 'Einstellungen',
        'toggle_theme': 'Theme wechseln',
        'language': 'Sprache',
        'change_currency': 'Währung ändern',
        'title': 'Spardosen Manager',
        'deposit': 'Geld einzahlen',
        'withdraw': 'Geld auszahlen',
        'current_balance': 'Aktueller Kontostand:',
        'error_insufficient': 'Fehler: Nicht genug Geld in der Spardose!',
        'error_invalid': 'Ungültige Eingabe, bitte erneut versuchen.',
        'currency_prompt': 'Geben Sie das neue Währungssymbol ein:',
        'window_mode': 'Fenstermodus',
        'normal': 'Normal',
        'fullscreen': 'Vollbild',
        'maximized': 'Maximiert',
        'minimized': 'Minimiert',
        'deposit_history': 'Einzahlungen',
        'withdraw_history': 'Auszahlungen'
    },
    'en': {
        'settings': 'Settings',
        'toggle_theme': 'Toggle Theme',
        'language': 'Language',
        'change_currency': 'Change Currency',
        'title': 'Piggy Bank Manager',
        'deposit': 'Deposit Money',
        'withdraw': 'Withdraw Money',
        'current_balance': 'Current Balance:',
        'error_insufficient': 'Error: Not enough money in the piggy bank!',
        'error_invalid': 'Invalid input, please try again.',
        'currency_prompt': 'Enter new currency symbol:',
        'window_mode': 'Window Mode',
        'normal': 'Normal',
        'fullscreen': 'Fullscreen',
        'maximized': 'Maximized',
        'minimized': 'Minimized',
        'deposit_history': 'Deposits',
        'withdraw_history': 'Withdrawals'
    }
}

# --- GUI Mode ---

class PiggyBankApp:
    def __init__(self, master):
        """Initialisiert die GUI-Anwendung, lädt Einstellungen und Kontostand und baut das Layout auf."""
        self.master = master
        self.settings = load_settings()
        self.language = self.settings.get("language", "de")
        self.currency = self.settings.get("currency", "€")
        self.theme = self.settings.get("theme", "light")
        self.window_mode = self.settings.get("window_mode", "normal")
        self.balance = load_balance()
        self.setup_ui()
        self.apply_theme()
        self.apply_window_mode()
        self.update_history()

    def setup_ui(self):
        """Erstellt das GUI-Layout mit Menüs, Eingabefeldern, Buttons und History (nur bei maximiert/vollbild)."""
        self.master.title(self.get_text('title'))
        
        # Menüleiste
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        
        self.settings_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label=self.get_text('settings'), menu=self.settings_menu)
        self.settings_menu.add_command(label=self.get_text('toggle_theme'), command=self.toggle_theme)
        
        # Sprachmenü innerhalb der Einstellungen
        self.lang_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.settings_menu.add_cascade(label=self.get_text('language'), menu=self.lang_menu)
        self.lang_menu.add_command(label="Deutsch", command=lambda: self.set_language('de'))
        self.lang_menu.add_command(label="English", command=lambda: self.set_language('en'))
        
        # Option zum Ändern des Währungssymbols
        self.settings_menu.add_command(label=self.get_text('change_currency'), command=self.change_currency)
        
        # Fenstermodus-Menü innerhalb der Einstellungen
        self.window_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.settings_menu.add_cascade(label=self.get_text('window_mode'), menu=self.window_menu)
        self.window_menu.add_command(label=self.get_text('normal'), command=lambda: self.set_window_mode('normal'))
        self.window_menu.add_command(label=self.get_text('fullscreen'), command=lambda: self.set_window_mode('fullscreen'))
        self.window_menu.add_command(label=self.get_text('maximized'), command=lambda: self.set_window_mode('maximized'))
        self.window_menu.add_command(label=self.get_text('minimized'), command=lambda: self.set_window_mode('minimized'))
        
        # Haupt-Frame für Widgets
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, padx=20, pady=20)  # Standard: etwas Platz, aber kein „großes“ Padding
        
        # Anzeige des aktuellen Kontostands
        self.balance_label = tk.Label(
            self.main_frame, 
            text=self.get_text('current_balance') + f" {self.balance:.2f}{self.currency}", 
            font=("Arial", 16)
        )
        self.balance_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        
        # Eingabefeld für den Betrag
        self.amount_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.amount_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        self.amount_entry.bind("<Return>", lambda event: self.deposit())
        
        # Buttons für Einzahlung und Auszahlung
        self.deposit_button = tk.Button(
            self.main_frame, 
            text=self.get_text('deposit'), 
            command=self.deposit, 
            font=("Arial", 14)
        )
        self.deposit_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        self.withdraw_button = tk.Button(
            self.main_frame, 
            text=self.get_text('withdraw'), 
            command=self.withdraw, 
            font=("Arial", 14)
        )
        self.withdraw_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # History-Frame: Links Einzahlungen, rechts Auszahlungen (jeweils letzte 5)
        self.history_frame = tk.Frame(self.main_frame)
        self.history_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky="nsew")
        self.history_frame.columnconfigure(0, weight=1)
        self.history_frame.columnconfigure(1, weight=1)
        
        self.deposit_history_label = tk.Label(
            self.history_frame, 
            text=self.get_text('deposit_history'),
            font=("Arial", 12)
        )
        self.deposit_history_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.withdraw_history_label = tk.Label(
            self.history_frame, 
            text=self.get_text('withdraw_history'),
            font=("Arial", 12)
        )
        self.withdraw_history_label.grid(row=0, column=1, padx=5, pady=5)
        
        self.deposit_listbox = tk.Listbox(self.history_frame, width=40, height=5)
        self.deposit_listbox.grid(row=1, column=0, padx=5, pady=5)
        
        self.withdraw_listbox = tk.Listbox(self.history_frame, width=40, height=5)
        self.withdraw_listbox.grid(row=1, column=1, padx=5, pady=5)
        
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # Speichert Einstellungen beim Schließen der Anwendung
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self, width=400, height=300):
        """Zentriert das Fenster auf dem Bildschirm."""
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def get_text(self, key):
        """Gibt den übersetzten Text zum gegebenen Schlüssel zurück."""
        return translations[self.language][key]

    def update_history(self):
        """Lädt die letzten 5 Transaktionen aus den XML-Dateien und zeigt sie in den Listboxen an (ohne Zeit)."""
        # Einzahlungen
        deposit_transactions = []
        if os.path.exists(DEPOSIT_HISTORY_FILE):
            try:
                tree = ET.parse(DEPOSIT_HISTORY_FILE)
                root = tree.getroot()
                transactions = list(root)
                last_transactions = transactions[-5:]
                for t in last_transactions:
                    amount = t.get("amount")
                    new_balance = t.get("new_balance")
                    # Uhrzeit NICHT anzeigen, nur Beträge
                    deposit_transactions.append(f"{amount}{self.currency} → {new_balance}{self.currency}")
            except Exception:
                deposit_transactions.append("Fehler beim Laden")
        else:
            deposit_transactions.append("Keine Einzahlungen")
        self.deposit_listbox.delete(0, tk.END)
        for item in deposit_transactions:
            self.deposit_listbox.insert(tk.END, item)
        
        # Auszahlungen
        withdraw_transactions = []
        if os.path.exists(WITHDRAW_HISTORY_FILE):
            try:
                tree = ET.parse(WITHDRAW_HISTORY_FILE)
                root = tree.getroot()
                transactions = list(root)
                last_transactions = transactions[-5:]
                for t in last_transactions:
                    amount = t.get("amount")
                    new_balance = t.get("new_balance")
                    # Uhrzeit NICHT anzeigen, nur Beträge
                    withdraw_transactions.append(f"{amount}{self.currency} → {new_balance}{self.currency}")
            except Exception:
                withdraw_transactions.append("Fehler beim Laden")
        else:
            withdraw_transactions.append("Keine Auszahlungen")
        self.withdraw_listbox.delete(0, tk.END)
        for item in withdraw_transactions:
            self.withdraw_listbox.insert(tk.END, item)

    def deposit(self):
        """Erhöht den Kontostand um den eingegebenen Betrag, speichert die Transaktion und aktualisiert die Anzeige."""
        try:
            input_str = self.amount_entry.get().replace(",", ".")
            amount = float(input_str)
            self.balance += amount
            save_balance(self.balance)
            self.update_balance_label()
            record_deposit_transaction(amount, self.balance)
            self.update_history()
        except ValueError:
            messagebox.showerror("Error", self.get_text('error_invalid'))
        self.amount_entry.delete(0, tk.END)

    def withdraw(self):
        """Verringert den Kontostand um den eingegebenen Betrag (falls genügend Guthaben vorhanden) und speichert die Transaktion."""
        try:
            input_str = self.amount_entry.get().replace(",", ".")
            amount = float(input_str)
            if amount > self.balance:
                messagebox.showerror("Error", self.get_text('error_insufficient'))
            else:
                self.balance -= amount
                save_balance(self.balance)
                self.update_balance_label()
                record_withdraw_transaction(amount, self.balance)
                self.update_history()
        except ValueError:
            messagebox.showerror("Error", self.get_text('error_invalid'))
        self.amount_entry.delete(0, tk.END)

    def update_balance_label(self):
        """Aktualisiert die Anzeige des aktuellen Kontostands."""
        self.balance_label.config(text=self.get_text('current_balance') + f" {self.balance:.2f}{self.currency}")

    def toggle_theme(self):
        """Wechselt zwischen dunklem und hellem Theme, speichert die Einstellung und wendet sie an."""
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.settings['theme'] = self.theme
        save_settings(self.settings)
        self.apply_theme()

    def apply_theme(self):
        """Wendet die Theme-Farben auf die Benutzeroberfläche an."""
        if self.theme == 'dark':
            bg_color = "#2e2e2e"
            fg_color = "#ffffff"
            btn_bg = "#444444"
        else:
            bg_color = "#ffffff"
            fg_color = "#000000"
            btn_bg = "#e0e0e0"
        self.master.configure(bg=bg_color)
        self.main_frame.configure(bg=bg_color)
        self.balance_label.configure(bg=bg_color, fg=fg_color)
        self.amount_entry.configure(bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self.deposit_button.configure(bg=btn_bg, fg=fg_color, activebackground=fg_color, activeforeground=bg_color)
        self.withdraw_button.configure(bg=btn_bg, fg=fg_color, activebackground=fg_color, activeforeground=bg_color)
        self.history_frame.configure(bg=bg_color)
        self.deposit_history_label.configure(bg=bg_color, fg=fg_color)
        self.withdraw_history_label.configure(bg=bg_color, fg=fg_color)
        self.deposit_listbox.configure(bg=bg_color, fg=fg_color)
        self.withdraw_listbox.configure(bg=bg_color, fg=fg_color)

    def set_language(self, lang):
        """Ändert die Anzeigesprache, speichert die Einstellung und aktualisiert die Texte."""
        self.language = lang
        self.settings['language'] = lang
        save_settings(self.settings)
        self.update_ui_texts()

    def update_ui_texts(self):
        """Aktualisiert alle Texte in der Benutzeroberfläche (Fenstertitel, Buttons, Menüs)."""
        self.master.title(self.get_text('title'))
        self.deposit_button.config(text=self.get_text('deposit'))
        self.withdraw_button.config(text=self.get_text('withdraw'))
        self.update_balance_label()
        self.settings_menu.entryconfig(0, label=self.get_text('toggle_theme'))
        self.settings_menu.entryconfig(1, label=self.get_text('language'))
        self.settings_menu.entryconfig(2, label=self.get_text('change_currency'))
        self.settings_menu.entryconfig(3, label=self.get_text('window_mode'))
        self.window_menu.entryconfig(0, label=self.get_text('normal'))
        self.window_menu.entryconfig(1, label=self.get_text('fullscreen'))
        self.window_menu.entryconfig(2, label=self.get_text('maximized'))
        self.window_menu.entryconfig(3, label=self.get_text('minimized'))
        self.deposit_history_label.config(text=self.get_text('deposit_history'))
        self.withdraw_history_label.config(text=self.get_text('withdraw_history'))

    def change_currency(self):
        """Ermöglicht das Ändern des Währungssymbols und speichert die neue Einstellung."""
        prompt = self.get_text('currency_prompt')
        new_currency = simpledialog.askstring("Currency", prompt)
        if new_currency:
            self.currency = new_currency
            self.settings['currency'] = new_currency
            save_settings(self.settings)
            self.update_balance_label()
            self.update_history()

    def set_window_mode(self, mode):
        """Setzt den Fenstermodus (normal, fullscreen, maximiert, minimiert) und speichert die Einstellung."""
        self.window_mode = mode
        self.settings['window_mode'] = mode
        save_settings(self.settings)
        self.apply_window_mode()

    def apply_window_mode(self):
        """Wendet den ausgewählten Fenstermodus an und zeigt die History nur in 'maximized' oder 'fullscreen'."""
        self.master.attributes("-fullscreen", False)
        if self.window_mode == 'fullscreen':
            self.master.attributes("-fullscreen", True)
        elif self.window_mode == 'maximized':
            self.master.state("zoomed")
        elif self.window_mode == 'minimized':
            self.master.iconify()
        else:
            self.master.state("normal")
            self.center_window(400, 300)
        
        # History-Panel nur in "maximiert" oder "vollbild" anzeigen
        if self.window_mode in ['maximized', 'fullscreen']:
            self.history_frame.grid()
        else:
            self.history_frame.grid_remove()

    def on_close(self):
        """Speichert die Einstellungen und schließt die Anwendung."""
        save_settings(self.settings)
        self.master.destroy()

def run_gui():
    """Startet den GUI-Modus der Anwendung."""
    root = tk.Tk()
    app = PiggyBankApp(root)
    root.mainloop()

# --- CLI Mode ---

def run_cli():
    """Startet den CLI-Modus der Anwendung mit einem textbasierten Menü."""
    balance = load_balance()
    while True:
        print("\nPiggy Bank Manager")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Show Balance")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            try:
                input_str = input("How much do you want to deposit? ").replace(",", ".")
                amount = float(input_str)
                balance += amount
                save_balance(balance)
                currency = load_settings().get('currency', '€')
                print(f"{amount:.2f}{currency} deposited. New balance: {balance:.2f}{currency}")
                record_deposit_transaction(amount, balance)
            except ValueError:
                print("Invalid input, please try again.")
        elif choice == "2":
            try:
                input_str = input("How much do you want to withdraw? ").replace(",", ".")
                amount = float(input_str)
                if amount > balance:
                    print("Error: Not enough money in the piggy bank!")
                else:
                    balance -= amount
                    save_balance(balance)
                    currency = load_settings().get('currency', '€')
                    print(f"{amount:.2f}{currency} withdrawn. New balance: {balance:.2f}{currency}")
                    record_withdraw_transaction(amount, balance)
            except ValueError:
                print("Invalid input, please try again.")
        elif choice == "3":
            currency = load_settings().get('currency', '€')
            print(f"Current balance: {balance:.2f}{currency}")
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    # Startet den CLI-Modus, falls "--cli" als Argument übergeben wird, ansonsten den GUI-Modus.
    if "--cli" in sys.argv:
        run_cli()
    else:
        run_gui()
