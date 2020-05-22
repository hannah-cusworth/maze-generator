import tkinter as tk
import tkinter.font as tkFont

# Algorithms
algorithm_list = [
            "Recursive Backtracker",
            "Eller's Algorithm",
            "Algorithm 3",
            ]
algo_info = [
    "Blah",
    "foo",
    "baz",
]

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
        self.window.rowconfigure([0,1,2,3,4], minsize=100, weight=1)

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
            pady=y,
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
            *algorithm_list,
            ) 
        self.select_variable.trace("w", self.change_algorithm)

        select_widget.configure(
            font=listfont, 
            width=30, 
            height=2, 
            bg="white",
            )
        menu = select_widget.nametowidget(select_widget.menuname)     # Get dropdown menu
        menu.configure(font=(listfont))                               # Set font size of menu
    
        select_widget.pack()

        # Information frame
        info_frame = tk.Frame()
        info_frame.grid(row=2, column=0)
        self.info_text_variable = tk.StringVar(self.window)
        self.info_text = tk.Label(
            master=info_frame,
            textvariable=self.info_text_variable,
            font=myfont,
            padx=x,
            pady=y,
        )
        self.info_text.pack()

        # Customisation frame
        custom_frame = tk.Frame()
        custom_frame.grid(row=3, column=0)
        self.speed_var = tk.IntVar(self.window)
        self.set_speed = tk.Scale(
            master=custom_frame,
            font=listfont,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            length=200,
            label="Speed",
            variable=self.speed_var
            )
        bias_var = tk.StringVar(self.window)
        self.set_bias_none = tk.Radiobutton(
            master=custom_frame,
            font=listfont,
            variable=bias_var,
            text="No Bias",
            )
        self.set_bias_left = tk.Radiobutton(
            master=custom_frame,
            font=listfont,
            variable=bias_var,
            text="Left Bias",
            value="W",
            )
        self.set_bias_right = tk.Radiobutton(
            master=custom_frame,
            font=listfont,
            variable=bias_var,
            text="Right Bias",
            value="E",
            )
        self.set_bias_up = tk.Radiobutton(
            master=custom_frame,
            font=listfont,
            variable=bias_var,
            text="Upward Bias",
            value="N"
            )
        self.set_bias_down = tk.Radiobutton(
            master=custom_frame,
            font=listfont,
            variable=bias_var,
            text="Downward Bias",
            value="S"
            )
        self.set_bias_y = tk.Radiobutton(
            master=custom_frame,
            font=listfont,
            variable=bias_var,
            text="Vertical Bias",
            value="X"
            )
        self.set_bias_x = tk.Radiobutton(
            master=custom_frame,
            font=listfont,
            variable=bias_var,
            text="Horizontal Bias",
            value="Y"
            )
        self.set_speed.pack()

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
            row=4, 
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
            
    def change_algorithm(self, foo, bar, baz): # Dummy args
        choice = self.select_variable.get()
        self.set_bias_down.pack_forget()
        self.set_bias_up.pack_forget()
        self.set_bias_left.pack_forget()
        self.set_bias_right.pack_forget()
        self.set_bias_none.pack_forget()
        self.set_bias_x.pack_forget()
        self.set_bias_y.pack_forget()
        
        if choice == algorithm_list[0]:
            self.info_text_variable.set(algo_info[0])
            self.set_bias_none.pack()
            self.set_bias_down.pack()
            self.set_bias_up.pack()
            self.set_bias_left.pack()
            self.set_bias_right.pack()
            
        if choice == algorithm_list[1]:
            self.info_text_variable.set(algo_info[1])
            self.set_bias_none.pack()
            self.set_bias_x.pack()
            self.set_bias_y.pack()

        if choice == algorithm_list[2]:
            self.info_text_variable.set(algo_info[2])
            
   



    def quit(self):
        self.window.destroy()




