import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import MovimientoMaquina

class StartScreen:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        
        self.window = tk.Toplevel(root)
        self.window.title("Seleccionar Dificultad")
        self.window.geometry("300x150")
        
        # Centrar la ventana
        window_width = 300
        window_height = 150
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        tk.Label(self.window, text="Seleccione la dificultad", font=("Arial", 12)).pack(pady=10)
        
        self.difficulty = ttk.Combobox(
            self.window, 
            values=["Principiante", "Amateur", "Experto"],
            state="readonly"
        )
        self.difficulty.current(1)  # Selecciona "Amateur" por defecto
        self.difficulty.pack(pady=10)
        
        tk.Button(
            self.window, 
            text="Comenzar Juego", 
            command=self.start_game,
            font=("Arial", 10)
        ).pack(pady=10)
        
    def start_game(self):
        difficulty = self.difficulty.get()
        self.callback(difficulty)
        self.window.destroy()

class YoshiBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Yoshi's Zones")
        
        # Configuración del tablero
        self.board_size = 8
        self.cell_size = 60
        self.canvas_size = self.board_size * self.cell_size

        # Mostrar pantalla de inicio
        self.difficulty_level = None
        self.start_screen = StartScreen(root, self.set_difficulty)
        # Esperar a que se seleccione la dificultad antes de continuar
        self.root.wait_window(self.start_screen.window)
        # Configurar profundidad según dificultad
        self.depth = {
            "Principiante": 2,
            "Amateur": 4,
            "Experto": 6
        }.get(self.difficulty_level, 4)  # Default a Amateur si hay algún problema

        # Posiciones iniciales de los Yoshis
        self.green_yoshi_pos = (0, 0)
        self.red_yoshi_pos = (0, 0)
        # Posicion aleatoria yoshis
        def posicion_aleatoria():
            x = random.randint(1,6)
            y = random.randint(1,6)
            return((x,y))
        self.green_yoshi_pos = posicion_aleatoria()
        self.red_yoshi_pos = posicion_aleatoria()
        #Nunca pueden quedar en al misma celda
        while self.green_yoshi_pos == self.red_yoshi_pos:
            self.red_yoshi_pos = posicion_aleatoria()
        
        # Turno inicial (verde comienza)
        self.current_turn = "green"
        
        # Puntuación
        self.green_score = 0
        self.red_score = 0
        
        # Casillas especiales pintadas (guardamos el color con que fueron pintadas)
        self.painted_cells = {}  # Formato: {(row, col): "color"}
        
        # Definir las zonas especiales
        self.special_zones = {
            # Esquina superior izquierda
            "superior_izquierda": [(0,0), (0,1), (0,2), (1,0), (2,0)],
            # Esquina superior derecha
            "superior_derecha": [(0,7), (0,6), (0,5), (1,7), (2,7)],
            # Esquina inferior izquierda
            "inferior_izquierda": [(7,0), (7,1), (7,2), (6,0), (5,0)],
            # Esquina inferior derecha
            "inferior_derecha": [(7,7), (7,6), (7,5), (6,7), (5,7)]
        }
        
        # Controlar si el juego ha terminado
        self.game_over = False
        
        # Crear frame superior para controles
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)
        
        # Lista desplegable de dificultad
        self.difficulty_label = tk.Label(self.top_frame, text=f"Dificultad: {self.difficulty_level}", font=("Arial", 10))
        self.difficulty_label.pack(side=tk.LEFT, padx=10)
        
        # Botón de reinicio
        self.reset_button = tk.Button(self.top_frame, text="Reiniciar", command=self.reset_game)
        self.reset_button.pack(side=tk.LEFT, padx=10)
        
        # Frame para información del juego
        self.info_frame = tk.Frame(root)
        self.info_frame.pack(pady=5)
        
        # Indicador de turno
        self.turn_label = tk.Label(self.info_frame, text="Turno: Yoshi Verde", fg="#2ecc71", font=("Arial", 10, "bold"))
        self.turn_label.pack(side=tk.LEFT, padx=20)
        
        # Marcador de puntuación
        self.score_label = tk.Label(
            self.info_frame, 
            text="Verde: 0 - Rojo: 0", 
            font=("Arial", 10, "bold")
        )
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        # Crear canvas
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()
        
        # Dibujar elementos
        self.draw_board()
        self.mark_special_zones()
        self.draw_yoshis()
        
        # Vincular evento de clic
        self.canvas.bind("<Button-1>", self.on_cell_click)
        
        # Almacenar posibles movimientos
        self.possible_moves = []

        # Primer movimiento de la maquina
        time.sleep(0.5)
        if self.current_turn == "green":
            print("==================================")
            movimiento = MovimientoMaquina.MovimientoMaquina(self.special_zones,self.painted_cells, self.green_yoshi_pos, self.red_yoshi_pos,self.depth)
            print(str(movimiento)+ "*************************************************")
            self.move_yoshi(movimiento[0], movimiento[1])
            self.clear_possible_moves()

    # Establece la dificultad seleccionada
    def set_difficulty(self, difficulty):
        self.difficulty_level = difficulty

    # Dibuja un tablero completamente blanco con líneas de grid
    def draw_board(self):
        self.canvas.create_rectangle(
            0, 0, 
            self.canvas_size, self.canvas_size, 
            fill="white", outline="black"
        )
        
        # Dibujar líneas de la cuadrícula
        for i in range(self.board_size + 1):
            # Líneas verticales
            self.canvas.create_line(
                i * self.cell_size, 0,
                i * self.cell_size, self.canvas_size,
                fill="#e0e0e0"
            )
            # Líneas horizontales
            self.canvas.create_line(
                0, i * self.cell_size,
                self.canvas_size, i * self.cell_size,
                fill="#e0e0e0"
            )
        
        # Dibujar casillas pintadas
        for (row, col), color in self.painted_cells.items():
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            fill_color = "#a5d6a7" if color == "green" else "#ef9a9a"
            self.canvas.create_rectangle(
                x1, y1, x2, y2, 
                fill=fill_color, 
                outline="black"
            )
    
    # Marca las 4 zonas especiales en forma de L en las esquinas
    def mark_special_zones(self):
        for zone in self.special_zones.values():
            for row, col in zone:
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Solo dibujar el borde si la casilla no está pintada
                if (row, col) not in self.painted_cells:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, 
                        fill="#f5f5f5", 
                        outline="black",
                        width=3
                    )
    
    # Dibuja los Yoshis en sus posiciones actuales
    def draw_yoshis(self):
        # Dibujar Yoshi verde
        self.draw_knight(*self.green_yoshi_pos, "#2ecc71")  # Verde brillante
        
        # Dibujar Yoshi rojo
        self.draw_knight(*self.red_yoshi_pos, "#e74c3c")  # Rojo brillante
    
    # Dibuja un caballo en la posición dada
    def draw_knight(self, row, col, color):
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 3
        
        # Dibujar el caballo
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color, outline="black", width=2
        )
        
        # Añadir texto "Y" para representar al Yoshi
        self.canvas.create_text(
            x, y,
            text="Y",
            font=("Arial", 14, "bold"),
            fill="white"
        )
    
    # Calcula todos los posibles movimientos de caballo desde una posición
    def get_knight_moves(self, row, col):
        moves = []
        # Todos los posibles movimientos en L del caballo
        knight_moves = [
            (2, 1), (2, -1),
            (-2, 1), (-2, -1),
            (1, 2), (1, -2),
            (-1, 2), (-1, -2)
        ]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            # Verificar que el movimiento está dentro del tablero
            if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size:
                # Verificar que no hay un Yoshi en esa posición
                if (new_row, new_col) != self.green_yoshi_pos and (new_row, new_col) != self.red_yoshi_pos:
                    # Verificar que la casilla no está pintada
                    if (new_row, new_col) not in self.painted_cells:
                        moves.append((new_row, new_col))
        
        return moves
    
    # Muestra los posibles movimientos como círculos verdes
    def show_possible_moves(self, moves):
        self.clear_possible_moves()
        
        for row, col in moves:
            x = col * self.cell_size + self.cell_size // 2
            y = row * self.cell_size + self.cell_size // 2
            radius = self.cell_size // 6
            
            circle = self.canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill="#27ae60", outline="#27ae60", width=2
            )
            self.possible_moves.append((row, col, circle))
    
    # Elimina los marcadores de posibles movimientos
    def clear_possible_moves(self):
        for _, _, circle in self.possible_moves:
            self.canvas.delete(circle)
        self.possible_moves = []
    
    # Maneja el clic en una celda del tablero
    def on_cell_click(self, event):
        if self.game_over:
            return
            
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        # Determinar qué Yoshi está activo según el turno
        active_yoshi_pos = self.green_yoshi_pos if self.current_turn == "green" else self.red_yoshi_pos
        
        # Si se hace clic en el Yoshi activo, mostrar movimientos posibles
        if (row, col) == active_yoshi_pos:
            moves = self.get_knight_moves(row, col)
            self.show_possible_moves(moves)
        # Si se hace clic en un movimiento posible, mover el Yoshi
        elif any((row, col) == (r, c) for r, c, _ in self.possible_moves):
            self.move_yoshi(row, col)
        # Si se hace clic en cualquier otro lugar, limpiar movimientos posibles
        else:
            self.clear_possible_moves()
    
    # Mueve el Yoshi activo a la posición especificada
    def move_yoshi(self, row, col):
        # Limpiar movimientos posibles
        self.clear_possible_moves()
        
        # Actualizar posición del Yoshi activo
        if self.current_turn == "green":
            self.green_yoshi_pos = (row, col)
        else:
            self.red_yoshi_pos = (row, col)
        
        # Verificar si el movimiento fue a una zona especial
        self.check_special_zone(row, col)
        
        # Cambiar turno
        self.current_turn = "red" if self.current_turn == "green" else "green"
        self.update_turn_label()
        
        # Redibujar el tablero
        self.canvas.delete("all")
        self.draw_board()
        self.mark_special_zones()
        self.draw_yoshis()
        
        # Verificar si el juego ha terminado
        self.check_game_over()

        if not self.game_over and self.current_turn == "green":
            self.root.after(int(0.5 * 1000), self.movimiento_maquina)

    # Realiza el movimiento de la IA después del delay
    def movimiento_maquina(self):
        print("==================================")
        movimiento = MovimientoMaquina.MovimientoMaquina(
            self.special_zones,
            self.painted_cells, 
            self.green_yoshi_pos, 
            self.red_yoshi_pos,
            self.depth
        )
        print(str(movimiento) + "*************************************************")
        self.move_yoshi(movimiento[0], movimiento[1])
        self.clear_possible_moves()
    
    # Verifica si el movimiento fue a una zona especial y pinta la casilla si es necesario
    def check_special_zone(self, row, col):
        # Verificar todas las zonas especiales
        for zone_name, zone_cells in self.special_zones.items():
            if (row, col) in zone_cells and (row, col) not in self.painted_cells:
                # Pintar la casilla con el color del Yoshi actual
                self.painted_cells[(row, col)] = self.current_turn
                
                # Recalcular puntuación
                self.calculate_scores()
                self.update_score_label()
                break
    
    # Calcula la puntuación de cada jugador basada en las zonas controladas
    def calculate_scores(self):
        self.green_score = 0
        self.red_score = 0
        
        # Contar zonas controladas por cada jugador
        for zone_name, zone_cells in self.special_zones.items():
            green_count = 0
            red_count = 0
            
            for cell in zone_cells:
                if cell in self.painted_cells:
                    if self.painted_cells[cell] == "green":
                        green_count += 1
                    else:
                        red_count += 1
            
            # Asignar la zona al jugador con mayoría
            if green_count > red_count:
                self.green_score += 1
            elif red_count > green_count:
                self.red_score += 1
    
    # Verifica si todas las casillas especiales han sido pintadas
    def check_game_over(self):
        total_special_cells = sum(len(zone) for zone in self.special_zones.values())
        painted_special_cells = sum(1 for cell in self.painted_cells if any(cell in zone for zone in self.special_zones.values()))
        
        if painted_special_cells == total_special_cells:
            self.game_over = True
            self.show_game_result()
    
    # Muestra el resultado final del juego
    def show_game_result(self):
        winner = ""
        if self.green_score > self.red_score:
            winner = "¡Yoshi Verde gana!"
        elif self.red_score > self.green_score:
            winner = "¡Yoshi Rojo gana!"
        else:
            winner = "¡Empate!"
        
        message = f"Juego terminado!\n\nPuntuación final:\nYoshi Verde: {self.green_score}\nYoshi Rojo: {self.red_score}\n\n{winner}"
        messagebox.showinfo("Fin del juego", message)
    
    # Actualiza la etiqueta que muestra de quién es el turno
    def update_turn_label(self):
        if self.current_turn == "green":
            self.turn_label.config(text="Turno: Yoshi Verde", fg="#2ecc71")
        else:
            self.turn_label.config(text="Turno: Yoshi Rojo", fg="#e74c3c")
    
    def update_score_label(self):
        """Actualiza la etiqueta de puntuación"""
        self.score_label.config(text=f"Verde: {self.green_score} - Rojo: {self.red_score}")
    
    # Reinicia el juego a su estado inicial
    def reset_game(self):
    # Mostrar pantalla de inicio para seleccionar nueva dificultad
        self.start_screen = StartScreen(self.root, self.set_difficulty_and_reset)
        self.root.wait_window(self.start_screen.window)

    def set_difficulty_and_reset(self, difficulty):
        """Establece la dificultad y luego reinicia el juego"""
        self.difficulty_level = difficulty
        self.depth = {
            "Principiante": 2,
            "Amateur": 4,
            "Experto": 6
        }.get(self.difficulty_level, 4)  # Default a Amateur si hay algún problema
        
        # Resetear posiciones
        def posicion_aleatoria():
            x = random.randint(1,6)
            y = random.randint(1,6)
            return((x,y))
        
        self.green_yoshi_pos = posicion_aleatoria()
        self.red_yoshi_pos = posicion_aleatoria()
        while self.green_yoshi_pos == self.red_yoshi_pos:
            self.red_yoshi_pos = posicion_aleatoria()
        
        # Resetear turno
        self.current_turn = "green"
        
        # Resetear puntuación
        self.green_score = 0
        self.red_score = 0
        
        # Resetear casillas pintadas
        self.painted_cells = {}
        
        # Resetear estado del juego
        self.game_over = False
        
        # Actualizar interfaz
        self.difficulty_label.config(text=f"Dificultad: {self.difficulty_level}")
        self.update_turn_label()
        self.update_score_label()
        self.clear_possible_moves()
        self.canvas.delete("all")
        self.draw_board()
        self.mark_special_zones()
        self.draw_yoshis()
        
        if not self.game_over and self.current_turn == "green":
            self.root.after(int(0.5 * 1000), self.movimiento_maquina)

def main():
    root = tk.Tk()
    game = YoshiBoard(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()