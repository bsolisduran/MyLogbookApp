import tkinter as tk
from tkinter import ttk
from globals import *


class AscentWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        
        self.title("Add Ascent Window")
        self.geometry("600x600")

        # Main Widgets:
        # -- Title:
        self.label1 = tk.Label(self, text="Add Ascent manager", font=numberFont)
        self.label1.pack()
        
        # -- Main Frame for labels and entries:
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack()

        # -- Labels:
        climbStyleLabel = self.get_label("Route / Boulder:", 0, 0, 1)
        dateLabel = self.get_label("Date:", 1, 0, 1)
        styleLabel = self.get_label("Style:", 2, 0, 1)
        gradeLabel = self.get_label("Grade:", 3, 0, 1)
        routeLabel = self.get_label("Route Name: ", 4, 0, 1)        
        cragLabel = self.get_label("Crag: ", 5, 0, 1)
        sectorLabel = self.get_label("Sector: ", 6, 0, 1)
        commentsLabel = self.get_label("Comments:", 7, 0, 1)
        gradeOpLabel = self.get_label("Grade opinion:", 8, 0, 1)
        triesLabel = self.get_label("Tries:", 9, 0, 1)

        # -- Climbing Style combobox:
        climbStyleValues = ["Route", "Boulder"]
        self.climbStyleCombo = self.get_comboBox(values=climbStyleValues, state='disabled', current=0)
        self.climbStyleCombo.grid(row=0, column=1, sticky='e')

        # -- Date Entry:
        self.dateEntry = self.get_entry(default="dd/mm/yyyy")
        self.dateEntry.grid(row=1, column=1, sticky='e')
        self.dateEntry.bind("<FocusIn>", lambda event: self.handle_focus_in())
        # self.dateEntry.bind("<FocusOut>", lambda event: self.validate())

        # -- ascent Style combobox:
        styleValues = ["RP", "FL", "OS"]
        self.styleCombo = self.get_comboBox(values=styleValues, state='readonly', current=None)
        self.styleCombo.grid(row=2, column=1, sticky='e')

        # -- Grade combobox:
        gradeValues = GRADES
        self.gradeCombo = self.get_comboBox(values=gradeValues, state='readonly', current=10)
        self.gradeCombo.grid(row=3, column=1, sticky='e')

        # -- Add button:
        self.addButton = tk.Button(self, text='Add ascent', width=25, command=self.add_ascent)
        self.addButton.pack()
       
        # -- Close button (exit to MainApplication):
        self.button1 = tk.Button(self, text = 'Close Window', width = 25, command = self.close_window)
        self.button1.pack()

    def get_label(self, text, row, column, columnspan):
        label = tk.Label(self.mainFrame, text=text, font=numberFont, anchor='w', justify='left')
        label.grid(row=row, column=column, columnspan=columnspan, sticky='w')

    def get_comboBox(self, values, state, current):
        self.comboBox = ttk.Combobox(self.mainFrame, values=values, font=numberFont, state=state)
        self.option_add('*TCombobox*Listbox.font', numberFont)
        # self.option_add('*TCombobox*Listbox.Justify', 'center')       # new line added
        self.comboBox.current(current)
        return self.comboBox

    def get_entry(self, default=None):
        self.entry = tk.Entry(self.mainFrame, font=numberFont)
        self.entry.delete(0, tk.END)
        if default:
            self.entry.config(fg='grey')
            self.entry.insert(0, default)

        return self.entry

    # def handle_default(self, default):
    #     self.entry.config(fg='grey')
    #     self.entry.insert(0, default)

    def handle_focus_in(self):
        self.entry.delete(0, tk.END)
        self.entry.config(fg='black')

    def add_ascent(self):
        print("ascent added!")
        print(self.climbStyleCombo.get())
        print(self.dateEntry.get())

    def close_window(self):
        self.destroy()