import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mariadb
from Ventana_Animal import Ventana_Animales
from Ventana_Predio import Ventana_Predios
import sys

APP_TITLE = 'GANA_CONTROL'
WINDOW_SIZE = "900x600"
BG = "#f4f3ec"
ACCENT = "#36448B"
ACCENT_DARK = "#2A3E75"
TEXT_COLOR = "#222"

# -------------------------------
# Conexión a la base de datos
# -------------------------------
def conectar_bd():
    try:
        conn = mariadb.connect(
            host='localhost',
            user='AdminGanaderia',
            password='2025',
            database='Proyecto_Ganaderia'
        )
        cursor = conn.cursor()
        print("Conexión exitosa a la base de datos.")
        return conn, cursor
    except mariadb.Error as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar:\n{e}")
        return None, None


# -------------------------------
# Clase principal del sistema BD
# -------------------------------
class APP_BD(tk.Tk):
    def __init__(self, usuario, rol):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.config(bg=BG)

        self.usuario = usuario
        self.rol = rol
        self.menu_open = False

        self.create_banner()
        self.menu_widgets()
        self.tramites_botones()

    def create_banner(self):
        banner_frame = tk.Frame(self, bg=ACCENT)
        banner_frame.pack(fill="x")

        tk.Label(
            banner_frame,
            text=f"🐮 Bienvenido {self.usuario} ({self.rol})",
            font=("Arial", 14, "bold"),
            bg=ACCENT,
            fg="white"
        ).pack(pady=10)

        try:
            img = Image.open("banner.png")
            img = img.resize((900, 180))
            self.banner_img = ImageTk.PhotoImage(img)
            tk.Label(banner_frame, image=self.banner_img, bg=ACCENT).pack(fill="x")
        except Exception:
            tk.Label(
                banner_frame,
                text="🐄 Bienvenido a GANA_CONTROL",
                font=("Arial", 20, "bold"),
                bg=ACCENT,
                fg="white",
                height=3
            ).pack(fill="x")

    def menu_widgets(self):
        self.side_panel_frame = tk.Frame(self, bg="#916D4C", width=60)
        self.side_panel_frame.pack(side="left", fill="y")

        self.menu_button = tk.Button(
            self.side_panel_frame,
            text="≡",
            bg="#916D4C",
            command=self.toggle_menu
        )
        self.menu_button.pack(side="top", pady=10)

        self.menu_buttons = []
        opciones = {
            "Animales": self.abrir_ventana_animales,
            "Predios": self.abrir_ventana_predio,
            "Productor": lambda: messagebox.showinfo("Info", "Ventana Productor aún no implementada"),
            "Pesaje": lambda: messagebox.showinfo("Info", "Ventana Pesaje aún no implementada"),
            "Registro": lambda: messagebox.showinfo("Info", "Ventana Registro aún no implementada")
        }

        for texto, comando in opciones.items():
            boton = tk.Button(
                self.side_panel_frame,
                text=texto,
                bg="white",
                relief="flat",
                command=comando
            )
            self.menu_buttons.append(boton)

    def toggle_menu(self):
        if not self.menu_open:
            for boton in self.menu_buttons:
                boton.pack(side="top", fill="x", pady=5, padx=5)
            self.menu_open = True
            self.menu_button.config(text="x")
        else:
            for boton in self.menu_buttons:
                boton.pack_forget()
            self.menu_open = False
            self.menu_button.config(text="≡")

    def tramites_botones(self):
        frame_central = tk.Frame(self, bg=BG)
        frame_central.pack(expand=True,fill="both")
        titulo = tk.Label(frame_central,
                           text="tramites", 
                           font=("Arial",28, "bold"),
                           bg=BG,
                           fg=ACCENT
                           ).pack(pady=2)

        botones_frame = tk.Frame(frame_central, bg=BG)
        botones_frame.pack(pady=20)

        botones = [
            ("Tramite 1", lambda:messagebox.showinfo("tramite", "Inice nuevo")),
            ("Tramite 2", lambda:messagebox.showinfo("tramite", "Inice nuevo")),
            ("Tramite 3", lambda:messagebox.showinfo("tramite", "Inice nuevo"))
        ]
        for texto, comando in botones:
            botones = tk.Button(
                botones_frame,
                text=texto,
                font=("Arial", 14, "bold"),
                bg=ACCENT,
                width=20, 
                height= 2, 
                relief="flat",
                command=comando
            )
            botones.pack(pady=10)

 
    def abrir_ventana_animales(self):
        ventana_animales = Ventana_Animales(self)
        ventana_animales.grab_set()

    def abrir_ventana_predio(self):
        ventana_predio = Ventana_Predios(self)
        ventana_predio.grab_set()


# -------------------------------
# Programa principal
# -------------------------------
if __name__ == "__main__":
    usuario = sys.argv[1] if len(sys.argv) > 1 else "Desconocido"
    rol = sys.argv[2] if len(sys.argv) > 2 else "Sin rol"
    print(f"Inició sesión: {usuario} ({rol})")

    app = APP_BD(usuario, rol)
    app.mainloop()
