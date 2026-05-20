# Análisis Exploratorio de Datos (EDA) — Dataset Impacto Redes Sociales

## Objetivo
Explorar distribuciones, patrones y relaciones iniciales dentro del dataset para comprender el comportamiento del uso de redes sociales y su posible impacto sobre el bienestar estudiantil. Todo el análisis debe generarse dentro de `social_impact_analysis.ipynb`.

## Exploración de Datos

### 1. Distribución de variables
- Generar histogramas para:
  - `Age`
  - `Avg_Daily_Usage_Hours`
  - `Sleep_Hours_Per_Night`
  - `Mental_Health_Score`
- Mostrar media y mediana en cada distribución.
- Identificar:
  - asimetrías
  - concentraciones
  - posibles valores atípicos

### 2. Análisis de correlaciones
- Calcular matriz de correlación entre variables numéricas.
- Mostrar heatmap anotado directamente en el notebook.
- Detectar relaciones positivas y negativas relevantes.

### 3. Comparaciones por categoría
- Generar boxplots de:
  - `Mental_Health_Score` por `Most_Used_Platform`
  - `Mental_Health_Score` por `Gender`
- Comparar dispersión, medianas y posibles diferencias entre grupos.

### 4. Relaciones bivariadas
- Scatter plot:
  - `Avg_Daily_Usage_Hours` vs `Mental_Health_Score`
  - `Avg_Daily_Usage_Hours` vs `Sleep_Hours_Per_Night`
  - `Sleep_Hours_Per_Night` vs `Mental_Health_Score`
- Agregar líneas de tendencia o regresión.
- Identificar patrones de comportamiento.

### 5. Interpretación de alertas
- Si `Avg_Daily_Usage_Hours > 6`:
  - Destacar posible consumo elevado.

- Si `Mental_Health_Score < 5`:
  - Destacar posible deterioro emocional.

- Si `Sleep_Hours_Per_Night < 6`:
  - Destacar posible privación de sueño.

- Si correlación uso-salud mental `< -0.5`:
  - Generar alerta de relación preocupante.

### 6. Exploración visual
- Generar:
  - Histogramas en grid 2x2
  - Heatmap correlacional
  - Boxplots comparativos
  - Scatter plots en grid 2x2
- Mostrar todas las visualizaciones directamente en Jupyter Notebook.

### 7. Insights principales
- Generar entre 4 y 6 conclusiones automáticas.
- Cada insight debe:
  - incluir métricas concretas
  - describir patrones encontrados
  - explicar posibles implicaciones sobre bienestar estudiantil