import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class LimitedNotebook(ttk.Notebook):
    def __init__(self, master=None, max_tabs=5, **kwargs):
        ttk.Notebook.__init__(self, master, **kwargs)
        self.max_tabs = max_tabs
        self.bind('<Button-1>', self.check_tab_limit)
    
    def check_tab_limit(self, event):
        # Check the number of tabs and prevent adding more than max_tabs
        if self.index('end') > self.max_tabs:
            tk.messagebox.showwarning("Tab Limit", f"Maximum {self.max_tabs} tabs allowed.")
            return "break"  # Prevents the tab from being selected
    
    def add_tab(self, tab_frame, tab_text):
        # Add a tab to the notebook
        if self.index('end') < self.max_tabs:
            self.add(tab_frame, text=tab_text)
            self.select(tab_frame)
        else:
            tk.messagebox.showwarning("Tab Limit", f"Maximum {self.max_tabs} tabs allowed.")

    def remove_tab(self, tab_index):
        # Remove a tab from the notebook
        if self.index('end') > 0:
            self.forget(tab_index)

# Example usage
def create_tab():
    tab_frame = ttk.Frame(notebook)
    notebook.add_tab(tab_frame, f"Tab {notebook.index('end')}")

def remove_tab():
    selected_tab_index = notebook.index(notebook.select())
    notebook.remove_tab(selected_tab_index)

def change_tab_width(width):
    notebook.tk_setPalette(background='gray')  # Set a background color for better visibility
    notebook.configure(tabwidth=width)

root = tk.Tk()
root.title("Limited Tab Notebook")

notebook = LimitedNotebook(root, max_tabs=3)
notebook.pack(padx=10, pady=10)

add_button = ttk.Button(root, text="Add Tab", command=create_tab)
add_button.pack(side=tk.LEFT, padx=5)

remove_button = ttk.Button(root, text="Remove Tab", command=remove_tab)
remove_button.pack(side=tk.LEFT, padx=5)

# Button to change tab width dynamically
change_width_button = ttk.Button(root, text="Change Tab Width", command=lambda: change_tab_width(8))
change_width_button.pack(side=tk.LEFT, padx=5)

root.mainloop()

