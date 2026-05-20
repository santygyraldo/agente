# Generación de Insights — Dataset Impacto Redes Sociales

## Objetivo
Sintetizar resultados del análisis exploratorio y correlacional para generar conclusiones interpretativas, identificar grupos de riesgo y producir recomendaciones basadas en evidencia cuantitativa. Todo el análisis debe generarse dentro de `social_impact_analysis.ipynb`.

## Generación de Insights

### 1. Síntesis de patrones
- Clasificar niveles de uso de redes sociales:
  - Alto consumo: `> 6 horas`
  - Consumo medio: `4–6 horas`
  - Bajo consumo: `< 4 horas`

- Clasificar estado de salud mental:
  - Deterioro: `< 5`
  - Aceptable: `>= 5`

- Clasificar hábitos de sueño:
  - Privación: `< 6 horas`
  - Adecuado: `>= 6 horas`

- Identificar patrones predominantes entre uso, sueño y salud mental.

### 2. Identificación de riesgos
- Detectar grupos con:
  - uso superior a `media + 1 desviación estándar`
  - salud mental inferior a `media - 1 desviación estándar`
- Calcular porcentaje de estudiantes con afectación académica.
- Identificar segmentos con mayores indicadores de riesgo.

### 3. Priorización de hallazgos
- Clasificar hallazgos según nivel de prioridad:

  - Prioridad Alta:
    - correlaciones `> 0.7` o `< -0.7`

  - Prioridad Media:
    - correlaciones entre `0.5 y 0.7`

  - Prioridad Baja:
    - correlaciones menores a `0.5`

- Destacar automáticamente patrones críticos o preocupantes.

### 4. Generación de recomendaciones
- Generar recomendaciones basadas en:
  - correlaciones detectadas
  - patrones de comportamiento
  - grupos de riesgo identificados
  - hábitos de sueño y uso digital

- Relacionar cada recomendación con evidencia cuantitativa encontrada en el análisis.

### 5. Formato de insights
Cada insight generado debe incluir:

1. Observación:
   - qué patrón fue encontrado

2. Evidencia:
   - métricas o valores relevantes

3. Interpretación:
   - significado del hallazgo

4. Recomendación:
   - posible acción o medida sugerida

### 6. Exploración visual
- Generar:
  - dashboard resumen en grid 2x2
  - mapa de calor de riesgo por subgrupos
  - visualizaciones interpretativas de hallazgos principales

- Mostrar todas las visualizaciones directamente en Jupyter Notebook.

### 7. Insights principales
- Generar entre 5 y 8 conclusiones automáticas.
- Cada conclusión debe:
  - incluir métricas concretas
  - explicar implicaciones relevantes
  - priorizar claridad interpretativa
  - enfocarse en bienestar estudiantil y comportamiento digital