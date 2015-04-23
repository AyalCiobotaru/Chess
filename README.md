# Chess
Chess Program

    from Tkinter import  Grid, Frame, Menu, Button, Label, Tk, END, Label, Entry
    
    class ChessBoard(Frame):
        def __init__(self, master=None, title="Chess"):
            Frame.__init__(self, master)
    
            self.master = master
            self.master.title(title)
    
            """
            self.tempFileName = "tempLog.pdf"
            self.log = open(self.tempFilename, "r")
            self.fileName = None
            """
            self.locations = ()
            self.board_setup()
            self.button_location = {}
            self.get_grid_info()
        
            print self.button_location
        
            self.bind("<Destroy>", self.exit)
            self.mainloop()
    
      # create the board in the GUI
      
        def board_setup(self, _=None):
            def set_up_GUI():
                menuBar = Menu(self)
                self.master.config(menu=menuBar)
                fileMenu = Menu(menuBar, tearoff=0)
                menuBar.add_cascade(label="File", menu=fileMenu)
                fileMenu.add_command(label="New", command=self.new_game)
                fileMenu.add_command(label="Save", command=self.save_game)
                fileMenu.add_command(label="Open", command=self.open_game)
                fileMenu.add_command(label="Exit", command=self.exit)
                fileMenu.insert_separator(fileMenu.index(END))
            
                self.labelframe = Frame(self.master)
                self.labelframe.grid(column=0, row=0, sticky="W", padx=13)
    
        def label_helper(row, column, labels="12345678"):
            for c in labels:
                Button(self.labelframe, text=c, state="disabled", bg="Grey", fg="white", justify="center",
                    width=10).grid(row=row, column=column)
                column += 1
    
        def row_label_helper(row, column, labels="12345678"):
            for c in labels:
                Label(self.labelframe, text=c, padx=15).grid(row=row, column=column)
                row += 1
    
        def row_helper(row, column):
            for row in range(1, 9):
                column = 1
                for button in range(1, 9):
                    if row % 2 == 0:
                        bg = "Black"
                        if button % 2 == 0:
                            bg = "White"
                    else:
                        bg = "White"
                        if button % 2 == 0:
                            bg = "Black"
                    Button(self.labelframe, bg=bg, width=10, height=3).grid(row=row, column=column,
                                                                    sticky="N")
                    column += 1
                row += 1
    
        set_up_GUI()
        label_helper(0, 1)
        row_label_helper(1, 0)
        row_helper(0, 1)
        row_label_helper(1, 9)
        label_helper(9, 1)
    
        def get_grid_info(self):
            for key in self.labelframe.children.values():
                self.locations = key.grid_info()['row'], key.grid_info()['column']
                self.button_location[self.locations] = key
    
        def new_game(self):
            pass
    
        def save_game(self):
            pass
        
        def open_game(self):
            pass
        
        def exit(self, _=None):
            self.quit()
            self.destroy()
    
    class Pieces(object, ChessBoard):
        def __init__(self):
            super(Pieces, self).__init__()
    
            self.white = ["ROOK", "KNIGHT", "BISHOP", "KING", "QUEEN", "BISHOP", "KNIGHT", "ROOK"]
            self.black = lower(self.white)
    
        def place_pieces(self, labels):
            for labels in self.white:
                self.button_location['8', str(y)].config(text=labels, fg="Blue")
            for labels in self.black:
                self.button_location['1', str(y)].config(text=labels, fg="Orange")
            for x in range(1,9):
                self.button_location['7', str(x)].config(text="PAWN", fg="Blue")
                self.button_location['2', str(s)].config(text="pawn", fg="Orange")
    
    ChessBoard(Tk())
