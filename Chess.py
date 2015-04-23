__author__ = 'aciobotaru'

from Tkinter import Grid, Frame, Menu, Button, Label, Tk, END, Entry, Event, PhotoImage, RAISED, Toplevel


class ChessBoard(Frame):
    def __init__(self, master=None, title="Chess"):
        Frame.__init__(self, master)

        self.master = master
        self.master.title(title)

        self.white = ["ROOK", "KNIGHT", "BISHOP", "QUEEN", "KING", "BISHOP.", "KNIGHT.", "ROOK."]
        self.black = [w.lower() for w in self.white]
        self.white_pawn = PhotoImage(file="White_Pawn.gif")
        self.black_pawn = PhotoImage(file="Black_Pawn.gif")
        self.black_pieces = [PhotoImage(file="Black_Rook.gif"), PhotoImage(file="Black_Knight.gif"),
                             PhotoImage(file="Black_Bishop.gif"), PhotoImage(file="Black_Queen.gif"),
                             PhotoImage(file="Black_King.gif"), PhotoImage(file="Black_Bishop1.gif"),
                             PhotoImage(file="Black_Knight1.gif"), PhotoImage(file="Black_Rook1.gif")]

        self.white_pieces = [PhotoImage(file="White_Rook.gif"), PhotoImage(file="White_Knight.gif"),
                             PhotoImage(file="White_Bishop.gif"), PhotoImage(file="White_Queen.gif"),
                             PhotoImage(file="White_King.gif"), PhotoImage(file="White_Bishop1.gif"),
                             PhotoImage(file="White_Knight1.gif"), PhotoImage(file="White_Rook1.gif")]
        self.piece = ""
        self.piece_color = ""
        self.original_row = int()
        self.original_col = int()
        self.image = ()
        self.locations = ()
        self.button_location = {}
        self.black_king_locations = []
        self.white_king_locations = []

        self.turn = 1
        self.board_setup()
        self.get_grid_info()
        self.place_pieces()
        # self.directions_window()
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
            fileMenu.add_command(label="Exit", command=self.exit)
            fileMenu.insert_separator(fileMenu.index(END))

            self.labelframe = Frame(self.master)
            self.labelframe.grid(column=0, row=0, sticky="W", padx=13)

        def label_helper(row, column, labels="ABCDEFGH"):
            for c in labels:
                Button(self.labelframe, text=c, state="disabled", bg="Grey", fg="white", justify="center",
                       width=20, bd=8, relief=RAISED).grid(row=row, column=column)
                column += 1

        def row_label_helper(row, column, labels="87654321"):
            for c in labels:
                Label(self.labelframe, text=c, padx=15).grid(row=row, column=column)
                row += 1

        # Sets up the black white pattern on the board
        # Makes the board wait for an event (mouse button press)
        def row_helper():
            for row in range(1, 9):
                for column in range(1, 9):
                    if row % 2 == 0:
                        bg = "Black"
                        if column % 2 == 0:
                            bg = "White"
                    else:
                        bg = "White"
                        if column % 2 == 0:
                            bg = "Black"
                    b1 = Button(self.labelframe, bg=bg, width=20, height=6, bd=8, relief=RAISED)
                    b1.grid(row=row, column=column, sticky="N")
                    b1.bind("<Button 1>", lambda e=row, i=row, k=column: self.decide_movement(i, k))
                    b1.bind("<Button 3>", lambda e=row, i=row, k=column: self.move_piece(i, k))

        set_up_GUI()
        label_helper(0, 1)
        row_label_helper(1, 0)
        row_helper()
        row_label_helper(1, 9)
        label_helper(9, 1)

    # Gets the location of each button
    def get_grid_info(self):
        for key in self.labelframe.children.values():
            self.locations = int(key.grid_info()['row']), int(key.grid_info()['column'])
            self.button_location[self.locations] = key

    @staticmethod
    def directions_window():
        directions_window = Tk()
        directions_window.title("How To Operate The Board")

        label = Label(directions_window, text="Left Click to pick a piece \n Right Click to place the piece", height=20,
                      width=50)
        label.pack()

    # Clears the board backgrounds removing all green boxes (possible moves)
    def clear_board(self):
        for row1 in range(1, 9):
            for column1 in range(1, 9):
                if row1 % 2 == 0:
                    bg = "Black"
                    if column1 % 2 == 0:
                        bg = "White"
                else:
                    bg = "White"
                    if column1 % 2 == 0:
                        bg = "Black"
                self.button_location[row1, column1]["bg"] = bg

    # places the text (how the pieces move) and the images of each piece
    def place_pieces(self):
        for labels in self.white:
            self.button_location[8, self.white.index(labels) + 1].config(text=labels, fg="DimGray")
        x = 0
        for images in self.white_pieces:
            x += 1
            self.button_location[8, x].config(image=images, width=140, height=95)
        for labels in self.black:
            self.button_location[1, self.black.index(labels) + 1].config(text=labels, fg="OrangeRed")
        x = 0
        for images in self.black_pieces:
            x += 1
            self.button_location[1, x].config(image=images, width=140, height=95)
        for x in range(1, 9):
            self.button_location[7, x].config(text="PAWN", fg="DimGray",
                                              image=self.white_pawn, width=140, height=95)
            self.button_location[2, x].config(text="pawn", fg="OrangeRed",
                                              image=self.black_pawn, width=140, height=95)

    # wrapper for the Rook, Bishop and Knight movement
    @staticmethod
    def movement_check(error_check):
        def wrapper():
            try:
                error_check()
            except KeyError:
                pass

        return wrapper

    # Left clicking on a piece highlights the allowed boxes green depending on these functions
    # Right clicking on that green box would move the piece
    def pawn_movement(self, row, col, color):
        self.clear_board()
        if color == "DimGray":
            piece = "OrangeRed"
            x = -1
            y = -2
            z = 7
        else:
            piece = "DimGray"
            x = 1
            y = 2
            z = 2
        # If the pawn reaches the other side, pop up window for new piece
        if row == 1:
            self.new_piece_gui(row, col, color)
        if row == 8:
            self.new_piece_gui(row, col, color)
            
        # Makes sure the spot in front of the piece is empty
        if self.button_location[row + x, col]["text"] == "":
            if row == z:
                if self.button_location[(row + x), col + 1]["fg"] == piece:
                    self.button_location[(row + x), (col + 1)]["bg"] = "Green"
                self.button_location[(row + x), col]["bg"] = "Green"
                if self.button_location[(row + y), col]["text"] == "":
                    self.button_location[(row + y), col]["bg"] = "Green"
            else:
                if self.button_location[(row + x), col]["text"] == "":
                    self.button_location[(row + x), col]["bg"] = "Green"
        # If spot diagonal of the pawn is not empty highlights it to "eat" that piece
        if self.button_location[(row + x), (col + 1)]["fg"] == piece:
            self.button_location[(row + x), (col + 1)]["bg"] = "Green"

        if self.button_location[(row + x), (col - 1)]["fg"] == piece:
            self.button_location[(row + x), (col - 1)]["bg"] = "Green"

    # 4 For loops for each direction of Rook Movement
    def rook_movement(self, row, col, color):
        if color == "DimGray":
            piece = "OrangeRed"
        else:
            piece = "DimGray"
        for x in range(row + 1, 9):
            if self.button_location[x, col]["text"] == "":
                self.button_location[x, col]["bg"] = "Green"
            elif self.button_location[x, col]["fg"] == piece:
                self.button_location[x, col]["bg"] = "Green"
                break
            else:
                break
        for x in range(row - 1, 0, -1):
            if self.button_location[x, col]["text"] == "":
                self.button_location[x, col]["bg"] = "Green"
            elif self.button_location[x, col]["fg"] == piece:
                self.button_location[x, col]["bg"] = "Green"
                break
            else:
                break

        for x in range(col + 1, 9):
            if self.button_location[row, x]["text"] == "":
                self.button_location[row, x]["bg"] = "Green"
            elif self.button_location[row, x]["fg"] == piece:
                self.button_location[row, x]["bg"] = "Green"
                break
            else:
                break
        for x in range(col - 1, 0, -1):
            if self.button_location[row, x]["text"] == "":
                self.button_location[row, x]["bg"] = "Green"
            elif self.button_location[row, x]["fg"] == piece:
                self.button_location[row, x]["bg"] = "Green"
                break
            else:
                break

    def knight_movement(self, row, col, color):
        self.clear_board()
        if color == "DimGray":
            piece = "OrangeRed"
        else:
            piece = "DimGray"

        @self.movement_check
        def moving_up():
            if self.button_location[(row - 2), (col - 1)]["fg"] == piece:
                self.button_location[(row - 2), (col - 1)]["bg"] = "Green"

            if self.button_location[(row - 2), (col - 1)]["text"] == "":
                self.button_location[(row - 2), (col - 1)]["bg"] = "Green"

            if self.button_location[(row - 1), (col - 2)]["fg"] == piece:
                self.button_location[(row - 1), (col - 2)]["bg"] = "Green"

            if self.button_location[(row - 1), (col - 2)]["text"] == "":
                self.button_location[(row - 1), (col - 2)]["bg"] = "Green"

        @self.movement_check
        def moving_right():
            if self.button_location[(row - 2), (col + 1)]["fg"] == piece:
                self.button_location[(row - 2), (col + 1)]["bg"] = "Green"

            if self.button_location[(row - 2), (col + 1)]["text"] == "":
                self.button_location[(row - 2), (col + 1)]["bg"] = "Green"

            if self.button_location[(row - 1), (col + 2)]["fg"] == piece:
                self.button_location[(row - 1), (col + 2)]["bg"] = "Green"

            if self.button_location[(row - 1), (col + 2)]["text"] == "":
                self.button_location[(row - 1), (col + 2)]["bg"] = "Green"

        @self.movement_check
        def moving_down():
            if self.button_location[(row + 1), (col + 2)]["fg"] == piece:
                self.button_location[(row + 1), (col + 2)]["bg"] = "Green"

            if self.button_location[(row + 1), (col + 2)]["text"] == "":
                self.button_location[(row + 1), (col + 2)]["bg"] = "Green"

            if self.button_location[(row + 2), (col + 1)]["fg"] == piece:
                self.button_location[(row + 2), (col + 1)]["bg"] = "Green"

            if self.button_location[(row + 2), (col + 1)]["text"] == "":
                self.button_location[(row + 2), (col + 1)]["bg"] = "Green"

        @self.movement_check
        def moving_left():
            if self.button_location[(row + 2), (col - 1)]["fg"] == piece:
                self.button_location[(row + 2), (col - 1)]["bg"] = "Green"

            if self.button_location[(row + 2), (col - 1)]["text"] == "":
                self.button_location[(row + 2), (col - 1)]["bg"] = "Green"

            if self.button_location[(row + 1), (col - 2)]["fg"] == piece:
                self.button_location[(row + 1), (col - 2)]["bg"] = "Green"

            if self.button_location[(row + 1), (col - 2)]["text"] == "":
                self.button_location[(row + 1), (col - 2)]["bg"] = "Green"

        moving_up()
        moving_right()
        moving_left()
        moving_down()

    def bishop_movement(self, row, col, color):
        self.clear_board()
        if color == "DimGray":
            piece = "OrangeRed"
        else:
            piece = "DimGray"

        @self.movement_check
        def up_right():
            x = row - 1
            y = col + 1
            while x > 0:
                if self.button_location[x, y]["text"] == "":
                    self.button_location[x, y]["bg"] = "Green"
                elif self.button_location[x, y]["fg"] == piece:
                    self.button_location[x, y]["bg"] = "Green"
                    break
                else:
                    break
                x -= 1
                y += 1

        @self.movement_check
        def up_left():
            x = row - 1
            y = col - 1
            while x > 0:
                if self.button_location[x, y]["text"] == "":
                    self.button_location[x, y]["bg"] = "Green"
                elif self.button_location[x, y]["fg"] == piece:
                    self.button_location[x, y]["bg"] = "Green"
                    break
                else:
                    break
                x -= 1
                y -= 1

        @self.movement_check
        def down_left():
            x = row + 1
            y = col - 1
            while x > 0:
                if self.button_location[x, y]["text"] == "":
                    self.button_location[x, y]["bg"] = "Green"
                elif self.button_location[x, y]["fg"] == piece:
                    self.button_location[x, y]["bg"] = "Green"
                    break
                else:
                    break
                x += 1
                y -= 1

        @self.movement_check
        def down_right():
            x = row + 1
            y = col + 1
            while x > 0:
                if self.button_location[x, y]["text"] == "":
                    self.button_location[x, y]["bg"] = "Green"
                elif self.button_location[x, y]["fg"] == piece:
                    self.button_location[x, y]["bg"] = "Green"
                    break
                else:
                    break
                x += 1
                y += 1

        up_right()
        up_left()
        down_left()
        down_right()

    # Combines the movement of the rook and the bishop
    def queen_movement(self, row, col, color):
        self.clear_board()
        self.bishop_movement(row, col, color)
        self.rook_movement(row, col, color)

    def king_movement(self, row, col, color):
        self.clear_board()
        if color == "DimGray":
            piece = "OrangeRed"
            self.white_castle(col)
        else:
            piece = "DimGray"
            self.black_castle(col)
        for x in range(-1, 2):
            for y in range(-1, 2):
                if self.button_location[(row + x), (col + y)]["text"] == "":
                    self.button_location[(row + x), (col + y)]["bg"] = "Green"
                elif self.button_location[(row + x), (col + y)]["fg"] == piece:
                    self.button_location[(row + x), (col + y)]["bg"] = "Green"
                    
    def white_castle(self, col):
        # Caslteing option
        # Checks if the king has moved
        moved = True
        castleing_left = False
        castleing_right = False
        for x in self.white_king_locations:
            if x == (8, 5):
                moved = False
            else:
                moved = True
                break

        # Checks if spots are open to the left or right
        if moved is False:
            for x in range(col+1, 8):
                if self.button_location[(8, x)]["text"] == "":
                    castleing_right = True
                else:
                    castleing_right = False
                    break
            for x in range(col-1, 1, -1):
                if self.button_location[(8, x)]["text"] == "":
                    castleing_left = True
                else:
                    castleing_left = False
                    break

        # if spots are open and the king hasn't moved checks to see if the Rook is there
        # castles if Rook is there.
        if castleing_right:
            if self.button_location[8, 8]["text"] == "ROOK.":
                self.button_location[8, 7]["bg"] = "Green"
        if castleing_left:
            if self.button_location[8, 1]["text"] == "ROOK":
                self.button_location[8, 3]["bg"] = "Green"

    def black_castle(self, col):
        # Caslteing option
        # Checks if the king has moved
        moved = True
        castleing_left = False
        castleing_right = False
        for x in self.black_king_locations:
            if x == (1, 5):
                moved = False
            else:
                moved = True
                break

        # Checks if spots are open to the left or right
        if moved is False:
            for x in range(col+1, 8):
                if self.button_location[(1, x)]["text"] == "":
                    castleing_right = True
                else:
                    castleing_right = False
                    break
            for x in range(col-1, 1, -1):
                if self.button_location[(1, x)]["text"] == "":
                    castleing_left = True
                else:
                    castleing_left = False
                    break

        # if spots are open and the king hasn't moved checks to see if the Rook is there
        # castles if Rook is there.
        if castleing_right:
            if self.button_location[1, 8]["text"] == "rook.":
                self.button_location[1, 7]["bg"] = "Green"
        if castleing_left:
            if self.button_location[1, 1]["text"] == "rook":
                self.button_location[1, 3]["bg"] = "Green"

    # Function to get called to castle
    def move_pieces_castleing(self, row, col):
        if self.piece == "KING":
            if self.original_row == 8 and self.original_col == 5:
                if row == 8 and col == 7:
                    self.button_location[8, 6].config(text="ROOK.", image=self.white_pieces[0],
                                                      width=140, height=95, fg="DimGray")
                    self.button_location[8, 8].config(text="", image="", height=6, width=20)
                if row == 8 and col == 3:
                    self.button_location[8, 4].config(text="ROOK", image=self.white_pieces[0],
                                                      width=140, height=95, fg="DimGray")
                    self.button_location[8, 1].config(text="", image="", height=6, width=20)

        if self.piece == "king":
            if self.original_row == 1 and self.original_col == 5:
                if row == 1 and col == 7:
                    self.button_location[1, 6].config(text="rook.", image=self.black_pieces[0],
                                                      width=140, height=95, fg="OrangeRed")
                    self.button_location[1, 8].config(text="", image="", height=6, width=20)
                if row == 1 and col == 3:
                    self.button_location[1, 4].config(text="rook", image=self.black_pieces[0],
                                                      width=140, height=95, fg="OrangeRed")
                    self.button_location[1, 1].config(text="", image="", height=6, width=20)

    # Takes in the text of the button clicked and goes through the dictionary to get to the correct movement of that
    # specific piece
    def decide_movement(self, row, col):
        movement = {
            "PAWN": self.pawn_movement, "ROOK": self.rook_movement, "ROOK.": self.rook_movement,
            "KNIGHT": self.knight_movement, "KNIGHT.": self.knight_movement,
            "BISHOP": self.bishop_movement, "BISHOP.": self.bishop_movement,
            "QUEEN": self.queen_movement, "KING": self.king_movement,
            "pawn": self.pawn_movement, "rook": self.rook_movement, "rook.": self.rook_movement,
            "knight": self.knight_movement, "knight.": self.knight_movement,
            "bishop": self.bishop_movement, "bishop.": self.bishop_movement,
            "queen": self.queen_movement, "king": self.king_movement}
        try:
            self.piece = self.button_location[row, col]["text"]
            self.piece_color = self.button_location[row, col]["fg"]
            self.original_row = row
            self.original_col = col
            self.piece_image = self.button_location[row, col]["image"]
            if self.turn % 2 == 0:
                if self.piece_color == "OrangeRed":
                    movement.get(self.piece)(row, col, color=self.piece_color)
                else:
                    self.clear_board()
                    wrong_turn_window = Toplevel()
                    wrong_turn_window.title("Wrong Turn")
                    wrong_turn_window.lift()

                    label = Label(wrong_turn_window, text="It's Not Your Turn!")
                    label.pack()

            if self.turn % 2 != 0:
                if self.piece_color == "DimGray":
                    movement.get(self.piece)(row, col, color=self.piece_color)
                else:
                    self.clear_board()
                    wrong_turn_window = Toplevel()
                    wrong_turn_window.title("Wrong Turn")
                    wrong_turn_window.lift()

                    label = Label(wrong_turn_window, text="It's Not Your Turn!")
                    label.pack()
                    
        # for clicking where there is no piece
        except TypeError:
            no_piece_window = Toplevel()
            no_piece_window.title("Wrong Click")
            no_piece_window.lift()

            label = Label(no_piece_window, text="There is no piece there")
            label.pack()

    # Moves the piece to the new button that was right-clicked and clears the original button of the text and image
    # Then checks to see if either king is in Check
    def move_piece(self, row, col):
        if self.button_location[row, col]["bg"] == "Green":
            self.button_location[row, col]["text"] = self.piece
            self.button_location[row, col]["fg"] = self.piece_color
            self.button_location[row, col].config(image=self.piece_image, width=140, height=95)
            self.move_pieces_castleing(row, col)
            self.piece = ""
            self.piece_color = ""
            self.button_location[self.original_row, self.original_col]["text"] = ""
            self.button_location[self.original_row, self.original_col]["fg"] = "white"
            self.button_location[self.original_row, self.original_col].config(image="", width=20, height=6)
            self.clear_board()
            self.king_in_danger()
            self.clear_board()
            self.turn += 1

        else:
            self.clear_board()

    # Checks to see if the king is in Check and a window pops up if the king is
    def king_in_danger(self):
        movement = {
            "PAWN": self.pawn_movement, "ROOK": self.rook_movement, "ROOK.": self.rook_movement,
            "KNIGHT": self.knight_movement, "KNIGHT.": self.knight_movement,
            "BISHOP": self.bishop_movement, "BISHOP.": self.bishop_movement,
            "QUEEN": self.queen_movement, "KING": self.king_movement,
            "pawn": self.pawn_movement, "rook": self.rook_movement, "rook.": self.rook_movement,
            "knight": self.knight_movement, "knight.": self.knight_movement,
            "bishop": self.bishop_movement, "bishop.": self.bishop_movement,
            "queen": self.queen_movement, "king": self.king_movement, "": self.pass_this}

        king_row = 1
        king_col = 1
        king_row1 = 1
        king_col1 = 1

        # Finds the king for each side
        for row2 in range(1, 9):
            for col2 in range(1, 9):
                piece_text = self.button_location[row2, col2]["text"]
                piece_row1 = row2
                piece_col1 = col2
                if piece_text == "KING":
                    king_row = piece_row1
                    king_col = piece_col1
                if piece_text == "king":
                    king_row1 = piece_row1
                    king_col1 = piece_col1
        self.white_king_locations.append((king_row, king_col))
        self.black_king_locations.append((king_row1, king_col1))

        # Runs each piece's movement in their specific location to see if they put the king in Check
        done = False
        for row1 in range(1, 9):
            if done:
                break
            for column1 in range(1, 9):
                piece_text = self.button_location[row1, column1]["text"]
                piece_color = self.button_location[row1, column1]["fg"]
                piece_row = row1
                piece_col = column1
                movement.get(piece_text)(row=piece_row, col=piece_col, color=piece_color)
                if self.button_location[king_row, king_col]["bg"] == "Green":
                    check_window = Toplevel()
                    check_window.title("CHECK!")
                    label = Label(check_window, text="CHECK!", height=20, width=50, fg="Blue")
                    label.pack()
                    done = True
                    break
                if self.button_location[king_row1, king_col1]["bg"] == "Green":
                    check_window = Toplevel()
                    check_window.title("CHECK!")
                    label = Label(check_window, text="CHECK!", height=20, width=50, fg="Red")
                    label.pack()
                    done = True
                    break

    # GUI to pop up when a pawn reaches the other side
    def new_piece_gui(self, row, col, color):
        if color == "DimGray":
            queen = self.white_pieces[3]
            rook = self.white_pieces[0]
            bishop = self.white_pieces[2]
            knight = self.white_pieces[1]
        else:
            queen = self.black_pieces[3]
            rook = self.black_pieces[0]
            bishop = self.black_pieces[2]
            knight = self.black_pieces[1]
            
        self.piece_window = Toplevel()
        self.piece_window.title("Pick Your Piece")
        queen_label = Label(self.piece_window, text="Queen")
        rook_label = Label(self.piece_window, text="Rook")
        bishop_label = Label(self.piece_window, text="Bishop")
        knight_label = Label(self.piece_window, text="Knight")
        queen_label.grid(row=0, column=0, pady=10, padx=20)
        rook_label.grid(row=1, column=0, pady=10, padx=20)
        bishop_label.grid(row=2, column=0, pady=10, padx=20)
        knight_label.grid(row=3, column=0, pady=10, padx=20)
        queen_button = Button(self.piece_window, image=queen, width=140, height=90, bg="white")
        rook_button = Button(self.piece_window, image=rook, width=140, height=90, bg="black")
        bishop_button = Button(self.piece_window, image=bishop, width=140, height=90, bg="white")
        knight_button = Button(self.piece_window, image=knight, width=140, height=90, bg="black")
        queen_button.config(command=lambda e=row, i=row, j=col, k=color: self.place_queen(i, j, k))
        rook_button.config(command=lambda e=row, i=row, j=col, k=color: self.place_rook(i, j, k))
        bishop_button.config(command=lambda e=row, i=row, j=col, k=color: self.place_bishop(i, j, k))
        knight_button.config(command=lambda e=row, i=row, j=col, k=color: self.place_knight(i, j, k))
        queen_button.grid(row=0, column=1)
        rook_button.grid(row=1, column=1)
        bishop_button.grid(row=2, column=1)
        knight_button.grid(row=3, column=1)
    
    # Replace Pawn with Queen
    def place_queen(self, row, col, color):
        if color == "DimGray":
            image = self.white_pieces[3]
            text = "QUEEN"
        else:
            image = self.black_pieces[3]
            text = "queen"
        self.button_location[row, col].config(text=text, image=image, width=140, height=95)
        self.piece_window.destroy()
        self.king_in_danger()
        self.clear_board()
    
    # Replace Pawn wtih Rook
    def place_rook(self, row, col, color):
        if color == "DimGray":
            image = self.white_pieces[0]
            text = "ROOK"
        else:
            image = self.black_pieces[0]
            text = "rook"
        self.button_location[row, col].config(text=text, image=image, width=140, height=95)
        self.piece_window.destroy()
        self.king_in_danger()
        self.clear_board()
    
    # Replace Pawn with Bishop
    def place_bishop(self, row, col, color):
        if color == "DimGray":
            image = self.white_pieces[2]
            text = "BISHOP"
        else:
            image = self.black_pieces[2]
            text = "bishop"
        self.button_location[row, col].config(text=text, image=image, width=140, height=95)
        self.piece_window.destroy()
        self.king_in_danger()
        self.clear_board()

    # Replace Pawn with Knight
    def place_knight(self, row, col, color):
        if color == "DimGray":
            image = self.white_pieces[1]
            text = "KNIGHT"
        else:
            image = self.black_pieces[1]
            text = "knight"
        self.button_location[row, col].config(text=text, image=image, width=140, height=95)
        self.piece_window.destroy()
        self.king_in_danger()
        self.clear_board()

    # Resets everything
    def new_game(self):
        for x in range(1, 9):
            for y in range(1, 9):
                self.button_location[x, y].config(text="", image="", width=20, height=6)
        self.place_pieces()
        self.turn = 1

    def exit(self, _=None):
        self.quit()
        self.destroy()

    def pass_this(self, row, col, color):
        pass

ChessBoard(Tk())
