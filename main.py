import os
import sys
import json
import tkinter as tk
from tkinter import messagebox, simpledialog, Menu

# Base directory (same folder where the script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BALANCE_FILE = os.path.join(BASE_DIR, "spardose.txt")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# Default settings for the application
DEFAULT_SETTINGS = {
    "language": "de",
    "currency": "€",
    "theme": "light",         # Options: "light" or "dark"
    "window_mode": "normal"     # Options: "normal", "fullscreen", "maximized", "minimized"
}

def load_balance():
    """Loads the balance from the file. Returns 0.0 if the file does not exist or an error occurs."""
    if os.path.exists(BALANCE_FILE):
        try:
            with open(BALANCE_FILE, "r") as f:
                return float(f.read().strip())
        except ValueError:
            return 0.0
    return 0.0

def save_balance(balance):
    """Saves the current balance to the file."""
    with open(BALANCE_FILE, "w") as f:
        f.write(str(balance))

def load_settings():
    """Loads the application settings from a JSON file and fills in missing values with defaults."""
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
    """Saves the current settings to a JSON file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

# Translation dictionary for German and English
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
        'minimized': 'Minimiert'
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
        'minimized': 'Minimized'
    }
}

# --- GUI Mode ---

class PiggyBankApp:
    def __init__(self, master):
        """Initializes the GUI application, loads settings and balance, and applies the layout."""
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

    def setup_ui(self):
        """Creates the GUI layout with menus, input fields, buttons, and configures the layout."""
        self.master.title(self.get_text('title'))
        
        # Create the menu bar using translations for all labels
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        
        self.settings_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label=self.get_text('settings'), menu=self.settings_menu)
        self.settings_menu.add_command(label=self.get_text('toggle_theme'), command=self.toggle_theme)
        
        # Language menu within settings
        self.lang_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.settings_menu.add_cascade(label=self.get_text('language'), menu=self.lang_menu)
        self.lang_menu.add_command(label="Deutsch", command=lambda: self.set_language('de'))
        self.lang_menu.add_command(label="English", command=lambda: self.set_language('en'))
        
        # Option to change the currency symbol
        self.settings_menu.add_command(label=self.get_text('change_currency'), command=self.change_currency)
        
        # Window mode menu within settings
        self.window_menu = tk.Menu(self.settings_menu, tearoff=0)
        self.settings_menu.add_cascade(label=self.get_text('window_mode'), menu=self.window_menu)
        self.window_menu.add_command(label=self.get_text('normal'), command=lambda: self.set_window_mode('normal'))
        self.window_menu.add_command(label=self.get_text('fullscreen'), command=lambda: self.set_window_mode('fullscreen'))
        self.window_menu.add_command(label=self.get_text('maximized'), command=lambda: self.set_window_mode('maximized'))
        self.window_menu.add_command(label=self.get_text('minimized'), command=lambda: self.set_window_mode('minimized'))
        
        # Main frame for widgets
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=True, padx=20, pady=20)
        
        # Display current balance
        self.balance_label = tk.Label(
            self.main_frame, 
            text=self.get_text('current_balance') + f" {self.balance:.2f}{self.currency}", 
            font=("Arial", 16)
        )
        self.balance_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        
        # Input field for the amount
        self.amount_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.amount_entry.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        # Bind the Enter key to trigger deposit
        self.amount_entry.bind("<Return>", lambda event: self.deposit())
        
        # Button for depositing money
        self.deposit_button = tk.Button(
            self.main_frame, 
            text=self.get_text('deposit'), 
            command=self.deposit, 
            font=("Arial", 14)
        )
        self.deposit_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        # Button for withdrawing money
        self.withdraw_button = tk.Button(
            self.main_frame, 
            text=self.get_text('withdraw'), 
            command=self.withdraw, 
            font=("Arial", 14)
        )
        self.withdraw_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # Save settings when the application is closed
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def center_window(self, width=400, height=300):
        """Centers the window on the screen with the specified size."""
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def get_text(self, key):
        """Returns the translated text for the given key."""
        return translations[self.language][key]

    def deposit(self):
        """Increases the balance by the entered amount and updates the display."""
        try:
            # Ersetze Komma durch Punkt für korrekte Float-Konvertierung
            input_str = self.amount_entry.get().replace(",", ".")
            amount = float(input_str)
            self.balance += amount
            save_balance(self.balance)
            self.update_balance_label()
        except ValueError:
            messagebox.showerror("Error", self.get_text('error_invalid'))
        self.amount_entry.delete(0, tk.END)

    def withdraw(self):
        """Decreases the balance by the entered amount if sufficient funds exist."""
        try:
            # Ersetze Komma durch Punkt für korrekte Float-Konvertierung
            input_str = self.amount_entry.get().replace(",", ".")
            amount = float(input_str)
            if amount > self.balance:
                messagebox.showerror("Error", self.get_text('error_insufficient'))
            else:
                self.balance -= amount
                save_balance(self.balance)
                self.update_balance_label()
        except ValueError:
            messagebox.showerror("Error", self.get_text('error_invalid'))
        self.amount_entry.delete(0, tk.END)

    def update_balance_label(self):
        """Updates the label that displays the current balance."""
        self.balance_label.config(text=self.get_text('current_balance') + f" {self.balance:.2f}{self.currency}")

    def toggle_theme(self):
        """Toggles between dark and light themes, saves the setting, and applies it."""
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.settings['theme'] = self.theme
        save_settings(self.settings)
        self.apply_theme()

    def apply_theme(self):
        """Applies the theme colors to the interface."""
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

    def set_language(self, lang):
        """Changes the application language, saves the setting, and updates UI texts."""
        self.language = lang
        self.settings['language'] = lang
        save_settings(self.settings)
        self.update_ui_texts()

    def update_ui_texts(self):
        """Updates all texts in the user interface (window title, buttons, menus)."""
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

    def change_currency(self):
        """Allows changing the currency symbol and saves the new setting."""
        prompt = self.get_text('currency_prompt')
        new_currency = simpledialog.askstring("Currency", prompt)
        if new_currency:
            self.currency = new_currency
            self.settings['currency'] = new_currency
            save_settings(self.settings)
            self.update_balance_label()

    def set_window_mode(self, mode):
        """Sets the window mode (normal, fullscreen, maximized, minimized) and saves the setting."""
        self.window_mode = mode
        self.settings['window_mode'] = mode
        save_settings(self.settings)
        self.apply_window_mode()

    def apply_window_mode(self):
        """Applies the selected window mode and centers the window in normal mode."""
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

    def on_close(self):
        """Saves settings and closes the application."""
        save_settings(self.settings)
        self.master.destroy()

def run_gui():
    """Starts the GUI mode of the application."""
    root = tk.Tk()
    app = PiggyBankApp(root)
    root.mainloop()

# --- CLI Mode ---

def run_cli():
    """Starts the CLI mode of the application with a text-based menu."""
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
    # Start CLI mode if "--cli" argument is provided, otherwise start GUI mode.
    if "--cli" in sys.argv:
        run_cli()
    else:
        run_gui()
