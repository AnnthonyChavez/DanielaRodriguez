# segunda_parte/main_gui.py

import os
import django
import sys
from tkinter import Tk, Label, Button, Frame, Scrollbar, Listbox, messagebox
from tkinter import END, Entry, Text
from PIL import Image, ImageTk
import subprocess # Necesario para ejecutar test_image.py

# --- Configurar el entorno de Django ---
# La ruta base de tu proyecto (donde están manage.py y las carpetas primer_parte, segunda_parte)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Añade la carpeta raíz de tu proyecto al sys.path
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
    print(f"DEBUG: Añadido '{PROJECT_ROOT}' al sys.path.")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platos_ecuador_project.settings')

try:
    django.setup()
    print("DEBUG: Configuración de Django exitosa.")
except Exception as e:
    print(f"ERROR: Fallo al configurar Django: {e}")
    print(f"Asegúrate de que el módulo 'platos_ecuador_project.settings' es correcto y accesible.")
    sys.exit(1) 

from primer_parte.models import PlatoTipico
from django.conf import settings

# --- Función auxiliar para redimensionar imágenes de forma segura ---
def resize_image_for_tkinter(image_path, max_size=(300, 300)):
    try:
        print(f"DEBUG: Intentando cargar imagen desde: {image_path}")
        if not os.path.exists(image_path):
            print(f"DEBUG: El archivo de imagen NO existe en la ruta: {image_path}")
            messagebox.showerror("Error de Imagen", f"Archivo de imagen no encontrado:\n{image_path}")
            return None

        img = Image.open(image_path)
        img.thumbnail(max_size, Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        print(f"DEBUG: Imagen '{os.path.basename(image_path)}' cargada exitosamente por PIL.")
        return tk_img
    except FileNotFoundError:
        print(f"DEBUG ERROR: FileNotFoundError para: {image_path}")
        messagebox.showerror("Error de Imagen", f"Archivo de imagen no encontrado en la ruta:\n{image_path}")
        return None
    except Exception as e:
        print(f"DEBUG ERROR: Excepción al cargar imagen con Pillow: {e} para {image_path}")
        messagebox.showerror("Error de Imagen", f"No se pudo cargar o procesar la imagen:\n{image_path}\nError: {e}")
        return None

class PlatoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Administrador de Platos Típicos de Ecuador")
        master.geometry("800x600")
        master.configure(bg="#f0f0f0")

        # Lista para mantener las referencias de PhotoImage vivas.
        # Esto es la "solución radical" para la persistencia.
        self.all_tk_images_in_memory = [] 

        self.list_frame = Frame(master, bg="white", padx=10, pady=10, bd=2, relief="groove")
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.platos_list_label = Label(self.list_frame, text="Lista de Platos", font=("Arial", 16, "bold"), bg="white", fg="#333")
        self.platos_list_label.pack(pady=5)

        self.platos_listbox = Listbox(self.list_frame, width=80, height=15, font=("Arial", 10), bd=1, relief="solid", highlightbackground="#ccc", selectbackground="#cceeff")
        self.platos_listbox.pack(side="left", fill="both", expand=True, padx=(0,5))

        self.scrollbar = Scrollbar(self.list_frame, orient="vertical")
        self.scrollbar.config(command=self.platos_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.platos_listbox.config(yscrollcommand=self.scrollbar.set)

        self.button_frame = Frame(master, bg="#f0f0f0", pady=10)
        self.button_frame.pack(pady=5)

        self.add_button = Button(self.button_frame, text="Añadir Plato", command=self.open_add_window, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = Button(self.button_frame, text="Editar Plato", command=self.open_edit_window, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = Button(self.button_frame, text="Eliminar Plato", command=self.delete_plato, bg="#f44336", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.detail_button = Button(self.button_frame, text="Ver Detalles", command=self.open_detail_window, bg="#9C27B0", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.detail_button.grid(row=0, column=3, padx=5)

        self.refresh_button = Button(self.button_frame, text="Actualizar Lista", command=self.populate_list, bg="#FF9800", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.refresh_button.grid(row=0, column=4, padx=5)

        # NUEVO BOTÓN: Para ejecutar test_image.py
        self.test_image_button = Button(self.button_frame, text="Probar Imagen", command=self.run_test_image_script, bg="#607D8B", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.test_image_button.grid(row=0, column=5, padx=5)


        self.populate_list()

    def populate_list(self):
        self.platos_listbox.delete(0, END)
        try:
            self.all_platos = list(PlatoTipico.objects.all().order_by('nombre'))
            if not self.all_platos:
                self.platos_listbox.insert(END, "No hay platos registrados. ¡Añade uno!")
            for i, plato in enumerate(self.all_platos):
                self.platos_listbox.insert(END, f"{plato.nombre} - Región: {plato.region or 'N/A'}")
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo cargar los platos: {e}")

    def get_selected_plato(self):
        try:
            index = self.platos_listbox.curselection()[0]
            return self.all_platos[index]
        except IndexError:
            messagebox.showwarning("Selección", "Por favor, selecciona un plato de la lista.")
            return None
        except Exception as e:
            messagebox.showerror("Error de Selección", f"Error al obtener el plato: {e}")
            return None

    def open_add_window(self):
        add_window = Tk()
        add_window.title("Añadir Nuevo Plato")
        add_window.geometry("400x450")
        add_window.configure(bg="#f9f9f9")

        Label(add_window, text="Nombre:", bg="#f9f9f9").pack(pady=5)
        nombre_entry = Entry(add_window, width=40)
        nombre_entry.pack(pady=5)

        Label(add_window, text="Descripción:", bg="#f9f9f9").pack(pady=5)
        descripcion_entry = Text(add_window, width=30, height=5)
        descripcion_entry.pack(pady=5)

        Label(add_window, text="Región:", bg="#f9f9f9").pack(pady=5)
        region_entry = Entry(add_window, width=40)
        region_entry.pack(pady=5)

        Label(add_window, text="Ingredientes Principales:", bg="#f9f9f9").pack(pady=5)
        ingredientes_entry = Text(add_window, width=30, height=4)
        ingredientes_entry.pack(pady=5)

        def save_plato():
            try:
                nombre = nombre_entry.get()
                descripcion = descripcion_entry.get("1.0", END).strip()
                region = region_entry.get()
                ingredientes = ingredientes_entry.get("1.0", END).strip()

                if not nombre or not descripcion or not ingredientes:
                    messagebox.showwarning("Campos Vacíos", "Nombre, Descripción e Ingredientes son obligatorios.")
                    return

                PlatoTipico.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    region=region,
                    ingredientes_principales=ingredientes
                )
                messagebox.showinfo("Éxito", "Plato añadido correctamente.")
                add_window.destroy()
                self.populate_list()
            except Exception as e:
                messagebox.showerror("Error al Guardar", f"No se pudo añadir el plato: {e}")

        Button(add_window, text="Guardar Plato", command=save_plato, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).pack(pady=15)

    def open_edit_window(self):
        selected_plato = self.get_selected_plato()
        if not selected_plato:
            return

        edit_window = Tk()
        edit_window.title(f"Editar Plato: {selected_plato.nombre}")
        edit_window.geometry("400x450")
        edit_window.configure(bg="#f9f9f9")

        Label(edit_window, text="Nombre:", bg="#f9f9f9").pack(pady=5)
        nombre_entry = Entry(edit_window, width=40)
        nombre_entry.insert(0, selected_plato.nombre)
        nombre_entry.pack(pady=5)

        Label(edit_window, text="Descripción:", bg="#f9f9f9").pack(pady=5)
        descripcion_entry = Text(edit_window, width=30, height=5)
        descripcion_entry.insert("1.0", selected_plato.descripcion)
        descripcion_entry.pack(pady=5)

        Label(edit_window, text="Región:", bg="#f9f9f9").pack(pady=5)
        region_entry = Entry(edit_window, width=40)
        region_entry.insert(0, selected_plato.region or "")
        region_entry.pack(pady=5)

        Label(edit_window, text="Ingredientes Principales:", bg="#f9f9f9").pack(pady=5)
        ingredientes_entry = Text(edit_window, width=30, height=4)
        ingredientes_entry.insert("1.0", selected_plato.ingredientes_principales)
        ingredientes_entry.pack(pady=5)

        def update_plato():
            try:
                selected_plato.nombre = nombre_entry.get()
                selected_plato.descripcion = descripcion_entry.get("1.0", END).strip()
                selected_plato.region = region_entry.get()
                selected_plato.ingredientes_principales = ingredientes_entry.get("1.0", END).strip()

                if not selected_plato.nombre or not selected_plato.descripcion or not selected_plato.ingredientes_principales:
                    messagebox.showwarning("Campos Vacíos", "Nombre, Descripción e Ingredientes son obligatorios.")
                    return

                selected_plato.save()
                messagebox.showinfo("Éxito", "Plato actualizado correctamente.")
                edit_window.destroy()
                self.populate_list()
            except Exception as e:
                messagebox.showerror("Error al Actualizar", f"No se pudo actualizar el plato: {e}")

        Button(edit_window, text="Actualizar Plato", command=update_plato, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5).pack(pady=15)

    def delete_plato(self):
        selected_plato = self.get_selected_plato()
        if not selected_plato:
            return

        if messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que quieres eliminar '{selected_plato.nombre}'?"):
            try:
                selected_plato.delete()
                messagebox.showinfo("Éxito", "Plato eliminado correctamente.")
                self.populate_list()
            except Exception as e:
                messagebox.showerror("Error al Eliminar", f"No se pudo eliminar el plato: {e}")

    def open_detail_window(self):
        selected_plato = self.get_selected_plato()
        if not selected_plato:
            return

        detail_window = Tk()
        detail_window.title(f"Detalles de {selected_plato.nombre}")
        detail_window.geometry("500x700")
        detail_window.configure(bg="#f9f9f9")

        Label(detail_window, text=selected_plato.nombre, font=("Arial", 18, "bold"), bg="#f9f9f9", fg="#0056b3").pack(pady=10)
        Label(detail_window, text=f"Región: {selected_plato.region or 'N/A'}", font=("Arial", 12), bg="#f9f9f9").pack(pady=2)

        Label(detail_window, text="Ingredientes Principales:", font=("Arial", 12, "bold"), bg="#f9f9f9").pack(pady=(10, 0))
        ingredientes_text = Text(detail_window, width=50, height=5, font=("Arial", 10), wrap="word", bd=1, relief="solid")
        ingredientes_text.insert(END, selected_plato.ingredientes_principales)
        ingredientes_text.config(state="disabled")
        ingredientes_text.pack(pady=5)

        Label(detail_window, text="Descripción:", font=("Arial", 12, "bold"), bg="#f9f9f9").pack(pady=(10, 0))
        desc_text = Text(detail_window, width=50, height=10, font=("Arial", 10), wrap="word", bd=1, relief="solid")
        desc_text.insert(END, selected_plato.descripcion)
        desc_text.config(state="disabled")
        desc_text.pack(pady=5)

        # Imagen
        if selected_plato.imagen:
            image_path = os.path.join(settings.MEDIA_ROOT, selected_plato.imagen.name)
            tk_img_display = resize_image_for_tkinter(image_path, max_size=(300, 300))
            
            if tk_img_display:
                img_label = Label(detail_window, image=tk_img_display, bg="#f9f9f9")
                img_label.pack(pady=10)
                
                # ¡La estrategia de persistencia más robusta!
                # Almacena la referencia en la lista de la instancia principal de la GUI.
                self.all_tk_images_in_memory.append(tk_img_display)
                
                # Para mayor seguridad, también adjúntala a la ventana de detalle (aunque la lista global es lo principal)
                detail_window.tk_img_ref = tk_img_display
                
            else:
                Label(detail_window, text="Error: No se pudo mostrar la imagen.", fg="red", bg="#f9f9f9").pack(pady=5)
        else:
            Label(detail_window, text="No hay imagen disponible para este plato.", bg="#f9f9f9").pack(pady=5)

        Button(detail_window, text="Cerrar", command=detail_window.destroy, bg="#ccc", fg="#333", font=("Arial", 10, "bold"), padx=10, pady=5).pack(pady=15)

    def run_test_image_script(self):
        # Obtener la ruta al script test_image.py
        test_script_path = os.path.join(os.path.dirname(__file__), 'test_image.py')
        
        # Obtener la ruta al ejecutable de Python del entorno virtual
        python_exe = sys.executable 

        if not os.path.exists(test_script_path):
            messagebox.showerror("Error", f"El script 'test_image.py' no se encontró en:\n{test_script_path}")
            return

        try:
            # Versión SIMPLIFICADA de subprocess.Popen para evitar WinError 87
            # Esto simplemente ejecuta el script Python. Puede que se abra en la misma consola
            # o en una nueva dependiendo de la configuración del sistema.
            subprocess.Popen([python_exe, test_script_path])
            
            messagebox.showinfo("Lanzamiento", "Intentando abrir la ventana de prueba de imagen.")

        except Exception as e:
            messagebox.showerror("Error al Abrir", f"No se pudo ejecutar test_image.py: {e}")



if __name__ == "__main__":
    root = Tk()
    gui = PlatoGUI(root)
    root.mainloop()