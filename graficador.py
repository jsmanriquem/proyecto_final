# Librerías necesarias para realizar un graficador
from tkinter import Tk, Frame, Button, Label, Menu, Toplevel, StringVar, ttk, Entry, filedialog, colorchooser, Scale, HORIZONTAL , IntVar, Checkbutton, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data_operations import DataOperations  

data_ops = DataOperations()

# Ventana principal
raiz = Tk()
raiz.geometry("1024x780")  # Tamaño de la pantalla
raiz.config(bg="gray")  # Color de fondo
raiz.wm_title('Gráfica de datos')  # Título de la gráfica

# Función para limpiar la gráfica
def limpiar_grafica():
    """Limpia la gráfica y restablece los parámetros a sus valores originales."""
    global y_limits, x_limits, marker_color, marker_type, show_grid, point_size, titulo_grafica, title_fuente, title_size, ejex_shape, ejex_size, ejex_titulo, ejey_shape, ejey_size, ejey_titulo, line_color, line_width, bg_color

    titulo_grafica = StringVar(value="Título de la Gráfica")
    title_fuente = "DejaVu Sans"
    title_size = 12
    
    ejex_titulo = StringVar(value="Eje X")
    ejex_shape = "DejaVu Sans"
    ejex_size = 10

    ejey_titulo = StringVar(value="Eje Y")
    ejey_shape = "DejaVu Sans"
    ejey_size = 10

    line_color = 'blue' 
    line_width = 2       
    bg_color = "white"
    marker_type = "o"
    marker_color = "blue"
    show_grid = False  # Variable para controlar si la grilla está activa o no
    point_size = 5  # Tamaño de los puntos

    # Restablecer límites y zoom
    zoom(reset=True)

    ax.clear()  # Borra el contenido 
    x_limits = [-10, 10]
    y_limits = [-10, 10]
    ax.grid(show_grid)  

    canvas.draw() #Redibujar

    # Mostrar ventana de confirmación
    limpio_si()

# Función para mostrar la confirmación de limpieza
def confirmar_limpiar_grafica():
    # Crear ventana emergente de confirmación
    ventana_confirmacion = Toplevel(raiz)
    ventana_confirmacion.title("Confirmación de limpieza")

    # Mensaje de confirmación
    mensaje = Label(ventana_confirmacion, text="¿Está seguro que desea limpiar la gráfica?")
    mensaje.pack(pady=10)

    # Botón para confirmar limpieza
    boton_si = Button(ventana_confirmacion, text="Sí, limpiar", command=lambda: [limpiar_grafica(), ventana_confirmacion.destroy()])
    boton_si.pack(side="left", padx=10, pady=10)

    # Botón para cancelar limpieza
    boton_no = Button(ventana_confirmacion, text="No, Cancelar", command=ventana_confirmacion.destroy)
    boton_no.pack(side="right", padx=10, pady=10)

def limpio_si():
    ventana_hecho = Toplevel(raiz)
    ventana_hecho.title("Éxito")

    # Mensaje de confirmación
    Label(ventana_hecho, text="La gráfica ha sido limpiada.", pady=20).pack()

    # Botón para cerrar la ventana
    Button(ventana_hecho, text="Aceptar", command=ventana_hecho.destroy).pack(pady=10)

# Menú de opciones para el usuario
barraMenu = Menu(raiz)
raiz.config(menu=barraMenu)

archivoMenu = Menu(barraMenu, tearoff=0)
archivoMenu.add_command(label="Cargar Datos", command=lambda: cargar_datos())

guardarComoMenu = Menu(archivoMenu, tearoff=0)
guardarComoMenu.add_command(label="PDF", command=lambda: guardar_grafica('pdf'))
guardarComoMenu.add_command(label="JPG", command=lambda: guardar_grafica('jpg'))
guardarComoMenu.add_command(label="PNG", command=lambda: guardar_grafica('png'))
archivoMenu.add_cascade(label="Guardar como ...", menu=guardarComoMenu)
archivoMenu.add_separator()
archivoMenu.add_command(label="Limpiar", command= confirmar_limpiar_grafica)

edicionMenu = Menu(barraMenu, tearoff=0)
edicionMenu.add_command(label="Cortar")
edicionMenu.add_command(label="Copiar")
edicionMenu.add_command(label="Pegar")
edicionMenu.add_separator()
edicionMenu.add_command(label="Rehacer")
edicionMenu.add_command(label="Deshacer")

ayudaMenu = Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="Revisar documentación")

