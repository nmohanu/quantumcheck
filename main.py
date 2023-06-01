import tkinter as tk
import random

# Create the main window
root = tk.Tk()
root.title("Chessboard")

# Define the dimensions of the chessboard
board_width = 8
board_height = 8
cell_size = 80  # Adjust this value to change the size of the cells

# Create a canvas to draw the chessboard
canvas = tk.Canvas(root, width=board_width * cell_size, height=board_height * cell_size)
canvas.pack()

# Initialize the chessboard
chessboard = [[' ' for _ in range(board_width)] for _ in range(board_height)]
chessboard[0] = ['P' for _ in range(board_width)]  # Add pawns to the second row for black
chessboard[7] = ['p' for _ in range(board_width)]  # Add pawns to the seventh row for white

# Create a dictionary to store the piece IDs on the canvas
piece_ids = {}

# Define colors for the chessboard
light_color = "#C3DFA5"  # Light green
dark_color = "#8BBF6E"   # Dark green

# Draw the chessboard with pieces
for row in range(board_height):
    for col in range(board_width):
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        # Alternate the colors of the cells
        fill_color = light_color if (row + col) % 2 == 0 else dark_color

        canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)

        # Draw the piece if there is one in the current cell
        piece = chessboard[row][col]
        if piece != ' ':
            if piece.isupper():
                color = "#000000"  # Black piece
            else:
                color = "#FFFFFF"  # White piece

            piece_id = canvas.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=color)
            piece_ids[(row, col)] = piece_id

# Variables to store the currently selected piece and its original position
selected_piece = None
original_pos = None

# Variable to store the current player's turn ('W' for white, 'B' for black)
current_player = 'W'

# Function to handle the piece dragging
def start_drag(event):
    global selected_piece, original_pos

    # Get the cell indices based on the mouse click coordinates
    col = event.x // cell_size
    row = event.y // cell_size

    # Check if there is a piece in the clicked cell and if it's the current player's turn
    if (row, col) in piece_ids and (chessboard[row][col].isupper() if current_player == 'W' else chessboard[row][col].islower()):
        selected_piece = piece_ids[(row, col)]
        original_pos = (row, col)
        canvas.tag_raise(selected_piece)  # Bring the selected piece to the front

import random

import random

def end_drag(event):
    global selected_piece, original_pos, current_player

    # Check if a piece was selected and dragged
    if selected_piece is not None:
        # Get the cell indices based on the drop coordinates
        col = event.x // cell_size
        row = event.y // cell_size

        # Move the piece to the new cell if it's a valid move and it's the current player's turn
        if (row, col) != original_pos and (chessboard[row][col] == ' ' or (chessboard[original_pos[0]][original_pos[1]].isupper() != chessboard[row][col].isupper())):
            piece = chessboard[original_pos[0]][original_pos[1]]

            # Determine the direction of movement based on the color of the piece
            direction = 1 if piece.isupper() else -1

            # Check if the move is valid for pawns (forward movement)
            if (row - original_pos[0]) == direction:
                # Check if there is a piece in the target cell and attempt to capture it
                if chessboard[row][col] != ' ':
                    # Check if the capturing piece has a blue outline
                    if canvas.itemcget(selected_piece, 'outline') == 'blue':
                        # Reset the selected piece and original position
                        selected_piece = None
                        original_pos = None
                        return

                    # Perform a 50% chance of successful capture
                    capture_success = random.choice([True, False])
                    if capture_success:
                        # Remove the captured piece from the canvas
                        canvas.delete(piece_ids[(row, col)])
                    else:
                        # Add a blue outline to the attempted captured piece
                        canvas.itemconfigure(piece_ids[(row, col)], outline='blue')

                        # Reset the selected piece and original position
                        selected_piece = None
                        original_pos = None
                        return

                chessboard[row][col] = piece
                chessboard[original_pos[0]][original_pos[1]] = ' '

                # Update the piece ID with the new cell indices
                piece_ids[(row, col)] = selected_piece
                del piece_ids[original_pos]

                # Calculate the new position on the canvas
                x = col * cell_size + cell_size // 2
                y = row * cell_size + cell_size // 2

                # Move the piece to the new position
                canvas.coords(selected_piece, x - 30, y - 30, x + 30, y + 30)

                # Switch the current player's turn
                current_player = 'B' if current_player == 'W' else 'W'

    # Reset the selected piece and original position
    selected_piece = None
    original_pos = None


    # Reset the selected piece and original position
    selected_piece = None
    original_pos = None


    canvas.bind("<ButtonRelease-1>", end_drag)


    # Reset the selected piece and original position
    selected_piece = None
    original_pos = None



# Bind the mouse click and release events to the respective functions
canvas.bind("<Button-1>", start_drag)
canvas.bind("<ButtonRelease-1>", end_drag)

# Start the main loop
root.mainloop()