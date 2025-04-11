import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import subprocess

# Colores iguales al admin
color_recuadro = "#f2f2f2"
color_boton = "#a41e34"
color_texto = "#ffffff"

def ventana_usuario_rrhh():
    global ventana, entry_usuario, entry_contraseña

    ventana = tk.Tk()
    ventana.title("Login Usuarios RRHH")
    ventana.attributes('-fullscreen', True)

    # Fondo
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    try:
        fondo = Image.open("image/fondo.jpg")
        fondo = fondo.resize((screen_width, screen_height), Image.LANCZOS)
        fondo_img = ImageTk.PhotoImage(fondo)
        fondo_label = tk.Label(ventana, image=fondo_img)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
        ventana.fondo_img = fondo_img
    except Exception as e:
        print("Error al cargar fondo:", e)

    frame_contenido = tk.Frame(ventana, bg="", highlightthickness=0)
    frame_contenido.pack(expand=True)

    # Logo
    try:
        logo = Image.open("image/logo.jpg")
        logo = logo.resize((150, 150), Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo)
        tk.Label(frame_contenido, image=logo_img, bg="", bd=0).pack(pady=(20, 10))
        ventana.logo_img = logo_img
    except Exception as e:
        print("Error al cargar logo:", e)

    # Recuadro de login
    frame_login = tk.Frame(frame_contenido, bg=color_recuadro, width=400, height=450)
    frame_login.pack()
    frame_login.pack_propagate(False)

    contenido = tk.Frame(frame_login, bg=color_recuadro)
    contenido.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(contenido, text="Login RRHH", font=("Arial", 20, "bold"),
             bg=color_recuadro, fg=color_boton).pack(pady=(0, 20))

    tk.Label(contenido, text="Usuario:", bg=color_recuadro, fg=color_boton, font=("Arial", 14)).pack()
    entry_usuario = tk.Entry(contenido, font=("Arial", 12), width=30)
    entry_usuario.pack(pady=10)

    tk.Label(contenido, text="Contraseña:", bg=color_recuadro, fg=color_boton, font=("Arial", 14)).pack()
    entry_contraseña = tk.Entry(contenido, show="*", font=("Arial", 12), width=30)
    entry_contraseña.pack(pady=10)

    tk.Button(contenido, text="Ingresar", bg=color_boton, fg=color_texto,
              font=("Arial", 12), width=20, command=verificar_login_rrhh).pack(pady=20)

    # Botón salir
    tk.Button(ventana, text="Salir", bg="#555", fg="white", font=("Arial", 10),
              command=ventana.destroy).place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)

    ventana.mainloop()

def verificar_login_rrhh():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()

    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rrhh"
        )

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuario_rrhh WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
        resultado = cursor.fetchone()

        if resultado:
            ventana.destroy()
            subprocess.Popen(["python", "usuario_panel.py"], shell=True)
        else:
            messagebox.showerror("Acceso", "Usuario o contraseña incorrectos")

        cursor.close()
        conexion.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al conectar con la base de datos:\n{err}")
