import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    # 1. Cargar los resultados finales de BERT
    df = pd.read_csv("../data/resultados_bert.csv")

    # 2. Configurar el estilo del gráfico
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # 3. Crear el histograma con una curva de densidad (KDE)
    # Dividimos por sentimiento para ver cuál es más "claro" para la IA
    sns.histplot(data=df, x="Confianza", hue="Sentimiento", 
                 element="step", kde=True, palette="viridis", alpha=0.6)

    # 4. Personalización técnica
    plt.title("Distribución de la Confianza del Modelo BERT", fontsize=15, fontweight='bold')
    plt.xlabel("Nivel de Confianza (0.0 a 1.0)", fontsize=12)
    plt.ylabel("Frecuencia de Comentarios", fontsize=12)
    plt.xlim(0, 1) # El rango de confianza siempre es de 0 a 1

    # 5. Guardar y mostrar
    plt.savefig("histograma_confianza_bert.png", dpi=300)
    print("Histograma guardado como 'histograma_confianza_bert.png'")
    plt.show()

except Exception as e:
    print(f"Error al generar el histograma: {e}")