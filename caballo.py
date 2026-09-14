import tkinter as tk
from tkinter import ttk
import threading
import random
import time
from pathlib import Path

class CarreraDeCaballos:
    def __init__(self, root):
        self.root = root
        self.root.title("Carrera de Caballos")
        self.root.geometry("600x500")
        
        self.ganador = -1
        self.lock = threading.Lock()
        self.threads = []
        self.progreso = [0, 0, 0, 0]
        self.numero_carrera = 0
        self.alerta_ganador = None
        
        #intertfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crear la interfaz gráfica"""

        self.root.configure(bg="#dff3e4")

        # Título
        titulo = tk.Label(self.root, text="CARRERA DE CABALLOS", 
                         font=("Arial", 15, "bold"))
        titulo.pack(pady=10)
        
        # Frame para los progressbars
        self.frame_caballos = tk.Frame(
            self.root,
            bg="#ba68c8"
        )
        self.frame_caballos.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Crear 4 caballos con sus progressbars
        self.labels = []
        self.progressbars = []
        self.labels_porcentaje = []
        
        for i in range(4):
            # Etiqueta del caballo
            label = tk.Label(self.frame_caballos, text=f"Caballo {i+1}", 
                           font=("Tahona", 10, "bold"))
            label.pack(pady=5)
            self.labels.append(label)
            
            # barra de progreso
            pbar = ttk.Progressbar(self.frame_caballos, length=400, mode='determinate',
                                  maximum=100)
            pbar.pack(pady=5)
            self.progressbars.append(pbar)
            
            # porcentaje
            label_pct = tk.Label(self.frame_caballos, text="0%", 
                               font=("Tahona", 9))
            label_pct.pack()
            self.labels_porcentaje.append(label_pct)
        
        # Botón de inicio
        self.btn_iniciar = tk.Button(self.root, text="Iniciar Carrera",
                                     command=self.iniciar_carrera,
                                     font=("Tahona", 12, "bold"),
                                     bg="purple", fg="white",
                                     padx=20, pady=10)
        self.btn_iniciar.pack(pady=10)
        
    def mostrar_alerta_ganador(self, mensaje):
        """Muestra el resultado en una ventana emergente."""
        self.alerta_ganador = tk.Toplevel(self.root)
        self.alerta_ganador.title("Resultado de la carrera")
        self.alerta_ganador.geometry("380x180")
        self.alerta_ganador.resizable(False, False)
        self.alerta_ganador.transient(self.root)
        self.alerta_ganador.grab_set()

        marco = tk.Frame(
            self.alerta_ganador,
            bg="#ba68c8",
            highlightbackground="#ba68c8",
            highlightthickness=3,
            padx=18,
            pady=12
        )
        marco.pack(padx=18, pady=15, fill="both", expand=True)

        tk.Label(
            marco,
            text=mensaje,
            font=("Verdana", 13, "bold"),
            fg="#8b1e1e",
            bg="#ba68c8",
            justify="center"
        ).pack(pady=(0, 12))

        botones = tk.Frame(marco, bg="#ba68c8")
        botones.pack()
        tk.Button(
            botones,
            text="OK",
            command=self.cerrar_alerta,
            width=10
        ).pack(side="left", padx=8)
        tk.Button(
            botones,
            text="Reiniciar ",
            command=self.volver_a_iniciar,
            width=10
        ).pack(side="left", padx=8)

    def cerrar_alerta(self):
        """Cierra la alerta y conserva el estado actual de la carrera."""
        if self.alerta_ganador is not None and self.alerta_ganador.winfo_exists():
            self.alerta_ganador.grab_release()
            self.alerta_ganador.destroy()
        self.alerta_ganador = None

    def volver_a_iniciar(self):
        """Cierra la alerta y comienza una carrera completamente nueva."""
        self.cerrar_alerta()
        self.iniciar_carrera()

    def iniciar_carrera(self):
        """Inicia la carrera cuando se presiona el botón"""
        
        # Reset
        self.numero_carrera += 1
        numero_carrera = self.numero_carrera
        self.ganador = -1
        self.progreso = [0, 0, 0, 0]
        
        # Deshabilitar botón
        self.btn_iniciar.config(state="disabled")
        
        # Resetear progressbars
        for pbar in self.progressbars:
            pbar['value'] = 0
        
        for label_pct in self.labels_porcentaje:
            label_pct.config(text="0%")
        
        # Crear threads para cada caballo
        self.threads = []
        for i in range(4):
            thread = threading.Thread(
                target=self.avanzar_caballo,
                args=(i, numero_carrera)
            )
            thread.start()
            self.threads.append(thread)
    
    def avanzar_caballo(self, indice, numero_carrera):
        """Simula el avance de un caballo (ejecutado en thread)"""
        
        progreso = 0
        
        while progreso < 100:
            if numero_carrera != self.numero_carrera:
                return

            # Incremento aleatorio entre 1 y 15
            progreso += random.randint(1, 15)
            
            # No exceder 100
            if progreso > 100:
                progreso = 100
            
            # Guardar progreso
            self.progreso[indice] = progreso
            
            # Actualizar UI
            self.actualizar_progressbar(indice, progreso)
            
            # Pausa para simular la carrera
            time.sleep(0.5)
        
        # El caballo llegó a 100
        with self.lock:
            if numero_carrera == self.numero_carrera and self.ganador == -1:
                self.ganador = indice
                mensaje = f" ¡Caballo {indice + 1} ganó la carrera! 🏆"
                self.root.after(0, self.mostrar_alerta_ganador, mensaje)
        
        # Habilitar botón cuando termine
        if numero_carrera == self.numero_carrera and all(
            self.progreso[i] == 100 for i in range(4)
        ):
            self.root.after(0, lambda: self.btn_iniciar.config(state="normal"))
    
    def actualizar_progressbar(self, indice, valor):
        """Actualiza el progressbar en el thread principal"""
        
        self.progressbars[indice]['value'] = valor
        self.labels_porcentaje[indice].config(text=f"{valor}%")
        self.root.update_idletasks()

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = CarreraDeCaballos(root)
    root.mainloop()