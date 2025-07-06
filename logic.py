import os
import yt_dlp
import threading
from utils import extraer_cancion_artista, es_musica

descargadas = set()
descargadas_lock = threading.Lock()

def procesar_entry(entry, download_folder, log_to_consola):
    if not es_musica(entry):
        log_to_consola(f"Omitido (no es música): {entry.get('title', '')}")
        original = os.path.join(download_folder, f"{entry['id']}.mp3")
        if os.path.exists(original):
            os.remove(original)
        return
    cancion, artista = extraer_cancion_artista(entry.get('title', ''), entry.get('uploader', ''))
    clave = (cancion.lower(), artista.lower())
    nuevo_nombre = f"{cancion} - {artista}.mp3"
    nuevo_nombre = os.path.basename(nuevo_nombre)
    nuevo_nombre = nuevo_nombre.replace('/', '').replace('\\', '')
    original = os.path.join(download_folder, f"{entry['id']}.mp3")
    destino = os.path.join(download_folder, nuevo_nombre)
    with descargadas_lock:
        if clave in descargadas:
            if os.path.exists(original):
                os.remove(original)
            log_to_consola(f"Omitida canción repetida: {nuevo_nombre}")
            return
        if os.path.exists(destino):
            if os.path.exists(original):
                os.remove(original)
            log_to_consola(f"Ya existe: {nuevo_nombre}, omitida.")
            descargadas.add(clave)
            return
        if os.path.exists(original):
            os.rename(original, destino)
            descargadas.add(clave)

def ejecutar_descarga(url, download_folder, root):
    descargadas.clear()
    def log_to_consola(msg):
        if root and hasattr(root, 'consola_widget'):
            consola = root.consola_widget
            consola.config(state='normal')
            consola.insert('end', str(msg) + '\n')
            consola.see('end')
            consola.config(state='disabled')
        else:
            print(msg)

    class YTDLPLogger:
        def debug(self, msg):
            if msg.strip():
                log_to_consola(msg)
        def info(self, msg):
            if msg.strip():
                log_to_consola(msg)
        def warning(self, msg):
            if msg.strip():
                log_to_consola('ADVERTENCIA: ' + msg)
        def error(self, msg):
            if msg.strip():
                log_to_consola('ERROR: ' + msg)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_folder, '%(id)s.%(ext)s'),
        'noplaylist': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'logger': YTDLPLogger(),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        entries = result['entries'] if 'entries' in result else [result]
        total = len(entries)
        completadas = [0]
        errores = []
        def procesar_y_actualizar(entry):
            try:
                procesar_entry(entry, download_folder, log_to_consola)
                log_to_consola(f"Descargada: {entry.get('title', 'Desconocido')}")
            except Exception as e:
                errores.append((entry.get('title', 'Desconocido'), str(e)))
                log_to_consola(f"Error al procesar '{entry.get('title', 'Desconocido')}': {e}")
            finally:
                completadas[0] += 1
                log_to_consola(f"Progreso: {completadas[0]} de {total} canciones procesadas.")
                root.update_idletasks()
        threads = []
        for entry in entries:
            t = threading.Thread(target=procesar_y_actualizar, args=(entry,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        if errores:
            log_to_consola("\nCanciones con error de descarga:")
            for titulo, err in errores:
                log_to_consola(f"- {titulo}: {err}")
                # Intentar eliminar el archivo mp3 si existe
                # Buscar el archivo por título (nombre destino) o por id
                # Primero buscar por id
                for entry in entries:
                    if entry.get('title', 'Desconocido') == titulo:
                        id_mp3 = os.path.join(download_folder, f"{entry['id']}.mp3")
                        if os.path.exists(id_mp3):
                            try:
                                os.remove(id_mp3)
                                log_to_consola(f"Archivo eliminado por error: {id_mp3}")
                            except Exception as ex:
                                log_to_consola(f"No se pudo eliminar {id_mp3}: {ex}")
                        # También intentar por nombre destino si existe
                        cancion, artista = extraer_cancion_artista(entry.get('title', ''), entry.get('uploader', ''))
                        nombre_destino = f"{cancion} - {artista}.mp3"
                        nombre_destino = os.path.join(download_folder, nombre_destino)
                        if os.path.exists(nombre_destino):
                            try:
                                os.remove(nombre_destino)
                                log_to_consola(f"Archivo eliminado por error: {nombre_destino}")
                            except Exception as ex:
                                log_to_consola(f"No se pudo eliminar {nombre_destino}: {ex}")
                        break
