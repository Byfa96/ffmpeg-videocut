import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Función para cortar video usando FFmpeg
def cortar_video(input_file, output_file, ss, t, modo_preciso=True):
    #Obligatorio tener ffmpeg añadido al PATH xd

    #Es más lento al momento de iniciar en casos donde el video sea muy largo y hay posibilidad de perder frames
    if modo_preciso:
        cmd = [
            "ffmpeg", "-i", input_file, "-ss", ss, "-t", t,
            "-c:v", "copy", "-c:a", "copy", output_file
        ]
    
    #Es más rápido y no se pierden frames, pero puede que el tiempo de inicio no sea exacto (Recomedado)
    else:
        cmd = [
            "ffmpeg", "-ss", ss, "-i", input_file, "-t", t,
            "-c:v", "copy", "-c:a", "copy", output_file
        ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return f"Video cortado con éxito: {output_file}"
    except subprocess.CalledProcessError as e:
        return f"Error al cortar video: {e.stderr}"

# Funciones para la GUI
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de videosss", "*.mp4 *.mkv *.avi *.mov")])
    entrada_var.set(archivo)

def cortar_video_gui():
    input_file = entrada_var.get()
    output_file = salida_var.get()
    ss = inicio_var.get()
    t = duracion_var.get()
    modo_preciso = modo_var.get()

    if not input_file or not output_file or not ss or not t:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return

    resultado = cortar_video(input_file, output_file, ss, t, modo_preciso)
    messagebox.showinfo("Resultado", resultado)


ventana = tk.Tk()
ventana.title("Cortar Videos con FFmpeg")

# Variables de entrada
entrada_var = tk.StringVar()
salida_var = tk.StringVar()
inicio_var = tk.StringVar()
duracion_var = tk.StringVar()
modo_var = tk.BooleanVar(value=True)

# Crear los widgets
tk.Label(ventana, text="Archivo de entrada:").grid(row=0, column=0, sticky="e")
tk.Entry(ventana, textvariable=entrada_var, width=50).grid(row=0, column=1)
tk.Button(ventana, text="Seleccionar", command=seleccionar_archivo).grid(row=0, column=2)

tk.Label(ventana, text="Archivo de salida:").grid(row=1, column=0, sticky="e")
tk.Entry(ventana, textvariable=salida_var, width=50).grid(row=1, column=1)

tk.Label(ventana, text="Tiempo de inicio (-ss):").grid(row=2, column=0, sticky="e")
tk.Entry(ventana, textvariable=inicio_var, width=20).grid(row=2, column=1)

tk.Label(ventana, text="Duración (-t):").grid(row=3, column=0, sticky="e")
tk.Entry(ventana, textvariable=duracion_var, width=20).grid(row=3, column=1)

tk.Label(ventana, text="Modo:").grid(row=4, column=0, sticky="e")
tk.Radiobutton(ventana, text="Preciso", variable=modo_var, value=True).grid(row=4, column=1, sticky="w")
tk.Radiobutton(ventana, text="Aproximado", variable=modo_var, value=False).grid(row=4, column=1)

tk.Button(ventana, text="Cortar Video", command=cortar_video_gui).grid(row=5, column=1)

# Mostrar la ventana
ventana.mainloop()
