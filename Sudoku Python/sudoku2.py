from tkinter import filedialog, messagebox
import tkinter as tk

class SudokuGame:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.history = []

    def load_initial_configuration(self, file_path):
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                for j, char in enumerate(line.strip()):
                    self.board[i][j] = int(char) if char.isdigit() else 0

    def make_move(self, row, col, number):
        if self.is_valid_move(row, col, number):
            self.board[row][col] = number
            self.history.append((row, col, number, 'New Move'))
            if self.is_game_over():
                self.history.append(('Game Over',))
            return True
        return False

    def undo_move(self):
        if self.history:
            last_move = self.history.pop()
            if last_move[-1] == 'New Move':
                row, col, _, _ = last_move
                self.board[row][col] = 0

    def redo_move(self):
        if self.history:
            last_move = self.history[-1]
            if last_move[-1] == 'New Move':
                row, col, number, _ = last_move
                if self.is_valid_move(row, col, number):
                    self.board[row][col] = number
                    self.history.append((row, col, number, 'Redo Move'))
                    if self.is_game_over():
                        self.history.append(('Game Over',))
                    return True
        return False

    def suggest_move(self, row, col):
        current_number = self.board[row][col]
        suggestions = [num for num in range(1, 10) if self.is_valid_move(row, col, num)]
        suggestions.remove(current_number) if current_number != 0 else suggestions
        return suggestions

    def is_valid_move(self, row, col, number):
        return (
            self.is_valid_row(row, number) and
            self.is_valid_col(col, number) and
            self.is_valid_region(row, col, number)
        )

    def is_valid_row(self, row, number):
        return number not in self.board[row]

    def is_valid_col(self, col, number):
        return number not in [self.board[row][col] for row in range(9)]

    def is_valid_region(self, row, col, number):
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == number:
                    return False
        return True

    def is_game_over(self):
        for i in range(9):
            if not (self.is_valid_row(i, 0) and
                    self.is_valid_col(0, i) and
                    self.is_valid_region(i // 3 * 3, (i % 3) * 3, 0)):
                return False
        return True

    def display_board(self):
        for row in self.board:
            print(" ".join(map(str, row)))

    def display_history(self):
        for move in self.history:
            print(move)

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Game")

        self.create_widgets()

        self.game = SudokuGame()

    def create_widgets(self):
        # Configuración de la ventana principal
        self.master.geometry("400x500")

        # Botón para cargar configuración
        self.load_button = tk.Button(self.master, text="Load Configuration", command=self.load_configuration_from_file)
        self.load_button.pack(pady=10)

        # Etiquetas y entradas para fila, columna y número
        tk.Label(self.master, text="Row:").pack(side=tk.LEFT, padx=5)
        self.row_entry = tk.Entry(self.master, width=5)
        self.row_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.master, text="Column:").pack(side=tk.LEFT, padx=5)
        self.col_entry = tk.Entry(self.master, width=5)
        self.col_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.master, text="Number:").pack(side=tk.LEFT, padx=5)
        self.num_entry = tk.Entry(self.master, width=5)
        self.num_entry.pack(side=tk.LEFT, padx=5)

        # Botones para realizar una jugada y deshacer una jugada
        self.make_move_button = tk.Button(self.master, text="Make Move", command=self.make_move)
        self.make_move_button.pack(pady=10)

        self.undo_button = tk.Button(self.master, text="Undo Move", command=self.undo_move)
        self.undo_button.pack(pady=10)

        # Widget Text para mostrar la tabla de Sudoku
        self.board_text = tk.Text(self.master, height=9, width=21, font=("Courier New", 12), bg="lightgrey")
        self.board_text.pack(pady=10)

        # Etiqueta para mostrar el historial
        self.history_label = tk.Label(self.master, text="", font=("Arial", 10))
        self.history_label.pack()

    def load_configuration_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.game.load_initial_configuration(file_path)
            self.display_board()

    def make_move(self):
        try:
            row = int(self.row_entry.get())
            col = int(self.col_entry.get())
            number = int(self.num_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")
            return

        if not (1 <= row <= 9 and 1 <= col <= 9 and 1 <= number <= 9):
            messagebox.showerror("Error", "Please enter numbers between 1 and 9.")
            return

        if self.game.make_move(row - 1, col - 1, number):
            self.display_board()

    def undo_move(self):
        self.game.undo_move()
        self.display_board()

    def display_board(self):
        # Limpiamos el contenido actual en el widget Text
        self.board_text.delete("1.0", tk.END)
        # Insertamos la tabla de Sudoku en el widget Text
        for row in self.game.board:
            self.board_text.insert(tk.END, " ".join(map(str, row)) + "\n")

    def display_history(self):
        history_str = "\n".join([str(move) for move in self.game.history])
        self.history_label.config(text="History:\n" + history_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()




