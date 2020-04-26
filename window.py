import tkinter as tk
import tkinter.font as tkFont

algorithm_list = (
            "Algorithm 1",
            "Algorithm 2",
            "Algorithm 3",
)
# Padding
x = 50
y = 50
button_padding = 200

class AlgoSelectWindow():
    def __init__(self):
        self.window = tk.Tk()
        self.choice = ""

        # Configure window
        self.window.title("Maze Generator")
        self.window.columnconfigure(0, minsize=500, weight=1)
        self.window.rowconfigure([0,1,2], minsize=100, weight=1)

        # Set font
        myfont = tkFont.Font(family="Helvetica", size=48)
        listfont = tkFont.Font(family="Helvetica", size=36)

        # Intro frame
        intro_frame = tk.Frame()
        intro_frame.grid(row=0, column=0)

        greeting = tk.Label(
            master=intro_frame,
            text="Welcome to the maze generation alogrithm visualizer!",
            font=myfont,
            padx=x,
            pady=y
        )
        greeting.pack()
       

        # Selection frame
        select_frame = tk.Frame()
        select_frame.grid(row=1, column=0)

        select_label = tk.Label(
            master=select_frame,
            text="To begin, please select an algorithm",
            font=myfont,
            padx=x,
            pady=y,
        )
        select_label.pack()
        
        self.select_variable = tk.StringVar(self.window)    # Variable which stores the current option choice
        select_widget = tk.OptionMenu(     # OptionMenu(parent, variable, value)
            select_frame, 
            self.select_variable,
            *algorithm_list,) 
        select_widget.configure(
            font=listfont, 
            width=20, 
            height=2, 
            bg="white",
            )
        menu = select_widget.nametowidget(select_widget.menuname)     # Get dropdown menu
        menu.configure(font=(listfont))                                     # Set font size of menu
        select_widget.pack()

        # Button
        run_button = tk.Button(
            text="Run algorithm",
            width=15,
            height=1,
            bg="red",
            fg="black",
            command=self.run_algorithm,
            font=myfont,
            pady=10,
        )
        run_button.grid(
            row=2, 
            column=0,
            padx=x,
            pady=button_padding,
            )
        
        # Intitiate 
        self.window.mainloop()

    def run_algorithm(self):
        self.choice = self.select_variable.get()
        if self.choice:
            self.quit()
    
    def quit(self):
        self.window.destroy()




