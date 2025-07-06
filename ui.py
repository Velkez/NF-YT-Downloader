import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from logic import ejecutar_descarga
import threading

def seleccionar_carpeta(carpeta_var):
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta de destino")
    if carpeta:
        carpeta_var.set(carpeta)

def iniciar_descarga(url_var, carpeta_var, root, consola):
    url = url_var.get().strip()
    carpeta = carpeta_var.get().strip()
    if not url:
        messagebox.showerror("Error", "Por favor ingresa la URL del canal o playlist.")
        return
    if not carpeta:
        messagebox.showerror("Error", "Por favor selecciona la carpeta de destino.")
        return
    global download_folder
    download_folder = carpeta
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    root.after(100, lambda: root.iconify())
    try:
        consola.config(state='normal')
        consola.delete(1.0, tk.END)
        consola.insert(tk.END, "Preparando descarga...\n")
        consola.config(state='disabled')
        root.update_idletasks()
        def descarga_y_mensaje():
            ejecutar_descarga(url, download_folder, root)
            consola.config(state='normal')
            consola.insert(tk.END, "Descarga completada.\n")
            consola.config(state='disabled')
            messagebox.showinfo("Completado", f"Descarga completada.\nLas canciones se han guardado en: {download_folder}")
        hilo = threading.Thread(target=descarga_y_mensaje, daemon=True)
        hilo.start()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
    root.after(100, lambda: root.deiconify())


def main():
    root = tk.Tk()
    root.title("Descargador de Música de YouTube")
    root.geometry("600x400")
    root.resizable(False, False)

    tk.Label(root, text="URL del canal o playlist de YouTube:").pack(pady=(18, 2))
    url_var = tk.StringVar()
    tk.Entry(root, textvariable=url_var, width=60).pack(pady=2)

    tk.Label(root, text="Carpeta de destino:").pack(pady=(10, 2))
    carpeta_var = tk.StringVar(value=os.path.abspath("Canciones-yt"))
    frame_carpeta = tk.Frame(root)
    frame_carpeta.pack()
    tk.Entry(frame_carpeta, textvariable=carpeta_var, width=45).pack(side=tk.LEFT, padx=2)
    tk.Button(frame_carpeta, text="Seleccionar...", command=lambda: seleccionar_carpeta(carpeta_var)).pack(side=tk.LEFT, padx=2)


    # Consola de logs
    consola = tk.Text(root, height=12, width=75, state='disabled', bg='#222', fg='#0f0', font=('Consolas', 10))
    consola.pack(pady=(10, 0))
    # Hacemos accesible la consola desde root para logic.py
    root.consola_widget = consola

    tk.Button(root, text="Descargar música", command=lambda: iniciar_descarga(url_var, carpeta_var, root, consola), bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=18)

    root.mainloop()

if __name__ == "__main__":
    main()