barraMenu.add_cascade(label="Archivo", menu=archivoMenu)
barraMenu.add_cascade(label="Edición", menu=edicionMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

# Frame para la gráfica
frame = Frame(raiz, bg='gray22', bd=3)
frame.grid(column=0, row=0, sticky='nsew')

# Crear la figura y el canvas
fig, ax = plt.subplots(dpi=90, figsize=(8, 6), facecolor='#D3D3D3')
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(column=0, row=0, padx=5, pady=5)

# Variables predeterminadas para los títulos
titulo_grafica = StringVar(value="Título de la Gráfica")
title_fuente = "DejaVu Sans"
title_size = 12
personal_ventana_title = None  # Inicializamos la ventana emergente como None

ejex_titulo = StringVar(value="Eje X")
ejex_shape = "DejaVu Sans"
ejex_size = 10
ventana_ejex = None # Venta emergente edición eje x
ventana_lim_x = None # Venta emergente edición límites eje x

ejey_titulo = StringVar(value="Eje Y")
ejey_shape = "DejaVu Sans"
ejey_size = 10
ventana_ejey = None # Ventana emerjente edición eje y
ventana_lim_y = None # Venta emergente edición límites eje y

# Variables de personalización
line_color = 'blue' 
line_width = 2       
bg_color = "white"
marker_type = "o"
marker_color = "blue"
show_grid = False  # Variable para controlar si la grilla está activa o no
point_size = 5  # Tamaño de los puntos
line = None
personalizacion_ventana= None

# Inicializar variables para manejo del zoom y desplazamiento
x_limits = [-10, 10]
y_limits = [-10, 10]
is_dragging = False
start_x, start_y = 0, 0
points = None  # Objeto necesario para almacenamiento de puntos y posterior edición

# Variables para las columnas
columna_x = StringVar()
columna_y = StringVar()

# Widgets de selección
columna_x_combo = None
columna_y_combo = None
graficar_button = None

def cargar_datos():
    """Carga los datos usando DataOperations y permite seleccionar columnas para graficar."""
    if data_ops.load_file(): 
        # Verifica si se cargaron datos
        if data_ops.data is not None and not data_ops.data.empty:
            print(data_ops.data)  
            actualizar_columnas()
        else:
            messagebox.showerror("Error", "No se pudieron cargar los datos del archivo.")

def actualizar_columnas():
    """Actualiza las listas desplegables con las columnas disponibles en el archivo de datos."""
    global columna_x_combo, columna_y_combo, graficar_button

    if columna_x_combo is not None:
        columna_x_combo.grid_forget()
    if columna_y_combo is not None:
        columna_y_combo.grid_forget()
    if graficar_button is not None:
        graficar_button.grid_forget()

    # Obtener las columnas del archivo de datos
    columns = data_ops.data.columns.tolist()
    print("Columnas disponibles:", columns)  # Imprimir las columnas disponibles

    # Solo crear los ComboBox si hay columnas disponibles
    if columns:
        columna_x_combo = ttk.Combobox(raiz, textvariable=columna_x, values=columns)
        columna_x_combo.grid(column=0, row=3, padx=5, pady=5)
        columna_x_combo.set("Selecciona la columna X")
        
        columna_y_combo = ttk.Combobox(raiz, textvariable=columna_y, values=columns)
        columna_y_combo.grid(column=1, row=3, padx=5, pady=5)
        columna_y_combo.set("Selecciona la columna Y")
        
        # Botón para graficar
        graficar_button = Button(raiz, text="Graficar", command=graficar_datos)
        graficar_button.grid(column=2, row=3, padx=5, pady=5)
    else:
        messagebox.showerror("Error", "No se encontraron columnas para graficar.")

def guardar_grafica(formato):
    """
    Función para guardar la gráfica actual en el formato especificado por el usuario.
    
    Parámetros
    -----------
    formato : str
        El formato en el que se desea guardar la gráfica ('pdf', 'png', 'jpg').
    
    Returns
    -----------
    None
        La función abre un cuadro de diálogo para guardar el archivo y luego lo guarda en el formato seleccionado.
    """
    archivo = filedialog.asksaveasfilename(defaultextension=f".{formato}",
                                           filetypes=[(f"{formato.upper()} files", f"*.{formato}"),
                                                      ("All files", "*.*")])

    if archivo:
        fig.savefig(archivo, format=formato)
        print(f"Gráfica guardada como {archivo}")

def graficar_datos():
    """
    Esta función se encarga de dibujar o actualizar la gráfica de datos en el canvas de Matplotlib 
    dentro de la interfaz gráfica. Limpia la gráfica anterior, dibuja una nueva basada en los datos actuales 
    y actualiza los títulos y límites de los ejes.

    Variables globales
    ------------------
    ax : matplotlib.axes.Axes
        El objeto de los ejes en los que se dibuja la gráfica.
    canvas : FigureCanvasTkAgg
        El widget de Matplotlib que renderiza la gráfica en la interfaz gráfica de usuario.
    x : numpy.ndarray
        El arreglo de valores en el eje X que serán graficados.
    y : numpy.ndarray
        El arreglo de valores en el eje Y que serán graficados.
    x_limits : list
        Lista que contiene los límites actuales del eje 'x' en la forma [xmin, xmax].
    y_limits : list
        Lista que contiene los límites actuales del eje 'y' en la forma [ymin, ymax].
    titulo_grafica : tkinter.StringVar
        Variable que almacena el texto del título de la gráfica, el cual puede ser editado por el usuario.
    titulo_eje_x : tkinter.StringVar
        Variable que almacena el texto del título del eje X, editable por el usuario.
    titulo_eje_y : tkinter.StringVar
        Variable que almacena el texto del título del eje Y, editable por el usuario.

    Returns
    ------------
    None
        No retorna ningún valor, sino que actualiza la gráfica con los nuevos datos y títulos.
    """

    x_col = columna_x.get()
    y_col = columna_y.get()

    if x_col not in data_ops.data.columns or y_col not in data_ops.data.columns:
        messagebox.showerror("Error", "Una o ambas columnas seleccionadas no son válidas.")
        return

    if not pd.api.types.is_numeric_dtype(data_ops.data[x_col]) or not pd.api.types.is_numeric_dtype(data_ops.data[y_col]):
        messagebox.showerror("Error", "Las columnas seleccionadas deben ser numéricas.")
        return

    x = data_ops.data[x_col]  # Usar la columna seleccionada para X
    y = data_ops.data[y_col]  # Usar la columna seleccionada para Y
    ax.clear()  # Limpiar la gráfica anterior
    line, = ax.plot(x, y, color=line_color, marker=marker_type, markersize=point_size, markerfacecolor=marker_color, linewidth=line_width, label="Seno")
    ax.set_xlim(x_limits)  # Límites del eje X
    ax.set_ylim(y_limits)  # Límites del eje Y
    ax.set_title(titulo_grafica.get())  # Actualizar título
    ax.set_xlabel(ejex_titulo.get())  # Actualizar título eje X    
    ax.set_ylabel(ejey_titulo.get())  # Actualizar título eje Y
    ax.grid(show_grid)
    ax.set_facecolor(bg_color)
    canvas.draw()  # Actualizar la gráfica

    canvas.mpl_connect('button_press_event', lambda event: on_line_click(event, line))
    canvas.mpl_connect('button_press_event', on_double_click)
    
    # Crear botón "+" para edición de límites eje X
    x_plus_button = Button(raiz, text="+", command=lambda: update_x_limits(raiz))
    x_plus_button.place(x=canvas.get_tk_widget().winfo_width() - 60, y=canvas.get_tk_widget().winfo_height() / 2 + 185)

    # Crear botón "+" para edición de límites eje Y
    y_plus_button = Button(raiz, text="+", command=lambda: update_y_limits(raiz))
    y_plus_button.place(x=canvas.get_tk_widget().winfo_width() - 60, y=canvas.get_tk_widget().winfo_height() / 2 - 185)

# Funciones para abrir ventana emergente y editar los puntos
def update_graph_property(property_type=None, new_value=None):
    global line_width, marker_type, line_color, marker_color, bg_color, point_size, show_grid

    if property_type == 'line_width':
        line_width = float(new_value)
    elif property_type == 'marker_type':
        marker_type = new_value
    elif property_type == 'line_color':
        line_color = colorchooser.askcolor()[1]
    elif property_type == 'marker_color':
        marker_color = colorchooser.askcolor()[1]
    elif property_type == 'bg_color':
        bg_color = colorchooser.askcolor()[1]
        ax.set_facecolor(bg_color)
    elif property_type == 'point_size':
        point_size = float(new_value)
    elif property_type == 'grid':
        show_grid = bool(new_value)
        ax.grid(show_grid)

    graficar_datos()  
    canvas.mpl_connect('button_press_event', lambda event: on_line_click(event, line))


def grafica_ventana(master):
    global personalizacion_ventana

    if personalizacion_ventana is not None and personalizacion_ventana.winfo_exists():
        personalizacion_ventana.lift()
        return  

    personalizacion_ventana = Toplevel(master)
    personalizacion_ventana.title("Personalización de Gráfica")
    personalizacion_ventana.geometry("400x400")

    # Sección del Fondo
    Label(personalizacion_ventana, text="Fondo", font=("Arial", 12, "bold")).pack(pady=10)
    Button(personalizacion_ventana, text="Color de Fondo", command=lambda: update_graph_property('bg_color')).pack(pady=5)

    # Checkbutton para activar/desactivar la grilla
    grid_var = IntVar(value=int(show_grid))  # Inicializar con el valor actual
    Checkbutton(personalizacion_ventana, text="Mostrar Grilla", variable=grid_var, command=lambda: update_graph_property('grid', grid_var.get())).pack(pady=5)

    # Crear un frame para la disposición en dos columnas
    frame = Frame(personalizacion_ventana)
    frame.pack(pady=10)

    linea_frame = Frame(frame)
    linea_frame.grid(row=0, column=0, padx=20)

    Label(linea_frame, text="Línea", font=("Arial", 12, "bold")).pack(pady=10)

    # Botón para seleccionar el color de la línea
    Button(linea_frame, text="Color de Línea", command=lambda: update_graph_property('line_color')).pack(pady=5)

    # Slider para ajustar el grosor de la línea
    Label(linea_frame, text="Tamaño de Línea:").pack(pady=5)
    line_width_slider = Scale(linea_frame, from_=0.5, to=10, resolution=0.1, orient=HORIZONTAL, command=lambda value: update_graph_property('line_width', value))
    line_width_slider.set(line_width)
    line_width_slider.pack(pady=5)

    puntos_frame = Frame(frame)
    puntos_frame.grid(row=0, column=1, padx=20)

    Label(puntos_frame, text="Puntos", font=("Arial", 12, "bold")).pack(pady=10)

    # Menú para seleccionar el tipo de marcador
    Label(puntos_frame, text="Tipo de Marcador:").pack()
    marker_options = ['o', 'x', '^', 's', '*']  
    marker_var = StringVar(value=marker_type)
    marker_menu = ttk.Combobox(puntos_frame, textvariable=marker_var, values=marker_options)
    marker_menu.pack(pady=5)
    marker_menu.bind("<<ComboboxSelected>>", lambda event: update_graph_property('marker_type', marker_var.get()))

    # Botón para seleccionar el color de los puntos
    Button(puntos_frame, text="Color de Puntos", command=lambda: update_graph_property('marker_color')).pack(pady=5)

    # Slider para ajustar el tamaño de los puntos
    Label(puntos_frame, text="Tamaño de Puntos:").pack(pady=5)
    point_size_slider = Scale(puntos_frame, from_=1, to=20, resolution=1, orient=HORIZONTAL, command=lambda value: update_graph_property('point_size', value))
    point_size_slider.set(point_size)
    point_size_slider.pack(pady=5)

def on_line_click(event, line):
    if event.inaxes and event.button == 1:  # Botón izquierdo del mouse
        # Se obtienen las coordenadas de los puntos de la línea
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        
        # Comprobar si el click fue cerca de la línea
        for i in range(len(xdata)):
            if abs(event.xdata - xdata[i]) < 0.1 and abs(event.ydata - ydata[i]) < 0.1:
                grafica_ventana(raiz) 
                break

# Función para aplicar los cambios del título
def apply_title_changes(title_size_var, title_fuente_var, titulo_grafica_entry):
    global title_size, title_fuente, titulo_grafica
    titulo_grafica.set(titulo_grafica_entry.get())  # Obtener el nuevo título
    
    # Obtener valores seleccionados
    title_size = int(title_size_var.get())
    title_fuente = title_fuente_var.get()
    
    # Actualizar el título de la gráfica
    ax.set_title(titulo_grafica.get(), fontsize=title_size, fontname=title_fuente)
    
    # Redibujar la gráfica
    canvas.draw()

# Función para abrir la ventana emergente de edición del título
def grafica_ventana_title(master):
    global personal_ventana_title
    
    # Verificar si la ventana ya está abierta
    if personal_ventana_title is not None and personal_ventana_title.winfo_exists():
        personal_ventana_title.lift()  # Lleva la ventana al frente
        return  # No abrir otra ventana

    # Crear nueva ventana
    personal_ventana_title = Toplevel(master)
    personal_ventana_title.title("Personalización de Título")
    personal_ventana_title.geometry("300x250")
    
    # Nombre del Título
    Label(personal_ventana_title, text="Ingrese el Título:").pack(pady=10)
    titulo_grafica_entry = Entry(personal_ventana_title)
    titulo_grafica_entry.insert(0, titulo_grafica.get())  # Mostrar el título actual
    titulo_grafica_entry.pack(pady=5)
    
    # Selección del tamaño de letra (8,10,12,...)
    Label(personal_ventana_title, text="Tamaño de la letra:").pack()
    title_size_options = [8, 10, 12, 14, 16, 18, 20]  # Tamaños de letra disponibles
    title_size_var = StringVar(value=str(title_size))  # Valor actual del tamaño
    
    # Crear un Combobox para seleccionar el tamaño de letra
    title_size_combobox = ttk.Combobox(personal_ventana_title, textvariable=title_size_var, values=title_size_options)
    title_size_combobox.pack(pady=5)
    
    # Selección de la fuente
    Label(personal_ventana_title, text="Fuente de la letra:").pack()
    title_fuente_options = ['Liberation Serif', 'DejaVu Serif']  # Fuentes disponibles (depende del usuario)
    title_fuente_var = StringVar(value=title_fuente)  # Valor actual de la fuente
    
    # Crear un Combobox para seleccionar la fuente
    title_fuente_combobox = ttk.Combobox(personal_ventana_title, textvariable=title_fuente_var, values=title_fuente_options)
    title_fuente_combobox.pack(pady=5)
    
    # Botón para aplicar los cambios
    Button(personal_ventana_title, text="Aplicar Cambios", 
           command=lambda: apply_title_changes(title_size_var, title_fuente_var, titulo_grafica_entry)).pack(pady=10)

# Función para aplicar los cambios del título
def apply_xaxis_changes(ejex_size_var, ejex_fuente_var, ejex_titulo_entry):
    global ejex_size, ejex_shape, ejex_titulo
    ejex_titulo.set(ejex_titulo_entry.get())  # Obtener el nuevo título del eje X    
    # Obtener valores seleccionados
    ejex_size = int(ejex_size_var.get())
    ejex_shape = ejex_fuente_var.get()
    
    # Actualizar el título del eje X de la gráfica
    ax.set_xlabel(ejex_titulo.get(), fontsize=ejex_size, fontname=ejex_shape)
    
    # Redibujar la gráfica
    canvas.draw()

# Función para abrir la ventana emergente de edición del título
def grafica_ventana_ejex(master):
    global ventana_ejex
    
    # Verificar si la ventana ya está abierta
    if ventana_ejex is not None and ventana_ejex.winfo_exists():
        ventana_ejex.lift()  # Lleva la ventana al frente
        return  # No abrir otra ventana

    # Crear nueva ventana
    ventana_ejex = Toplevel(master)
    ventana_ejex.title("Personalización Eje x")
    ventana_ejex.geometry("300x250")
    
    # Nombre del Título
    Label(ventana_ejex, text="Ingrese Eje x:").pack(pady=10)
    titulo_ejex_var = Entry(ventana_ejex)
    titulo_ejex_var.insert(0, ejex_titulo.get())  # Mostrar el título actual
    titulo_ejex_var.pack(pady=5)
    
    # Selección del tamaño de letra (8,10,12,...)
    Label(ventana_ejex, text="Tamaño de la letra:").pack()
    ejex_size_options = [8, 10, 12, 14, 16, 18, 20]  # Tamaños de letra disponibles
    ejex_size_var = StringVar(value=str(ejex_size))  # Valor actual del tamaño
    
    # Crear un Combobox para seleccionar el tamaño de letra
    ejex_size_combobox = ttk.Combobox(ventana_ejex, textvariable=ejex_size_var, values=ejex_size_options)
    ejex_size_combobox.pack(pady=5)
    
    # Selección de la fuente
    Label(ventana_ejex, text="Fuente de la letra:").pack()
    ejex_fuente_options = ['Liberation Serif', 'DejaVu Serif']  # Fuentes disponibles (depende del usuario)
    ejex_fuente_var = StringVar(value=ejex_shape)  # Valor actual de la fuente
    
    # Crear un Combobox para seleccionar la fuente
    ejex_fuente_combobox = ttk.Combobox(ventana_ejex, textvariable=ejex_fuente_var, values=ejex_fuente_options)
    ejex_fuente_combobox.pack(pady=5)
    
    # Botón para aplicar los cambios
    Button(ventana_ejex, text="Aplicar Cambios", 
           command=lambda: apply_xaxis_changes(ejex_size_var, ejex_fuente_var,titulo_ejex_var)).pack(pady=10)

# Función para aplicar los cambios del eje y
def apply_yaxis_changes(ejey_size_var, ejey_fuente_var, ejey_titulo_entry):
    global ejey_size, ejey_shape, ejey_titulo
    ejey_titulo.set(ejey_titulo_entry.get())  # Obtener el nuevo título del eje X    
    # Obtener valores seleccionados
    ejey_size = int(ejey_size_var.get())
    ejey_shape = ejey_fuente_var.get()
    
    # Actualizar el título del eje X de la gráfica
    ax.set_ylabel(ejey_titulo.get(), fontsize=ejey_size, fontname=ejey_shape)
    
    # Redibujar la gráfica
    canvas.draw()

# Función para abrir la ventana emergente de edición del eje y
def grafica_ventana_ejey(master):
    global ventana_ejey
    
    # Verificar si la ventana ya está abierta
    if ventana_ejey is not None and ventana_ejey.winfo_exists():
        ventana_ejey.lift()  # Lleva la ventana al frente
        return  # No abrir otra ventana

    # Crear nueva ventana
    ventana_ejey = Toplevel(master)
    ventana_ejey.title("Personalización Eje y")
    ventana_ejey.geometry("300x250")
    
    # Nombre del Título
    Label(ventana_ejey, text="Ingrese Eje y:").pack(pady=10)
    titulo_ejey_var = Entry(ventana_ejey)
    titulo_ejey_var.insert(0, ejey_titulo.get())  # Mostrar el título actual
    titulo_ejey_var.pack(pady=5)
    
    # Selección del tamaño de letra (8,10,12,...)
    Label(ventana_ejey, text="Tamaño de la letra:").pack()
    ejey_size_options = [8, 10, 12, 14, 16, 18, 20]  # Tamaños de letra disponibles
    ejey_size_var = StringVar(value=str(ejey_size))  # Valor actual del tamaño
    
    # Crear un Combobox para seleccionar el tamaño de letra
    ejey_size_combobox = ttk.Combobox(ventana_ejey, textvariable=ejey_size_var, values=ejey_size_options)
    ejey_size_combobox.pack(pady=5)
    
    # Selección de la fuente
    Label(ventana_ejey, text="Fuente de la letra:").pack()
    ejey_fuente_options = ['Liberation Serif', 'DejaVu Serif']  # Fuentes disponibles (depende del usuario)
    ejey_fuente_var = StringVar(value=ejey_shape)  # Valor actual de la fuente
    
    # Crear un Combobox para seleccionar la fuente
    ejey_fuente_combobox = ttk.Combobox(ventana_ejey, textvariable=ejey_fuente_var, values=ejey_fuente_options)
    ejey_fuente_combobox.pack(pady=5)
    
    # Botón para aplicar los cambios
    Button(ventana_ejey, text="Aplicar Cambios", 
           command=lambda: apply_yaxis_changes(ejey_size_var, ejey_fuente_var,titulo_ejey_var)).pack(pady=10)

# Función para detectar doble clic en el título y abrir la ventana de edición
def on_double_click(event):
    if event.dblclick:
        # Coordenadas del clic en la ventana gráfica
        x, y = event.x, event.y

        # Obtener la posición del título
        bbox_title = ax.title.get_window_extent(canvas.get_renderer())
        bbox_xlabel = ax.xaxis.label.get_window_extent(canvas.get_renderer())
        bbox_ylabel = ax.yaxis.label.get_window_extent(canvas.get_renderer())

        # Comprobar si el clic fue en el título de la gráfica
        if bbox_title.contains(x, y):
            grafica_ventana_title(raiz)  # Usar la ventana principal 'raiz' para abrir la personalización
        # Comprobar si el clic fue en el título de la gráfica
        elif bbox_xlabel.contains(x, y):
            grafica_ventana_ejex(raiz)
        # Comprobar si el clic fue hecho en Eje y
        elif bbox_ylabel.contains(x,y):
            grafica_ventana_ejey(raiz)

# Conectar evento de doble clic
canvas.mpl_connect('button_press_event', on_double_click)

# Guardar límites originales para reestablecer al tamaño original
origx_lim = x_limits.copy()
origy_lim = y_limits.copy()

def update_x_limits(master):
    """Muestra una ventana emergente para actualizar los límites del eje X."""
    global ventana_lim_x

    # Crear nueva ventana
    ventana_lim_x = Toplevel(master)
    ventana_lim_x.title("Límites Eje X")
    ventana_lim_x.geometry("300x250")

    # Etiquetas y campos de entrada para x_min y x_max
    Label(ventana_lim_x, text="Ingrese x_min:").pack(pady=5)
    x_min_entry = Entry(ventana_lim_x)
    x_min_entry.insert(0, str(x_limits[0]))  # Valor de x_min
    x_min_entry.pack()

    Label(ventana_lim_x, text="Ingrese x_max:").pack(pady=5)
    x_max_entry = Entry(ventana_lim_x)
    x_max_entry.insert(0, str(x_limits[1]))  # Valor de x_max
    x_max_entry.pack()

    # Botón para actualizar los límites de X
    Button(ventana_lim_x, text="Actualizar Límites", command=lambda: set_x_limits(x_min_entry, x_max_entry)).pack(pady=10)

def set_x_limits(x_min_entry, x_max_entry):
    """Actualiza los límites del eje X según los valores ingresados por el usuario en la ventana emergente."""
    global x_limits, origx_lim

    try:
        # Obtener y validar valores ingresados
        x_min = float(x_min_entry.get())
        x_max = float(x_max_entry.get())
        if x_min < x_max:
            x_limits = [x_min, x_max]
            origx_lim = x_limits.copy()
            print(f"Límites del eje X actualizados: {x_limits}")
            graficar_datos()  # Redibuja la gráfica con los nuevos límites
        else:
            print("El valor de x_min debe ser menor que x_max.")
    except ValueError:
        print("Por favor, ingrese valores numéricos válidos.")

def update_y_limits(master):
    """Muestra una ventana emergente para actualizar los límites del eje Y."""
    global ventana_lim_y

    # Crear nueva ventana
    ventana_lim_y = Toplevel(master)
    ventana_lim_y.title("Límites Eje Y")
    ventana_lim_y.geometry("300x250")

    # Etiquetas y campos de entrada para x_min y x_max
    Label(ventana_lim_y, text="Ingrese y_min:").pack(pady=5)
    y_min_entry = Entry(ventana_lim_y)
    y_min_entry.insert(0, str(y_limits[0]))  # Valor de y_min
    y_min_entry.pack()

    Label(ventana_lim_y, text="Ingrese y_max:").pack(pady=5)
    y_max_entry = Entry(ventana_lim_y)
    y_max_entry.insert(0, str(y_limits[1]))  # Valor de y_max
    y_max_entry.pack()

    # Botón para actualizar los límites de X
    Button(ventana_lim_y, text="Actualizar Límites", command=lambda: set_y_limits(y_min_entry, y_max_entry)).pack(pady=10)

def set_y_limits(y_min_entry, y_max_entry):
    """Actualiza los límites del eje Y según los valores ingresados por el usuario en la ventana emergente."""
    global y_limits, origy_lim

    try:
        # Obtener y validar valores ingresados
        y_min = float(y_min_entry.get())
        y_max = float(y_max_entry.get())
        if y_min < y_max:
            y_limits = [y_min, y_max]
            origy_lim = y_limits.copy()
            print(f"Límites del eje Y actualizados: {y_limits}")
            graficar_datos()  # Redibuja la gráfica con los nuevos límites
        else:
            print("El valor de y_min debe ser menor que y_max.")
    except ValueError:
        print("Por favor, ingrese valores numéricos válidos.")

def zoom(event=None,reset=False):
    """
    Ajuste del nivel de zoom en la gráfica redibujando los ejes a partir de nuevos límites que 
    se actualizarán dependiendo de la amplificación que de el usuario. El nivel de zoom es 
    controlado por el valor de una barra deslizante [scale] y la gráfica es redibujada en 
    función de los límites ajustados. También se actualiza el porcentaje de zoom mostrado en pantalla
    [zoom_label]. Si se desea volver al tamaño original de la gráfica este se reestablecera cuando 
    [reset] sea True.

    Parámetros
    ----------
    event : tkinter.Event, optional
        Evento que dispara la acción de zoom.

    reset : bool, optional
        Si True, restablece los límites originales de la gráfica.
    
    Variables globales
    ------------------
    x_limits : list
        Lista que contiene los límites actuales del eje 'x' en la forma [xmin, xmax].
    y_limits : list
        Lista que contiene los límites actuales del eje 'y' en la forma [ymin, ymax].

    Returns
    -------
    None
        La función no retorna ningún valor, simplemente actualiza la gráfica y la interfaz de usuario.
    """
    global x_limits, y_limits # Variables globales, límites de 'x' y 'y'
    if reset:
        # Restablecer límites originales
        x_limits = origx_lim.copy()
        y_limits = origy_lim.copy()
        zoom_label.config(text="Zoom: 100%")  # Restablecer la etiqueta de zoom
        x_scale.set(0)  # Resetear la barra de zoom de X
        y_scale.set(0)  # Resetear la barra de zoom de Y
    else:
        # Obtener los valores de las barras deslizantes para cada eje
        x_zoom_level = x_scale.get()
        y_zoom_level = y_scale.get()
        
        x_mid = (origx_lim[1] + origx_lim[0]) / 2  # Punto medio 'x'
        x_zoom_factor = 1 + x_zoom_level
        x_range = (origx_lim[1] - origx_lim[0]) / x_zoom_factor
        x_limits = [x_mid - x_range / 2, x_mid + x_range / 2]
        
        y_mid = (origy_lim[1] + origy_lim[0]) / 2  # Punto medio 'y'
        y_zoom_factor = 1 + y_zoom_level
        y_range = (origy_lim[1] - origy_lim[0]) / y_zoom_factor
        y_limits = [y_mid - y_range / 2, y_mid + y_range / 2]

        # Actualizar la etiqueta de porcentaje de zoom para cada eje
        x_zoom_percentage = int((x_zoom_level / 10) * 100)
        y_zoom_percentage = int((y_zoom_level / 10) * 100)
        zoom_label.config(text=f"Zoom X: {x_zoom_percentage}% | Zoom Y: {y_zoom_percentage}%")

    # Redibujar la gráfica con los nuevos límites
    graficar_datos() # Modificar respecto a los módulos por agregar

# Funciones para manejar el desplazamiento con el mouse sobre la gráfica
def on_press(event):
    """
    Evento que permite inicializar un evento con un clic siempre y cuando este se haya 
    realizado dentro de la gráfica, es decir, definido dentro de los límites de la definición
    para matplotlib. 

    Parámetros
    ----------
    event : matplotlib.backend_bases.MouseEvent
        Evento que contiene la información del clic del mouse dentro de los límites de la 
        gráfica y almacenando las coordenadas [x,y] del clic realizado.

    Variables globales
    ------------------
    is_dragging : bool
        Indicador que se establece en True cuando el usuario está arrastrando el mouse.
    start_x : float
        Coordenada 'x' donde se inició el clic en la gráfica.
    start_y : float
        Coordenada 'y' donde se inició el clic en la gráfica.

    Returns
    -------
    None
        La función no retorna ningún valor, simplemente actualiza datos.
    """
    global is_dragging, start_x, start_y
    if event.inaxes:
        is_dragging = True   # Interacción con la gráfica
        start_x, start_y = event.xdata, event.ydata  # Almacenamiento de datos iniciales de clic

def on_release(event):
    """
    Evento que permite finalizar la función anterior de interacción del usuario y la 
    gráfica a través del mouse. A demás, permite que la acción solo se realice siempre y 
    cuando el usuario deslice mientras hace el clic, al soltar el clic se finaliza la acción.

    Parámetros
    ----------
    event : matplotlib.backend_bases.MouseEvent
        Evento que contiene la información del clic del mouse dentro de los límites de la 
        gráfica y almacenando las coordenadas [x,y] del clic realizado.

    Variables globales
    ------------------
    is_dragging : bool
        Indicador que se establece en False cuando el usuario suelta el botón del mouse,
        lo que indica que la interacción/arrastre ha finalizado.

    Returns
    -------
    None
        La función no retorna ningún valor, simplemente actualiza datos.
    """
    global is_dragging
    is_dragging = False # Finalizar el evento de interacción al soltar el clic.

def on_motion(event):
    """
    Evento que permite desplazar la gráfica mientras el usuario interactúa/arrastra el 
    mouse, ajustando los límites de los ejes de acuerdo al desplazamiento del cursor.

    Parámetros
    ----------
    event : matplotlib.backend_bases.MouseEvent
        Evento que contiene la información del clic del mouse dentro de los límites de la 
        gráfica y almacenando las coordenadas [x,y] del clic realizado.

    Variables globales
    ------------------
    x_limits : list
        Lista que contiene los límites actuales del eje 'x' en la forma [xmin, xmax].
    y_limits : list
        Lista que contiene los límites actuales del eje 'y' en la forma [ymin, ymax].
    start_x : float
        Coordenada 'x' donde se inició el clic en la gráfica.
    start_y : float
        Coordenada 'y' donde se inició el clic en la gráfica.

    
    """
    global x_limits, y_limits, start_x, start_y
    if is_dragging and event.inaxes: # Verificación de interacción True and True
        
        # Calculo de diferencia entre el clic inicial y la posición actual del cursor
        dx = start_x - event.xdata
        dy = start_y - event.ydata
        
        # Redefinir los límites de acuerdo al desplazamiento
        x_limits = [x + dx for x in x_limits]
        y_limits = [y + dy for y in y_limits]

        # Redibujar la gráfica con los nuevos límites
        graficar_datos()

# Conectar eventos del ratón
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

# Crear frame para los controles de zoom
frame_zoom = Frame(raiz, bg="gray22")
frame_zoom.grid(row=1, column=0, padx=10, pady=10)

# Barra de zoom
style = ttk.Style()
style.configure("Horizontal.TScale", background='gray22')  # Configurar estilo para la barra

# Barra zoom eje x
x_scale = ttk.Scale(frame_zoom, to=10, from_=0, orient='horizontal', length=200, style="Horizontal.TScale", command=zoom)
x_scale.grid(column=0, row=0, padx=5)

#Barra zoom eje y
y_scale = ttk.Scale(frame_zoom, to=10, from_=0, orient='horizontal', length=200, style="Horizontal.TScale", command=zoom)
y_scale.grid(column=1, row=0, pady=5)

# Etiqueta para mostrar el porcentaje de zoom de cada eje
zoom_label = ttk.Label(frame, text="Zoom X: 0% | Zoom Y: 0%")
zoom_label.grid(column=0, row=5)

# Ejecutar la aplicación
raiz.mainloop()
