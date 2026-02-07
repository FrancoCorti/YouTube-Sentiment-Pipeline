import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    # 1. Cargar los resultados de BERT
    df = pd.read_csv("../data/resultados_bert.csv")

    # 2. Configurar el estilo visual
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))

    # 3. Definir colores lógicos (Rojo para Neg, Verde para Pos, Gris para Neu)
    paleta = {"Positivo": "#2ecc71", "Neutral": "#95a5a6", "Negativo": "#e74c3c"}

    # 4. Crear un gráfico de barras (Countplot)
    ax = sns.countplot(x='Sentimiento', data=df, palette=paleta, order=["Positivo", "Neutral", "Negativo"])

    # 5. Añadir detalles profesionales
    plt.title('Sentimiento de la Comunidad (Modelo BERT Español)', fontsize=16, fontweight='bold')
    plt.xlabel('Categoría de Sentimiento', fontsize=12)
    plt.ylabel('Cantidad de Comentarios', fontsize=12)

    # Añadir los números arriba de cada barra
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha = 'center', va = 'center', xytext = (0, 9), textcoords = 'offset points')

    # 6. Guardar la imagen
    plt.savefig("reporte_grafico_barras.png")
    print("Gráfico profesional guardado como 'reporte_grafico_barras.png'")
    
    # Mostrar el gráfico
    plt.show()

except Exception as e:
    print(f"Error al graficar: {e}")