import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

algorithm_list = [
            "Algorithm 1",
            "Algorithm 2",
            "Algorithm 3",
        ]


class ChoiceWindow():
    def __init__(self):
        self.window = tk.Tk()
        self.choice = ""

        # Configure window
        self.window.title("Maze Generator")
        self.window.columnconfigure(0, minsize=250, weight = 1)
        self.window.rowconfigure([0,1], minsize=100, weight=1)

        # Set font
        myfont = tkFont.Font(family="Helvetica", size=48)
        

        # Intro frame
        intro_frame = tk.Frame()
        intro_frame.grid(row=0, column=0)

        greeting = tk.Label(
            master=intro_frame,
            text="Welcome to the maze generation alogrithm visualizer!",
            font=myfont,
        )
        greeting.pack()
       

        # Selection frame
        select_frame = tk.Frame()
        select_frame.grid(row=1, column=0)

        select_label = tk.Label(
            master=select_frame,
            text="To begin, please select an algorithm",
            font=myfont
        )
        select_label.pack()
        
        
        self.select_widget = ttk.Combobox(
            master=select_frame,
            values= algorithm_list,
            font=myfont,   
        )
        self.window.option_add('*TCombobox*Listbox.font', myfont)
        self.select_widget.pack()

        run_button = tk.Button(
            text="Run algorithm",
            width=15,
            height=5,
            bg="red",
            fg="black",
            master=select_frame,
            command=self.run_algorithm,
            font=myfont,
        )
        run_button.pack()
        
        # Intitiate 
        self.window.mainloop()

    def run_algorithm(self):
        self.choice = self.select_widget.get()
        self.quit()
    
    def quit(self):
        self.window.destroy()



window = ChoiceWindow()
print(window.choice)