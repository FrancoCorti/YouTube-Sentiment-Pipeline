import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# Función para limpieza 
def limpiar_texto_nube(texto):
    texto = str(texto).lower() # Todo a minúsculas
    texto = re.sub(r'http\S+|www\S+|https\S+', '', texto) # Eliminar URLs
    texto = re.sub(r'<.*?>', '', texto) # Eliminar etiquetas HTML
    # Mantener solo letras (incluyendo tildes y ñ)
    texto = re.sub(r'[^a-zñáéíóúü\s]', '', texto) 
    return texto.strip()

try:
    # 1. Cargar los resultados de BERT
    print("☁️ Leyendo 'resultados_bert.csv' para generar nubes de palabras...")
    df = pd.read_csv("../data/resultados_bert.csv")

    # 2. Definir palabras a excluir 
    stopwords_es = set([
        "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "u", "de", "del", "al", "a",
        "en", "con", "por", "para", "sin", "sobre", "entre", "hasta", "desde", "es", "son", "fue", "fueron",
        "si", "no", "pero", "más", "menos", "este", "esta", "estos", "estas", "eso", "esa", "esos", "esas",
        "mi", "tu", "su", "nuestro", "nuestra", "vuestro", "vuestra", "mis", "tus", "sus", "nuestros", "nuestras",
        "yo", "tú", "él", "ella", "nosotros", "vosotros", "ellos", "ellas", "se", "lo", "le", "me", "te", "nos",
        "os", "les", "que", "como", "cuando", "donde", "quien", "porque", "muy", "tan", "tanto", "gran", "tal",
        "todo", "toda", "todos", "todas", "vez", "siempre", "nunca", "nadie", "nada", "bien", "mal",
        "solo", "puede", "pueden", "ser", "hacer", "hace", "hizo", "decir", "dijo", "ver", "verlo", "ir", "va",
        "ahora", "luego", "antes", "despues", "aqui", "ahi", "allí", "uno", "otra", "otras", "además", "mucho", 
        "mucha", "muchos", "muchas", "poco", "poca", "pocos", "pocas", "creo", "creer", "siendo", "será", "está", "tiene", "tienen", "tenía", "hay", "hace", "hacen", "cada", "mismo", 
        "así", "aquí", "ahora", "si", "video", "comentario", "canal", "cosa", "base", "cancion", "datos", "entender", "baile", "clave", "cosa", "tienes", "tiene","sabe","sea","suele","alejado","alejados","ni"
    ])

    # 3. Configuración de Sentimientos y sus Colormaps 
    sentimientos = ['Positivo', 'Negativo', 'Neutral']
    colores = {'Positivo': 'Greens', 'Negativo': 'Reds', 'Neutral': 'Blues'}

    plt.figure(figsize=(18, 6)) 

    for i, sentimiento in enumerate(sentimientos):
        # Filtrar datos por sentimiento
        df_filtrado = df[df['Sentimiento'] == sentimiento]
        
        # Validar si hay comentarios para este sentimiento
        if df_filtrado.empty:
            print(f"Saltando nube {sentimiento}: No hay comentarios.")
            continue

        # Unir todos los comentarios en un solo texto gigante y limpiar
        texto_unido = df_filtrado['Comentario'].apply(limpiar_texto_nube).str.cat(sep=" ")
        
        # Validar que el texto resultante no esté vacío
        if len(texto_unido.strip()) < 10:
            print(f"Saltando nube {sentimiento}: Texto insuficiente para generar imagen.")
            continue

        # 4. Generar la Nube de Palabras
        wordcloud = WordCloud(
            width=800, 
            height=500, 
            background_color='white', 
            stopwords=stopwords_es, 
            colormap=colores[sentimiento],
            max_words=100
        ).generate(texto_unido)
        
        # 5. Agregar al gráfico (Subplot)
        plt.subplot(1, 3, i + 1)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f'Palabras {sentimiento}', fontsize=18, fontweight='bold', pad=20)
        plt.axis('off')

    # Guardar y mostrar
    plt.tight_layout()
    plt.savefig("nubes_sentimiento_final.png", dpi=300) # dpi=300 para mayor calidad
    print("¡Éxito! Imagen guardada como 'nubes_sentimiento_final.png'")
    plt.show()

except Exception as e:
    print(f"Error al generar las nubes: {e}")