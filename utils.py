import re

def extraer_cancion_artista(title, uploader):
    title = re.sub(r"#.*", "", title).strip()
    frases_extras = [
        r"(?i)\bvideo oficial\b", r"(?i)\bofficial video\b", r"(?i)\bletra\b", r"(?i)\blyric[s]?\b",
        r"(?i)\baudio\b", r"(?i)\bvideo\b", r"(?i)\bHD\b", r"(?i)\bremasterizado\b", r"(?i)\bremastered\b",
        r"(?i)\bcover\b", r"(?i)\bclip oficial\b", r"(?i)\bversi[oó]n\b", r"(?i)\boficial\b",
        r"(?i)\bvisualizer\b", r"(?i)\bperformance\b", r"(?i)\bkaraoke\b", r"(?i)\ben vivo\b",
        r"(?i)\bvídeo oficial\b", r"(?i)\bvídeo\b", r"(?i)\bvídeo musical\b", r"(?i)\bmusical video\b"
    ]
    for frase in frases_extras:
        title = re.sub(frase, '', title, flags=re.IGNORECASE)
    title = re.sub(r'\s+', ' ', title).strip()
    partes = re.split(r"\s*-\s*", title)
    if len(partes) == 2:
        if uploader.lower() in partes[0].lower():
            artista = partes[0].strip()
            cancion = partes[1].strip()
        elif uploader.lower() in partes[1].lower():
            artista = partes[1].strip()
            cancion = partes[0].strip()
        else:
            cancion, artista = partes[0].strip(), partes[1].strip()
    else:
        cancion = title.strip()
        artista = uploader.strip() if uploader else "Desconocido"
    return cancion, artista

def es_musica(entry):
    categoria = entry.get('categories', [])
    if isinstance(categoria, list):
        if any('music' in c.lower() or 'música' in c.lower() for c in categoria):
            return True
    elif isinstance(categoria, str):
        if 'music' in categoria.lower() or 'música' in categoria.lower():
            return True
    no_musica = [
        'entrevista', 'interview', 'podcast', 'documental', 'making of', 'detrás de cámaras',
        'capítulo', 'episodio', 'capitulo', 'episode', 'vlog', 'noticia', 'noticias', 'en vivo',
        'live', 'stream', 'streaming', 'directo', 'reacción', 'reaction', 'análisis', 'analisis',
        'resumen', 'review', 'trailer', 'avance', 'teaser', 'película', 'pelicula', 'movie', 'serie', 'series'
    ]
    titulo = entry.get('title', '').lower()
    descripcion = entry.get('description', '').lower() if entry.get('description') else ''
    for palabra in no_musica:
        if palabra in titulo or palabra in descripcion:
            return False
    return True
