import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import pandas as pd


load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    print("ERROR: No se encontró la YOUTUBE_API_KEY. Revisá el archivo .env")
else:
    print(f"Llave cargada correctamente (empieza con: {API_KEY[:5]}...)")

youtube = build('youtube', 'v3', developerKey=API_KEY)


# 2. Función para obtener comentarios de un video
def obtener_comentarios(video_id):
    comentarios = []
    
    # Pedimos a la API los comentarios del video
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=50, # Traemos los primeros 50
        textFormat="plainText"
    )
    response = request.execute()

    # Extraemos solo el texto del comentario y lo guardamos en una lista
    for item in response['items']:
        comentario = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comentarios.append(comentario)
    
    return comentarios

# 3. Probamos con un video (Puse uno de ejemplo)
ID_DEL_VIDEO = "yLKuq6SpMfs" 

try:
    print("Iniciando extracción...")
    lista_comentarios = obtener_comentarios(ID_DEL_VIDEO)
    
    # Creamos una "Tabla" (DataFrame) con los resultados
    df = pd.DataFrame(lista_comentarios, columns=["Comentario"])
    
    # Mostramos los primeros 5 en pantalla
    print("\n--- Comentarios extraídos con éxito ---")
    print(df.head())
    
    # Guardamos en un archivo CSV para no perder los datos
    df.to_csv("comentarios_crudos.csv", index=False)
    print("Los datos se guardaron en 'comentarios_crudos.csv'")

except Exception as e:
    print(f" Ocurrió un error: {e}")