# segunda_parte/main_gui.py

import os
import django
import sys
from tkinter import Tk, Label, Button, Frame, Scrollbar, Listbox, messagebox
from tkinter import END, Entry # Importar Entry para campos de texto

# Configurar el entorno de Django
# Asegúrate de que 'platos_ecuador_project' es el nombre de tu carpeta de proyecto Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'platos_ecuador_project.settings')
django.setup()

# Importar el modelo de Django después de la configuración del entorno
from primer_parte.models import PlatoTipico

class PlatoGUI:
    def __init__(self, master):
        self.master = master
        master.title("Administrador de Platos Típicos de Ecuador")

        # Estilos básicos
        master.geometry("800x600")
        master.configure(bg="#f0f0f0")

        # Frame para el listado de platos
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

        # Frame para botones de acción
        self.button_frame = Frame(master, bg="#f0f0f0", pady=10)
        self.button_frame.pack(pady=5)

        self.add_button = Button(self.button_frame, text="Añadir Plato", command=self.open_add_window, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.add_button.grid(row=0, column=0, padx=5)

        self.edit_button = Button(self.button_frame, text="Editar Plato", command=self.open_edit_window, bg="#2196F3", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.edit_button.grid(row=0, column=1, padx=5)

        self.delete_button = Button(self.button_frame, text="Eliminar Plato", command=self.delete_plato, bg="#f44336", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.refresh_button = Button(self.button_frame, text="Actualizar Lista", command=self.populate_list, bg="#FF9800", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5)
        self.refresh_button.grid(row=0, column=3, padx=5)

        # Cargar la lista inicial de platos
        self.populate_list()

    def populate_list(self):
        self.platos_listbox.delete(0, END)
        try:
            platos = PlatoTipico.objects.all().order_by('nombre')
            if not platos:
                self.platos_listbox.insert(END, "No hay platos registrados. ¡Añade uno!")
            for plato in platos:
                self.platos_listbox.insert(END, f"{plato.nombre} - Región: {plato.region or 'N/A'}")
        except Exception as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo cargar los platos: {e}")

    def get_selected_plato(self):
        try:
            index = self.platos_listbox.curselection()[0]
            selected_plato_text = self.platos_listbox.get(index)
            # Extraer el nombre del plato del texto mostrado
            plato_name = selected_plato_text.split(" - Región:")[0]
            return PlatoTipico.objects.get(nombre=plato_name)
        except IndexError:
            messagebox.showwarning("Selección", "Por favor, selecciona un plato de la lista.")
            return None
        except PlatoTipico.DoesNotExist:
            messagebox.showerror("Error", "El plato seleccionado no existe en la base de datos.")
            return None
        except Exception as e:
            messagebox.showerror("Error de Selección", f"Error al obtener el plato: {e}")
            return None


    def open_add_window(self):
        add_window = Tk()
        add_window.title("Añadir Nuevo Plato")
        add_window.geometry("400x350")
        add_window.configure(bg="#f9f9f9")

        Label(add_window, text="Nombre:", bg="#f9f9f9").pack(pady=5)
        nombre_entry = Entry(add_window, width=40)
        nombre_entry.pack(pady=5)

        Label(add_window, text="Descripción:", bg="#f9f9f9").pack(pady=5)
        descripcion_entry = Entry(add_window, width=40)
        descripcion_entry.pack(pady=5)

        Label(add_window, text="Región:", bg="#f9f9f9").pack(pady=5)
        region_entry = Entry(add_window, width=40)
        region_entry.pack(pady=5)

        Label(add_window, text="Ingredientes Principales:", bg="#f9f9f9").pack(pady=5)
        ingredientes_entry = Entry(add_window, width=40)
        ingredientes_entry.pack(pady=5)

        def save_plato():
            try:
                nombre = nombre_entry.get()
                descripcion = descripcion_entry.get()
                region = region_entry.get()
                ingredientes = ingredientes_entry.get()

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
        edit_window.geometry("400x350")
        edit_window.configure(bg="#f9f9f9")

        Label(edit_window, text="Nombre:", bg="#f9f9f9").pack(pady=5)
        nombre_entry = Entry(edit_window, width=40)
        nombre_entry.insert(0, selected_plato.nombre)
        nombre_entry.pack(pady=5)

        Label(edit_window, text="Descripción:", bg="#f9f9f9").pack(pady=5)
        descripcion_entry = Entry(edit_window, width=40)
        descripcion_entry.insert(0, selected_plato.descripcion)
        descripcion_entry.pack(pady=5)

        Label(edit_window, text="Región:", bg="#f9f9f9").pack(pady=5)
        region_entry = Entry(edit_window, width=40)
        region_entry.insert(0, selected_plato.region or "")
        region_entry.pack(pady=5)

        Label(edit_window, text="Ingredientes Principales:", bg="#f9f9f9").pack(pady=5)
        ingredientes_entry = Entry(edit_window, width=40)
        ingredientes_entry.insert(0, selected_plato.ingredientes_principales)
        ingredientes_entry.pack(pady=5)

        def update_plato():
            try:
                selected_plato.nombre = nombre_entry.get()
                selected_plato.descripcion = descripcion_entry.get()
                selected_plato.region = region_entry.get()
                selected_plato.ingredientes_principales = ingredientes_entry.get()

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


if __name__ == "__main__":
    root = Tk()
    gui = PlatoGUI(root)
    root.mainloop()