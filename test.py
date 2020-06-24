from tkinter import *
root=Tk()
t = Text(root)
t.pack()
t.bind('<MouseWheel>',lambda event:print(event))

root.mainloop()