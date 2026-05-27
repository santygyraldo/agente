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
* Evaluación comparativa de modelos

El agente no contiene lógica analítica hardcodeada.

Su responsabilidad es:

* cargar y coordinar skills analíticos
* interpretar instrucciones
* validar flujo de ejecución
* consolidar resultados
* detectar patrones relevantes
* seleccionar el modelo más adecuado
* generar insights interpretativos y recomendaciones

---

# Skills Integradas

## 1. Data Wrangling

### Objetivo

Limpiar, validar y preparar el dataset antes de ejecutar análisis estadísticos o generación de insights.

### Responsabilidades

* Detección de valores nulos
* Tratamiento de datos faltantes
* Eliminación de duplicados
* Detección de outliers mediante IQR
* Validación de tipos de datos
* Transformación de variables categóricas
* Preparación del dataset para análisis

### Reglas de tratamiento

#### Valores nulos

* < 5%
  - eliminar registros faltantes

* 5% – 20%
  - imputar mediana (numéricos)
  - imputar moda (categóricos)

* > 20%
  - evaluar exclusión de variable

---

#### Outliers

* Detectar usando método IQR

* Si representan comportamiento válido
  - conservar para análisis

* Si representan errores
  - eliminar o corregir

* Si distorsionan el análisis
  - aplicar winsorization

---

#### Duplicados

* Detectar registros repetidos
* Eliminar duplicados exactos

---

#### Tipos de datos

* Validar variables numéricas y categóricas
* Corregir formatos inconsistentes

### Resultado esperado

* Dataset limpio y consistente
* Variables preparadas para análisis
* Reducción de sesgos analíticos

---

## 2. Exploratory Data Analysis (EDA)

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

## 3. Correlation Analysis

### Objetivo

Identificar relaciones estadísticas significativas entre variables y detectar indicadores de riesgo.

### Responsabilidades

* Matriz completa de correlación
* Relaciones:
  - Uso vs Salud Mental
  - Uso vs Sueño
  - Sueño vs Salud Mental
* Scatter plots con tendencia
* Análisis por subgrupos
* Interpretación automática de correlaciones
* Detección de patrones críticos

### Reglas de interpretación

* |r| > 0.7 → Muy fuerte
* |r| > 0.5 → Fuerte
* |r| > 0.3 → Moderada
* |r| < 0.3 → Débil

---

## 4. Model Selection

### Objetivo

Evaluar diferentes modelos analíticos para seleccionar el enfoque más adecuado en la detección de patrones de riesgo y comportamiento digital.

### Modelos evaluados

#### Regresión Lineal
Objetivo:
- predecir `Mental_Health_Score`

Variables:
- Avg_Daily_Usage_Hours
- Sleep_Hours_Per_Night
- Age

---

#### Árbol de Decisión
Objetivo:
- clasificar niveles de riesgo estudiantil

Variables:
- uso diario
- sueño
- salud mental

---

#### K-Means Clustering
Objetivo:
- segmentar estudiantes según patrones de comportamiento

Variables:
- uso diario
- sueño
- salud mental

---

### Métricas de evaluación

#### Regresión Lineal
* R² Score
* Mean Squared Error (MSE)

#### Árbol de Decisión
* Accuracy
* Precision
* Recall

#### K-Means
* Silhouette Score

---

### Reglas de selección

El agente debe:

* comparar métricas entre modelos
* seleccionar el modelo con mejor desempeño
* priorizar interpretabilidad sobre complejidad
* evitar sobreajuste (overfitting)

### Resultado esperado

* Modelo seleccionado automáticamente
* Métricas comparativas
* Interpretación del rendimiento
* Relación entre modelo y comportamiento estudiantil

---

## 5. Insight Generation

### Objetivo

Transformar resultados estadísticos y métricas de modelos en conclusiones interpretativas y recomendaciones accionables.

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
* Resultados obtenidos por modelos analíticos

---

# Flujo de Ejecución

El agente debe adaptar el flujo analítico según:

* calidad del dataset
* presencia de nulos u outliers
* correlaciones detectadas
* rendimiento de modelos
* riesgos identificados

## Flujo principal

```text
Dataset CSV
   ↓
Data Wrangling Skill
   ↓
EDA Skill
   ↓
Correlation Analysis Skill
   ↓
Model Selection Skill
   ↓
Insight Generation Skill
   ↓
Conclusiones automáticas