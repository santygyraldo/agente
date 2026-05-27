## 4. Model Selection

### Objetivo

Evaluar diferentes modelos analíticos para identificar el enfoque más adecuado en la detección de patrones de riesgo y comportamiento digital estudiantil.

### Modelos evaluados

#### 1. Regresión Lineal
Objetivo:
- predecir `Mental_Health_Score`

Variables:
- Avg_Daily_Usage_Hours
- Sleep_Hours_Per_Night
- Age

---

#### 2. Árbol de Decisión
Objetivo:
- clasificar niveles de riesgo estudiantil

Criterios:
- uso elevado
- privación de sueño
- deterioro de salud mental

---

#### 3. K-Means Clustering
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

---

### Resultado esperado

* Modelo seleccionado automáticamente
* Métricas comparativas
* Interpretación del rendimiento
* Relación entre modelo y comportamiento estudiantil