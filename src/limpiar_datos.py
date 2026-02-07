import pandas as pd
import re

def limpieza_suave(texto):
    # 1. Aseguramos que sea string
    texto = str(texto)
    
    # 2. Eliminar etiquetas HTML (YouTube mete muchos <br>)
    texto = re.sub(r'<.*?>', ' ', texto)
    
    # 3. Eliminar URLs (Links)
    # Esto busca cualquier cosa que empiece con http, https o www
    texto = re.sub(r'http\S+|www\S+|https\S+', '', texto, flags=re.MULTILINE)
    
    # 4. Eliminar espacios extra (deja el texto prolijo)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto

try:
    print("Leyendo 'comentarios_crudos.csv'...")
    df = pd.read_csv("../data/comentarios_crudos.csv")

    # Aplicamos la limpieza suave
    df['Comentario_Para_BERT'] = df['Comentario'].apply(limpieza_suave)

    # Guardamos este nuevo archivo
    df.to_csv("comentarios_ready_bert.csv", index=False)
    
    print("\n--- Comparación de Limpieza Suave ---")
    print(f"Original: {df['Comentario'].iloc[0][:70]}...")
    print(f"Suave:    {df['Comentario_Para_BERT'].iloc[0][:70]}...")
    
    print(f"\n✅ Archivo 'comentarios_ready_bert.csv' creado con éxito.")

except Exception as e:
    print(f"❌ Error: {e}")