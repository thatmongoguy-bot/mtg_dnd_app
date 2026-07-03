import tkinter as tk
from tkinter import ttk, messagebox

class MTG_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MTG Assistant")
        self.root.geometry("500x400")
        self.player_frames = []

        self.setup_screen()
    
    def setup_screen(self):
        """Setup the initial screen with format and player selection"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        tk.Label(self.root, text="MTG Assistant", font=("Arial", 24)).pack(pady=10)
        
        # Format selection
        tk.Label(self.root, text="Select Format:").pack(pady=(10,0))
        self.format_var = tk.StringVar(value="Standard")
        tk.Radiobutton(self.root, text="Standard (20 life)", variable=self.format_var, value="Standard").pack()
        tk.Radiobutton(self.root, text="Commander (40 life)", variable=self.format_var, value="Commander").pack()
        
        # Player count
        tk.Label(self.root, text="Number of Players (2-8):").pack(pady=(10,0))
        self.player_count = tk.IntVar(value=2)
        self.player_count.trace('w', lambda *args: self.update_name_entries())  # Update names when player count changes
        spinbox = ttk.Spinbox(self.root, from_=2, to=8, textvariable=self.player_count, width=5)
        spinbox.pack()
        
        # Player names
        self.name_frame = tk.Frame(self.root)
        self.name_frame.pack(pady=10)
        self.name_entries = []
        self.update_name_entries()
        
        # Start button
        start_btn = tk.Button(self.root, text = "> Start Game", 
        command = self.start_game, 
        
        font = ("Arial", 14, "bold"), 
        relief = "raised", bd = 4, padx = 20, pady = 5)
        start_btn.pack(pady = 10)
        self.root.update()  # Ensure the GUI updates after adding the start button

    
    def update_name_entries(self):
        #print("Debug: update_name_entries called")  # Debug statement
        """Create name entry fields based on player count"""
        for widget in self.name_frame.winfo_children():
            widget.destroy()
        self.name_entries = []
        
        for i in range(self.player_count.get()):
            tk.Label(self.name_frame, text=f"Player {i+1}:").grid(row=i, column=0, padx=5, pady=2)
            entry = tk.Entry(self.name_frame, width=20)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.name_entries.append(entry)
            self.root.update()  # Ensure the GUI updates after adding each entry
    
    def start_game(self):
        from game import Game

        format_type = self.format_var.get()
        self.game = Game(format_type)

        for entry in self.name_entries:
            name = entry.get().strip()
            if not name:
                messagebox.showerror("Input Error", "All player names must be filled.")
                return
            self.game.add_player(name)
        self.game.save_state()
        self.show_game_screen()

    def show_game_screen(self):
        # Display the main game screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.player_frames = []  # Reset player frames list

        tk.Label(self.root, 
        text = f"{self.game.format_type} Game",
        font = ("Arial", 18)).pack(pady = 5)

        # Show each player
        for i, player in enumerate(self.game.players):
            print(f"DEBUG: creating frame for {player.name}")
            
            frame = tk.LabelFrame(self.root,
            text = player.name, font = ("Arial", 12, "bold"))
            
            frame.pack(fill = "x", padx = 10, pady = 5)
            
            self.player_frames.append(frame)

        # Life
            tk.Label(frame, text = "Life:", font = ("Arial", 10)).grid(row = 0, column = 0, padx = 5, pady = 2)
            life_label = tk.Label(frame, text = str(player.life.value), font = ("Arial", 16, "bold"))
            life_label.grid(row = 0, column = 1, padx = 5, pady = 2)


            tk.Button(frame, text = "-", command = lambda idx = i:
                self.change_life(idx, -1), width = 3).grid(row = 0, column = 2, padx =2)
            tk.Button(frame, text = "+", command = lambda idx = i:
                self.change_life(idx, 1), width = 3).grid(row = 0, column = 3, padx = 2)

        # Poison
            tk.Label(frame, text = "Poison:", font = ("Arial", 10)).grid(row = 1, column = 0, padx = 5, pady = 2)
            
            poison_label = tk.Label(frame, text = str(player.poison.value), font = ("Arial", 12))
            poison_label.grid(row = 1, column = 1, padx = 5, pady = 2)
            
            tk.Button(frame, text = "+ Poison", command = lambda idx = i:
                self.add_poison(idx)).grid(row = 1, column = 2, columnspan = 2, padx = 2)

            print(f"DEBUG: created frame for {player.name} with life {player.life.value} and poison {player.poison.value}")

        # Store labels for updating
            frame.life_label = life_label
            frame.poison_label = poison_label
            self.player_frames = [] # reset the list  
            self.player_frames.append(frame)

    def change_life(self, index, amount):
        player = self.game.players[index]
        if amount == -1:
            player.life.decrement()
        else:
            player.life.increment()
        self.update_display()

    def add_poison(self, index):
        self.game.players[index].poison.increment()
        self.update_display()

    def update_display(self):
        for i, frame in enumerate(self.player_frames):
            player = self.game.players[i]
            frame.life_label.config(text = str(player.life.value))
            frame.poison_label.config(text = str(player.poison.value))

if __name__ == "__main__":
    root = tk.Tk()
    app = MTG_GUI(root)
    root.mainloop()