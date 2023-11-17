import tkinter as tk


class Texter(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack()

        self.frames = {}

        for F in (ConnectPage, EditorPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        page_name = EditorPage.__name__
        self.frames[page_name] = frame
        self.show_frame(ConnectPage)

    def show_frame(self, cont) :
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_name) :
        return self.frames[page_name]


class ConnectPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="SecondPage",
                            command=lambda : controller.show_frame(EditorPage))
        button1.grid(row=2, column=3, padx=15)


class EditorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.text = CustomText(self, height=25, width=80)
        self.text.grid(column=0, row=0, sticky="nw")
        self.text.bind("<<TextModified>>", self.onModification)

        button2 = tk.Button(self, text="FirstPage",
                            command=lambda : controller.show_frame(ConnectPage))
        button2.grid(row=2, column=3, padx=15)

    def onModification(self, event):
        print("Yellow!")


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs) :
        """A text widget that report on internal widget commands"""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args) :
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace") :
            self.event_generate("<<TextModified>>")

        return result


if __name__ == '__main__':
    gui = Texter()
    gui.mainloop()
