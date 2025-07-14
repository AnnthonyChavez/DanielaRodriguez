import tkinter as tk
from PIL import Image, ImageTk
import os

# La ruta exacta a tu imagen de "Caldo de gallina"
# Asegúrate de que esta ruta sea correcta y que la imagen exista
# Esta ruta debe ser absoluta para que funcione independientemente de dónde se llame el script.
# Adaptar si tu imagen no es Caldo_de_gallina.jpg
# La parte '..\media\platos' asume que test_image.py está en 'segunda_parte'
# y el proyecto raíz 'Deber' contiene 'media'.
current_dir = os.path.dirname(__file__)
project_root_dir = os.path.abspath(os.path.join(current_dir, '..'))
IMAGE_PATH = os.path.join(project_root_dir, r"media\platos\Caldo_de_gallina.jpg") # Usa r"" para rutas de Windows


def load_and_display_image():
    root = tk.Tk()
    root.title("Prueba de Imagen (test_image.py)")

    try:
        if not os.path.exists(IMAGE_PATH):
            print(f"ERROR: Archivo no encontrado en {IMAGE_PATH}")
            tk.messagebox.showerror("Error", f"Archivo de imagen no encontrado:\n{IMAGE_PATH}")
            root.destroy() # Cierra la ventana si no se encuentra el archivo
            return

        # Cargar la imagen con PIL
        pil_image = Image.open(IMAGE_PATH)
        
        # Redimensionar la imagen si es demasiado grande para la pantalla
        max_size = (400, 400)
        pil_image.thumbnail(max_size, Image.LANCZOS)
        
        # Convertir a formato PhotoImage para Tkinter
        tk_image = ImageTk.PhotoImage(pil_image)
        
        # Crear un Label para mostrar la imagen
        image_label = tk.Label(root, image=tk_image)
        image_label.pack(padx=20, pady=20)
        
        # Esto es CRUCIAL: Mantener una referencia a la imagen para evitar que el recolector de basura la elimine
        image_label.image = tk_image 
        root.tk_image_ref = tk_image # También una referencia en la ventana principal (por redundancia)
        
        print(f"DEBUG (test_image.py): Imagen '{os.path.basename(IMAGE_PATH)}' cargada y referenciada.")

    except Exception as e:
        print(f"ERROR (test_image.py): Fallo al cargar o mostrar la imagen: {e}")
        tk.messagebox.showerror("Error de Imagen", f"No se pudo cargar o mostrar la imagen:\n{e}")
        root.destroy() # Cierra la ventana si hay un error
        return

    root.mainloop()

if __name__ == "__main__":
    load_and_display_image()