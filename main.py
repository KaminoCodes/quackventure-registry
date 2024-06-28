import ctypes
import sys
import tkinter as tk
from tkinter import filedialog
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
    if file_path:
        entry_var.set(file_path)

def install_registry():
    exe_path = entry_var.get().replace("/", r"\\")
    if not exe_path:
        result_label.config(text="Please select a file first.")
        return

    try:
        # URI Registration
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"quackventure")
        winreg.SetValueEx(key, "URL Protocol", 0, winreg.REG_SZ, "")
        winreg.SetValue(key, None, winreg.REG_SZ, "Quackventure")
        winreg.CloseKey(key)

        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"quackventure\shell")
        winreg.CloseKey(key)

        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"quackventure\shell\open")
        winreg.CloseKey(key)

        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"quackventure\shell\open\command")
        command = f'"{exe_path}" "%1"'
        winreg.SetValue(key, None, winreg.REG_SZ, command)
        winreg.CloseKey(key)

        # File Association - Play
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Quackventure Level")
        winreg.SetValue(key, None, winreg.REG_SZ, "Quackventure Level")
        winreg.CloseKey(key)

        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Quackventure Level\DefaultIcon")
        winreg.SetValue(key, None, winreg.REG_SZ, f"{exe_path},0")
        winreg.CloseKey(key)

        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Quackventure Level\shell")
        winreg.SetValue(key, None, winreg.REG_SZ, "open")
        winreg.CloseKey(key)

        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Quackventure Level\shell\open")
        winreg.SetValue(key, None, winreg.REG_SZ, "Play")
        winreg.CloseKey(key)

        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Quackventure Level\shell\open\command")
        play_command = f'"{exe_path}" --map="%1"'
        winreg.SetValue(key, None, winreg.REG_SZ, play_command)
        winreg.CloseKey(key)

        # File Association - Edit
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Quackventure Level\shell\edit")
        winreg.SetValue(key, None, winreg.REG_SZ, "Edit")
        winreg.CloseKey(key)

        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Quackventure Level\shell\edit\command")
        edit_command = f'"{exe_path}" --edit="%1"'
        winreg.SetValue(key, None, winreg.REG_SZ, edit_command)
        winreg.CloseKey(key)

        result_label.config(text="Registry installed successfully.")
    except Exception as e:
        result_label.config(text=f"Error: {e}")

if is_admin():
    # Create the main window
    root = tk.Tk()
    root.title("Quackventure Registry Installer")

    # Create and set the string variable for entry
    entry_var = tk.StringVar()

    # Create the GUI elements
    instruction_label = tk.Label(root, text="Select the location of 'quackventure.exe':")
    instruction_label.pack(pady=10)

    file_entry = tk.Entry(root, textvariable=entry_var, width=50)
    file_entry.pack(padx=10)

    browse_button = tk.Button(root, text="Browse", command=select_file)
    browse_button.pack(pady=5)

    install_button = tk.Button(root, text="Install Registry", command=install_registry)
    install_button.pack(pady=10)

    result_label = tk.Label(root, text="")
    result_label.pack(pady=10)

    # Run the application
    root.mainloop()
else:
    # Re-run the script with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
