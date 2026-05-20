# Análisis de Correlaciones — Dataset Impacto Redes Sociales

## Objetivo
Analizar relaciones entre variables numéricas para identificar patrones de comportamiento, indicadores de riesgo y asociaciones entre el uso de redes sociales, hábitos de sueño y salud mental. Todo el análisis debe generarse dentro de `social_impact_analysis.ipynb`.

## Análisis de Correlaciones

### 1. Matriz general de correlación
- Calcular matriz de correlación para todas las variables numéricas.
- Mostrar heatmap anotado directamente en el notebook.
- Identificar correlaciones positivas y negativas relevantes.

### 2. Análisis de relaciones clave
- Scatter plot: `Avg_Daily_Usage_Hours` vs `Mental_Health_Score`.
- Scatter plot: `Avg_Daily_Usage_Hours` vs `Sleep_Hours_Per_Night`.
- Scatter plot: `Sleep_Hours_Per_Night` vs `Mental_Health_Score`.
- Agregar líneas de tendencia o regresión para mejorar la interpretación.

### 3. Análisis por subgrupos
- Recalcular correlaciones agrupadas por `Gender`.
- Recalcular correlaciones agrupadas por `Most_Used_Platform`.
- Comparar diferencias de comportamiento entre grupos.
- Destacar segmentos con posibles patrones de riesgo.

### 4. Interpretación de correlaciones
- Interpretar correlaciones usando:
  - `|r| > 0.7` → Muy fuerte
  - `|r| > 0.5` → Fuerte
  - `|r| > 0.3` → Moderada
  - `|r| < 0.3` → Débil

- Si la correlación entre uso y salud mental es `< -0.5`:
  - Generar alerta de posible impacto psicológico negativo.

- Si la correlación entre uso y sueño es `< -0.5`:
  - Generar alerta de posible interferencia en hábitos de sueño.

- Si la correlación entre sueño y salud mental es `> 0.5`:
  - Destacar el sueño como posible factor protector.

### 5. Exploración visual
- Generar:
  - Heatmap de correlaciones
  - Scatter plots con líneas de tendencia
  - Visualizaciones comparativas por subgrupos
- Mostrar todas las visualizaciones directamente en Jupyter Notebook.

### 6. Insights principales
- Generar entre 4 y 6 conclusiones en markdown.
- Cada insight debe:
  - incluir al menos una métrica concreta
  - explicar patrones detectados
  - identificar posibles implicaciones sobre el bienestar estudiantil