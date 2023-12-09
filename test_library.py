import time
from tkinter import ttk
import tkinter as tk

root=tk.Tk()

root.config(width=300,height=220)

notebook=ttk.Notebook(root)
notebook.place(x=0,y=0)

tabList=[]
i=0
while i<6:    
     tabList.append(tk.Frame(root))
     tabList[i].config(width=300,height=150,background='white')
     i+=1

i=0
while i<6: 
    notebook.add(tabList[i],text='tab'+str(i))
    i+=1

def fLoopTabs():
    select_tab_val = notebook.select()
    if (len(select_tab_val) != 0):
        print('select_tab  {}'.format(select_tab_val))
        index = notebook.index(select_tab_val)
        print('select_tab index {}'.format(index))
        notebook.select(index+1)

button=ttk.Button(root,text='Loop',command=fLoopTabs)
button.place(x=20,y=180)

root.mainloop()