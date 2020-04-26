import tkinter as tk
from tkinter import ttk

font = "Helvetica"
size = 18
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

        # Intro frame
        intro_frame = tk.Frame()
        intro_frame.grid(row=0, column=0)

        greeting = tk.Label(
            master=intro_frame,
            text="Welcome to the maze generation alogrithm visualizer!",
        )
        greeting.pack()
       

        # Selection frame
        select_frame = tk.Frame()
        select_frame.grid(row=1, column=0)

        select_label = tk.Label(
            master=select_frame,
            text="To begin, please select an algorithm",
            font = font,
            size = size,
        )
        select_label.pack()
        
        
        self.select_widget = ttk.Combobox(
            master=select_frame,
            values= algorithm_list,
            font = font,
            size = size,
        )
        self.select_widget.pack()

        run_button = tk.Button(
            text="Run algorithm",
            width=15,
            height=5,
            bg="red",
            fg="black",
            master=select_frame,
            command=self.run_algorithm,
            font = font,
            size = size,
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