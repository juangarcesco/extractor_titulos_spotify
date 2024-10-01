import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configura tus credenciales
client_id = 'TU_CLIENT_ID'
client_secret = 'TU_CLIENT_SECRET'

# Autenticación con la API de Spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def obtener_todos_los_episodios(podcast_id):
    episodios = []
    offset = 0
    
    # Obtener el total de episodios primero
    total_episodios = 0
    while True:
        results = sp.show_episodes(podcast_id, limit=50, offset=offset)
        total_episodios += len(results['items'])
        if results['next'] is None:
            break
        offset += 50

    # Reiniciar offset para obtener los episodios y asignar numeración descendente
    offset = 0
    while True:
        results = sp.show_episodes(podcast_id, limit=50, offset=offset)
        for i, episodio in enumerate(results['items']):
            episodio['numero'] = total_episodios - len(episodios)  # Numeración descendente hasta 1
            
            # Agregar duración, fecha y descripción
            duracion_segundos = episodio['duration_ms'] // 1000  # Duración en segundos
            episodio['duracion'] = duracion_segundos / 60  # Convertir a minutos
            episodio['fecha'] = episodio['release_date']  # Fecha de lanzamiento
            episodio['descripcion'] = episodio['description']  # Descripción del episodio

            episodios.append(episodio)
        if results['next'] is None:
            break
        offset += 50

    return episodios

# Reemplaza 'PODCAST_ID' con el ID del podcast
podcast_id = 'EL_ID_DEL_PODCAST'
todos_los_episodios = obtener_todos_los_episodios(podcast_id)

# Exportar a un archivo .txt con numeración, descripción y duración
with open("episodios_podcast.txt", "w", encoding="utf-8") as archivo:
    for episodio in todos_los_episodios:
        archivo.write(f"Título {episodio['numero']}: {episodio['name']}\n")
        archivo.write(f"Duración: {episodio['duracion']:.2f} minutos\n")  # Mostrar en minutos con dos decimales
        archivo.write(f"Fecha: {episodio['fecha']}\n")
        archivo.write(f"Descripción: {episodio['descripcion']}\n\n")  # Añadir una línea en blanco entre episodios

print("Episodios exportados a 'episodios_podcast.txt'")

