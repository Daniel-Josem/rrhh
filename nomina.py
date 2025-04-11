import tkinter as tk

def nominas():
    ventana = tk.Tk()
    ventana.title("Nómina")
    ventana.attributes('-fullscreen', True)
    ventana.config(bg="#d9d9d9")

    tk.Label(ventana, text="Lista de Productos", font=("calibri", 18, "bold"), bg="black", fg="white").pack(pady=10)
    
    tk.Button(ventana, text="Cerrar", font=("Arial", 16), bg="#a41e34", fg="white", width=20,
              command=ventana.destroy).pack(pady=20)

    ventana.mainloop()  
