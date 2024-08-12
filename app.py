from shiny import reactive
from shiny.express import input, render, ui, output
from shinywidgets import render_plotly
import pandas as pd 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import dotenv_values

## Creando código para la conección con API de Spotify# Carga las variables desde el archivo .env
config = dotenv_values(".env") # Carga las variables desde el archivo .env

client_id = config['CLIENT_ID']
client_secret = config['CLIENT_SECRET']

### Autenticacióin del usuario
try: 
    # Capturando las credenciales del usuario
    client_credentials_manager = SpotifyClientCredentials(client_id= client_id, client_secret=client_secret)
    
    #Guardando la conección de las credenciales
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

except Exception as e:
    print(f"Hubo un error al ejecutar la autenticación de las credenciales: {e}")
    
### Creando función para captura de datos de Spotify
def DataframeArtistaSpotify(sp, artista):
    """
    Crea un DataFrame de Pandas con información detallada sobre las canciones de un artista en Spotify.

    Args:
        sp: Objeto de conexión a la API de Spotify.
        artista (str): Nombre del artista a buscar.

    Returns:
        pd.DataFrame: DataFrame con las siguientes columnas:
            - Álbum: Nombre del álbum.
            - Tipo: Tipo de lanzamiento (Álbum o Single).
            - Año: Año de lanzamiento del álbum.
            - Canción: Título de la canción.
            - Artistas: Lista de artistas de la canción.
            - Duración: Duración de la canción en formato minutos:segundos.
            - Popularidad: Popularidad de la canción en una escala del 0 al 100.

    Esta función realiza los siguientes pasos:
        1. Busca el ID del artista en la API de Spotify utilizando el nombre proporcionado.
        2. Obtiene los álbumes y singles del artista.
        3. Itera sobre cada álbum y single, extrayendo información sobre cada canción.
        4. Crea una lista con los datos de todas las canciones.
        5. Convierte la lista en un DataFrame de Pandas.
    """
    
    # Buscamos el ID del artista en la API de Spotify
    resultados = sp.search(q=artista, limit=1, type='artist')
    artista_id =  resultados['artists']['items'][0]['id']

    # Crear una lista vacía para almacenar los datos de las canciones
    canciones_data = [] 
    
    # Obtenemos los álbumes y singles del artista
    albumes = sp.artist_albums(artista_id) # Obtener los álbumes del artista

    # Iteramos sobre cada álbum y single
    for album in albumes['items']: # Obtener las canciones para cada álbum
        # Extraemos información del álbum
        album_nombre = album['name']
        album_tipo = album['album_type']
        album_año = album['release_date'].split('-')[0]  # Obtener el año de lanzamiento
        
        # Obtenemos las pistas del álbum
        tracks = sp.album_tracks(album['id'])

        # Iteramos sobre cada canción
        for track in tracks['items']: # Para cada canción, obtener los detalles y añadirlos a la lista de canciones
            cancion_nombre = track['name']
            cancion_artistas = ', '.join([t['name'] for t in track['artists']])
            cancion_duracion = '{:02d}:{:02d}'.format(*divmod(track['duration_ms'] // 1000, 60))
            cancion_popularidad = sp.track(track['id'])['popularity'] # Obtener la popularidad de la canción
            
            # Añadir los detalles de cadaa canción a la lista de canciones
            canciones_data.append([album_nombre, album_tipo, album_año, cancion_nombre, cancion_artistas, cancion_duracion, cancion_popularidad])
    
    return pd.DataFrame(canciones_data, columns=['Álbum', 'Tipo', 'Año', 'Canción', 'Artistas', 'Duración', 'Popularidad'])

## Creando Interfaz de Shiny

with ui.sidebar():
    ui.input_text("text", label="Introduce el nombre del artista")

texto = str(reactive.value([]))

with ui.nav_panel("Gráfico 1"):
    
    with ui.card():
        ui.card_header("Tu artista es: ", 
                        style="color:white; background:#2A2A2A !important;")
        @render.text
        def text_out():
            return f"{input.text()}"

with ui.nav_panel("Gráfico 2"):
    "Page 2 content"
