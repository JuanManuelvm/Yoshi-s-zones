import tkinter as tk
from tkinter import ttk

class YoshiBoard:
    def __init__(self, root):
        self.root = root
        self.root.title("Yoshi's Zones")
        
        # Configuración del tablero
        self.board_size = 8
        self.cell_size = 60
        self.canvas_size = self.board_size * self.cell_size
        
        # Posiciones iniciales de los Yoshis
        self.green_yoshi_pos = (3, 3)
        self.red_yoshi_pos = (4, 4)
        
        # Crear frame superior para el combobox
        self.top_frame = tk.Frame(root)
        self.top_frame.pack(pady=10)
        
        # Lista desplegable de dificultad
        self.difficulty_label = tk.Label(self.top_frame, text="Dificultad:")
        self.difficulty_label.pack(side=tk.LEFT, padx=5)
        
        self.difficulty = ttk.Combobox(
            self.top_frame, 
            values=["Principiante", "Normal", "Avanzado"],
            state="readonly"
        )
        self.difficulty.current(1)  # Selecciona "Normal" por defecto
        self.difficulty.pack(side=tk.LEFT)
        
        # Crear canvas
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.pack()
        
        # Dibujar elementos
        self.draw_board()
        self.mark_special_zones()
        self.draw_yoshis()
    
    def draw_board(self):
        """Dibuja un tablero completamente blanco con líneas de grid"""
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
                fill="#e0e0e0"  # Gris claro para las líneas de grid
            )
            # Líneas horizontales
            self.canvas.create_line(
                0, i * self.cell_size,
                self.canvas_size, i * self.cell_size,
                fill="#e0e0e0"
            )
    
    def mark_special_zones(self):
        """Marca las 4 zonas especiales en forma de L en las esquinas"""
        # Coordenadas de las esquinas
        corners = [
            (0, 0),                     # Esquina superior izquierda
            (0, self.board_size - 1),    # Esquina superior derecha
            (self.board_size - 1, 0),    # Esquina inferior izquierda
            (self.board_size - 1, self.board_size - 1)  # Esquina inferior derecha
        ]
        
        for corner_row, corner_col in corners:
            # Determinar la orientación de la L basada en la esquina
            if corner_row == 0 and corner_col == 0:  # Superior izquierda
                cells = [(0,0), (0,1), (0,2), (1,0), (2,0)]
            elif corner_row == 0 and corner_col == self.board_size - 1:  # Superior derecha
                cells = [(0,7), (0,6), (0,5), (1,7), (2,7)]
            elif corner_row == self.board_size - 1 and corner_col == 0:  # Inferior izquierda
                cells = [(7,0), (7,1), (7,2), (6,0), (5,0)]
            else:  # Inferior derecha
                cells = [(7,7), (7,6), (7,5), (6,7), (5,7)]
            
            for row, col in cells:
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Dibujar zona especial con borde negro
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill="#f5f5f5",  # Gris muy claro
                    outline="black",  # Borde negro
                    width=3  # Borde grueso
                )
    
    def draw_yoshis(self):
        """Dibuja los Yoshis en sus posiciones iniciales"""
        # Dibujar Yoshi verde
        self.draw_knight(*self.green_yoshi_pos, "#2ecc71")  # Verde brillante
        
        # Dibujar Yoshi rojo
        self.draw_knight(*self.red_yoshi_pos, "#e74c3c")  # Rojo brillante
    
    def draw_knight(self, row, col, color):
        """Dibuja un caballo en la posición dada"""
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

def main():
    root = tk.Tk()
    game = YoshiBoard(root)
    root.mainloop()

if __name__ == "__main__":
    main()