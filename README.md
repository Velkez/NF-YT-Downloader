# Descargador de Música de YouTube

Aplicación de escritorio en Python para descargar música de canales o playlists de YouTube, con interfaz gráfica, filtrado inteligente y renombrado automático.

---

## Instalación de dependencias

1. **Instala Python 3.11.x**  
   Descárgalo desde [python.org](https://www.python.org/downloads/) o usa Chocolatey:
   ```powershell
   choco install python --version=3.11

2. **Crea y activa un entorno virtual** (opcional pero recomendado)**:**
    ```powershell
    py -3.11 -m venv venv311
    venv311\Scripts\Activate

3. **Instala las dependencias del proyecto:**
    ```powershell
    pip install -r requirements.txt

---
## Empaquetar el programa como .exe (Windows)
1. **Instala PyInstaller:**
    ```powershell
    pip install pyinstaller

2. **Empaqueta usando el archivo .spec:**
    ```powershell
    pyinstaller --clean main.spec

- El ejecutable estará en `NaferYTDownloader.exe`.

---
## Notas
- Si tienes errores de empaquetado con Python 3.10, usa Python 3.11.
- El archivo .gitignore ya ignora carpetas y archivos temporales.
- Puedes modificar el archivo requirements.txt si agregas más dependencias.

---
### Créditos
- Basado en yt-dlp y mutagen.
- Interfaz gráfica con Tkinter.
