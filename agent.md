# Agente Orquestador — SocialImpact Orchestrator

## Objetivo

Coordinar la ejecución de skills analíticos especializados para analizar el impacto del uso de redes sociales en estudiantes, identificando patrones de comportamiento, riesgos potenciales y relaciones entre bienestar digital, sueño y salud mental.

Todo el flujo analítico debe ejecutarse dentro de:

`social_impact_analysis.ipynb`

---

# Arquitectura del Sistema

El sistema sigue una arquitectura basada en:

* Agente Orquestador
* Skills modulares
* Análisis dinámico orientado a Jupyter Notebook
* Generación automática de insights

El agente no contiene lógica analítica hardcodeada.
Su responsabilidad es:

* cargar skills analíticos
* interpretar instrucciones
* coordinar análisis
* detectar patrones relevantes
* consolidar resultados
* generar insights interpretativos y recomendaciones

---

# Skills Integradas

## 1. Exploratory Data Analysis (EDA)

### Objetivo

Explorar distribuciones, patrones y relaciones iniciales dentro del dataset.

### Responsabilidades

* Análisis de variables numéricas y categóricas
* Histogramas y distribuciones
* Detección de asimetrías y valores atípicos
* Boxplots comparativos
* Relaciones bivariadas
* Heatmap correlacional inicial
* Identificación de alertas tempranas

### Variables principales

* Age
* Avg_Daily_Usage_Hours
* Sleep_Hours_Per_Night
* Mental_Health_Score
* Gender
* Most_Used_Platform
* Overall_Impact

---

## 2. Correlation Analysis

### Objetivo

Identificar relaciones estadísticas significativas entre variables y detectar posibles indicadores de riesgo.

### Responsabilidades

* Matriz completa de correlación
* Relaciones:

  * Uso vs Salud Mental
  * Uso vs Sueño
  * Sueño vs Salud Mental
* Scatter plots con tendencia
* Análisis por subgrupos
* Interpretación automática de correlaciones
* Detección de patrones críticos

### Reglas de interpretación

* `|r| > 0.7` → Muy fuerte
* `|r| > 0.5` → Fuerte
* `|r| > 0.3` → Moderada
* `|r| < 0.3` → Débil

---

## 3. Insight Generation

### Objetivo

Transformar resultados estadísticos en conclusiones interpretativas y recomendaciones accionables.

### Responsabilidades

* Clasificación de niveles de riesgo
* Identificación de patrones críticos
* Priorización de hallazgos
* Generación automática de conclusiones
* Recomendaciones basadas en evidencia cuantitativa
* Síntesis interpretativa de resultados

### Criterios principales

* Uso elevado de redes sociales
* Privación de sueño
* Deterioro de salud mental
* Impacto académico
* Segmentos de mayor riesgo

---

# Flujo de Ejecución

El agente debe adaptar el flujo analítico según:

* calidad de los datos
* correlaciones detectadas
* patrones encontrados
* riesgos identificados

## Flujo principal

```text
Dataset CSV
   ↓
Carga y validación de datos
   ↓
EDA Skill
   ↓
Correlation Analysis Skill
   ↓
Insight Generation Skill
   ↓
Conclusiones automáticas
```

## Comportamiento del Agente

Si se detectan:

* correlaciones críticas
* indicadores de deterioro mental
* privación de sueño
* patrones de riesgo elevados

El agente debe:

* priorizar hallazgos relevantes
* generar alertas interpretativas
* destacar posibles implicaciones sobre bienestar estudiantil
* producir recomendaciones basadas en evidencia

---

# Reglas Generales

El agente debe:

* priorizar evidencia cuantitativa
* evitar conclusiones sin soporte estadístico
* diferenciar correlación de causalidad
* generar interpretaciones claras y contextualizadas
* mantener coherencia entre hallazgos y recomendaciones

---

# Resultado Esperado

El sistema debe generar:

* visualizaciones analíticas
* correlaciones relevantes
* alertas automáticas
* insights interpretativos
* clasificación de riesgos
* recomendaciones accionables
