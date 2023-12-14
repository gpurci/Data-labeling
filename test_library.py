from tkinter import * 
from tkinter import ttk

class GUI():                              
    def __init__(self):  
        self.root = Tk()
        self.sv = StringVar() 
        self.prevlaue=''
        #entry
        self.entry = ttk.Entry(self.root, width=30, textvariable =self.sv)
        self.entry.grid(pady=20,padx=20) 
        self.entry.bind("<KeyRelease>", self.OnEntryClick) #keyup                  
        self.root.mainloop()       

    def OnEntryClick(self, event):
        value=self.sv.get().strip()
        changed = True if self.prevlaue != value else False
        print(value, 'Text has changed ? {}'.format(changed))
        self.prevlaue = value

#create the gui
GUI()