# 🤖 Agente Orquestador: SocialImpact Orchestrator

Este documento describe la arquitectura del agente orquestador diseñado para analizar el impacto de las redes sociales en estudiantes.

---

## 1. Arquitectura del Sistema

El sistema sigue un patrón de **Agente Orquestador con Skills**, donde las responsabilidades están claramente separadas:

### 1.1 Agente Orquestador (`analyzer.py`)
Es el componente principal que coordina el flujo de trabajo. No contiene lógica analítica, sino que invoca a las habilidades (skills) en un orden lógico:
1.  **Preparación**: Invoca a `DataPreparationSkill`.
2.  **Exploración**: Invoca a `EDASkill`.
3.  **Modelado**: Invoca a `PredictiveModelingSkill`.

### 1.2 Skills (`skills.py`)
Son módulos independientes que contienen la lógica específica:

-   **DataPreparationSkill**: Encargada de la carga de archivos, limpieza de nulos, eliminación de duplicados y transformaciones (codificación de variables).
-   **EDASkill**: Encargada de generar visualizaciones estadísticas y análisis de correlación.
-   **PredictiveModelingSkill**: Encargada de entrenar un modelo de Machine Learning (Random Forest) para clasificar el impacto general.

---

## 2. Pipeline de Ejecución

El flujo de datos es explícito y secuencial:

`Data set.csv` ➔ **DataPreparation** ➔ `DataFrame Limpio` ➔ **EDA** ➔ `Insights Visuales` ➔ **PredictiveModeling** ➔ `Modelo & Métricas`

---

## 3. Resultados Analíticos (Entregables)

El sistema genera los siguientes resultados mínimos requeridos:

### 3.1 Dataset Preparado (Data Wrangling)
- **Limpieza automática**: Eliminación de nulos y duplicados.
- **Análisis de NaN**: Reporte detallado de valores faltantes por columna con porcentajes.
- **Validación Rigurosa**:
  - Verificación de rangos de valores (ej: Edad 10-60, Uso 0-24h, Sueño 0-12h, Salud 0-10).
  - Validación de tipos de datos para columnas numéricas.
- **Detección de Outliers**: Identificación de valores atípicos usando método IQR (Interquartile Range) con límites superior e inferior.
- **Transformaciones**: Codificación de variables categóricas (`LabelEncoder`) y creación de variables sintéticas (`Usage_Category`, `Affects_Academic_Binary`).

### 3.2 Evidencia de Análisis Exploratorio (EDA)
Las visualizaciones se exportan automáticamente a la carpeta `analysis_results/`:
- `agente_correlation.png`: Matriz de correlación para identificar relaciones clave.
- `agente_mental_health.png`: Boxplot que muestra el impacto de las plataformas en la salud mental.
- `agente_scatter_plots.png`: 4 scatter plots bivariados (Uso vs Salud Mental, Uso vs Sueño, Sueño vs Salud Mental, Edad vs Uso).
- `agente_pairplot.png`: Pairplot completo con KDE para análisis multivariado de todas las variables numéricas.
- `agente_multivariate.png`: Análisis multivariado por categorías (Uso vs Sueño coloreado por Impacto General, Uso vs Salud Mental coloreado por Género).

### 3.3 Modelado Predictivo
- **Entrenamiento y Prueba**: El sistema divide los datos (75% entrenamiento, 25% prueba) y evalúa múltiples algoritmos.
- **Modelos Comparados**: Random Forest vs. Regresión Logística.
- **Selección de Modelo Final**: Se selecciona el modelo con mejor `accuracy` en el conjunto de prueba.
- **Justificación Técnica**: Random Forest es seleccionado usualmente por su capacidad para capturar interacciones complejas y no lineales entre el tiempo de uso, las horas de sueño y la salud mental, superando a modelos lineales en precisión predictiva.

---

## 4. Requisitos de Instalación

```bash
pip install -r requirements.txt
```

---

## 4. Ejecución

Para iniciar el agente, ejecute:

```bash
python analyzer.py
```

Las visualizaciones resultantes se guardarán automáticamente en la carpeta `analysis_results/`.