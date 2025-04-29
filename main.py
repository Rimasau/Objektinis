import tkinter as tk
from tkinter import messagebox
import random


class Ship:
    def __init__(self, size):
        self.size = size
        self.hit_count = 0

    def ship_sunk(self):
        return self.hit_count >= self.size


class Carrier(Ship):
    def __init__(self):
        super().__init__(size=5)


class Battleship(Ship):
    def __init__(self):
        super().__init__(size=4)


class Cruiser(Ship):
    def __init__(self):
        super().__init__(size=3)


class Submarine(Ship):
    def __init__(self):
        super().__init__(size=3)


class Destroyer(Ship):
    def __init__(self):
        super().__init__(size=2)


class ShipFactory:
    @staticmethod
    def create_ship(ship_type):
        if ship_type == 'Carrier':
            return Carrier()
        elif ship_type == 'Battleship':
            return Battleship()
        elif ship_type == 'Cruiser':
            return Cruiser()
        elif ship_type == 'Submarine':
            return Submarine()
        elif ship_type == 'Destroyer':
            return Destroyer()
        else:
            raise ValueError(f"Unknown ship type: {ship_type}")


class GUI:
    def __init__(self, grid_file, winner_file):
        self.grid_file = grid_file
        self.winner_file = winner_file
        self.grid_size = self.read_grid_size()
        self.player_grid = [['•' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.cpu_grid = [['•' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        ship_type = ['Carrier', 'Battleship', 'Cruiser', 'Submarine', 'Destroyer',]
        self.player_ships = [ShipFactory.create_ship(st) for st in ship_type]
        self.cpu_ships = [ShipFactory.create_ship(st) for st in ship_type]
        self.player_hits = 0
        self.cpu_hits = 0
        self.root = tk.Tk()
        self.root.iconbitmap("krok.ico")
        self.root.title("Croca croca")
        self.enemy_buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.player_buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.setup_game()

    def read_grid_size(self):
        with open(self.grid_file, 'r') as file:
            line = file.readline().strip()
            if not line:
                raise ValueError("Grid size file is empty")
            return int(line)

    def write_winner(self, winner):
        with open(self.winner_file, 'a') as file:
            file.write(f"Laimejo {winner}!\n")

    def setup_game(self):
        for ship in self.player_ships:
            self.place_ship(self.player_grid, ship)
        for ship in self.cpu_ships:
            self.place_ship(self.cpu_grid, ship)

        tk.Label(self.root, text="Tavo zemelapis:").grid(row=0, column=0, columnspan=self.grid_size)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                text = 'O' if self.player_grid[y][x] == 'O' else '•'
                btn = tk.Label(self.root, text=text, width=4, borderwidth=1, relief="solid")
                btn.grid(row=y + 1, column=x)
                self.player_buttons[y][x] = btn

        offset = self.grid_size + 4
        tk.Label(self.root, text="Priesininko zemelapis:",fg="red").grid(row=0, column=offset, columnspan=self.grid_size)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                btn = tk.Button(self.root, text="•", width=4, command=lambda x=x, y=y: self.player_turn(x, y))
                btn.grid(row=y + 1, column=x + offset)
                self.enemy_buttons[y][x] = btn

    def place_ship(self, grid, ship):
        while True:
            direction = random.choice(['horizontal', 'vertical'])
            if direction == 'horizontal':
                x = random.randint(0, self.grid_size - ship.size)
                y = random.randint(0, self.grid_size - 1)
            else:
                x = random.randint(0, self.grid_size - 1)
                y = random.randint(0, self.grid_size - ship.size)

            valid = True
            for i in range(ship.size):
                if direction == 'horizontal' and grid[y][x + i] != '•':
                    valid = False
                    break
                elif direction == 'vertical' and grid[y + i][x] != '•':
                    valid = False
                    break

            if valid:
                for i in range(ship.size):
                    if direction == 'horizontal':
                        grid[y][x + i] = 'O'
                    else:
                        grid[y + i][x] = 'O'
                break

    def player_turn(self, x, y):
        if self.cpu_grid[y][x] in ['X', 'N']:
            return

        if self.cpu_grid[y][x] == 'O':
            self.cpu_grid[y][x] = 'X'
            self.enemy_buttons[y][x].config(text='X', bg='green')
            self.player_hits += 1
        else:
            self.cpu_grid[y][x] = 'N'
            self.enemy_buttons[y][x].config(text='N', bg='red')

        if self.player_hits == sum(ship.size for ship in self.cpu_ships):
            messagebox.showinfo("Pabaiga", "Tu laimejai!")
            self.write_winner("Zaidejas")
            self.root.quit()
        else:
            self.root.after(100, self.cpu_turn)

    def cpu_turn(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if self.player_grid[y][x] in ['X', 'N']:
                continue

            if self.player_grid[y][x] == 'O':
                self.player_grid[y][x] = 'X'
                self.player_buttons[y][x].config(text='X', bg='red')
                self.cpu_hits += 1
            else:
                self.player_grid[y][x] = 'N'
                self.player_buttons[y][x].config(text='N', bg='green')
            break

        if self.cpu_hits == sum(ship.size for ship in self.player_ships):
            messagebox.showinfo("Pabaiga", "Laimejo priesininkas!")
            self.write_winner("Kompiuteris")
            self.root.quit()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    grid_file = 'grid_size.txt'
    winner_file = 'winner.txt'
    game = GUI(grid_file, winner_file)
    game.run()
