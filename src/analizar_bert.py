import pandas as pd
from pysentimiento import create_analyzer

print("🤖 Cargando modelo BERT ...")
analyzer = create_analyzer(task="sentiment", lang="es")

def analizar_con_bert(texto):
    # Filtro básico: si el texto es casi nulo, es Neutral
    if len(str(texto)) < 3:
        return "Neutral", 0.0
    
    try:
        # 2. PREDICCIÓN
        # El modelo procesa el texto y devuelve un objeto con el resultado
        resultado = analyzer.predict(texto)
        
        # Mapeamos los códigos del modelo a palabras amigables
        sentimiento_map = {'POS': 'Positivo', 'NEG': 'Negativo', 'NEU': 'Neutral'}
        etiqueta_codificada = resultado.output
        
        # Obtenemos la probabilidad (confianza) del sentimiento detectado
        confianza = resultado.probas[etiqueta_codificada]
        
        return sentimiento_map[etiqueta_codificada], confianza
    except Exception as e:
        return "Error", 0.0

try:
    # 3. LECTURA DEL ARCHIVO CON LIMPIEZA SUAVE
    print("📂 Leyendo 'comentarios_ready_bert.csv'...")
    df = pd.read_csv("../comentarios_ready_bert.csv")

    print("🧠 Analizando sentimientos con Deep Learning...")
    # Aplicamos la función y guardamos los dos valores resultantes en columnas nuevas
    # La columna que usamos es la que creamos en el script de limpieza suave
    resultados = df['Comentario_Para_BERT'].apply(analizar_con_bert)
    
    # zip(*) es un truco para separar la tupla (Sentimiento, Confianza) en dos listas
    df['Sentimiento'], df['Confianza'] = zip(*resultados)

    # 4. GUARDADO DE RESULTADOS FINALES
    df.to_csv("resultados_bert.csv", index=False)
    print("✅ Análisis completado. Archivo 'resultados_bert.csv' generado.")

    # 5. RESUMEN EN PANTALLA
    print("\n--- Vista Previa de Resultados ---")
    print(df[['Comentario_Para_BERT', 'Sentimiento', 'Confianza']].head(10))
    
    print("\n--- Conteo Final ---")
    print(df['Sentimiento'].value_counts())

except Exception as e:
    print