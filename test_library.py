import time
import tkinter.ttk as ttk
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
    notebook.select('tab'+str(3))
    #Here goes the Screenshot function

button=ttk.Button(root,text='Loop',command=fLoopTabs)
button.place(x=20,y=180)

root.mainloop()