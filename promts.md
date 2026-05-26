# Prompts Utilizados para el Desarrollo del Proyecto

## Proyecto
Agente Orquestador para Análisis de Impacto de Redes Sociales en Estudiantes

Este documento consolida los prompts utilizados durante el proceso de mejora, optimización y perfeccionamiento técnico del proyecto desarrollado.

---

# 1. Arquitectura del Agente Orquestador

## Prompt Utilizado

Diseñe mejoras sobre la arquitectura ya implementada del agente orquestador encargado de coordinar el pipeline analítico del proyecto.

La arquitectura debe cumplir obligatoriamente con los siguientes requerimientos:

- Implementar un único agente principal responsable de coordinar todo el flujo de ejecución.
- Separar las funcionalidades analíticas en tres habilidades independientes (skills):
  - Preparación de datos
  - Análisis exploratorio de datos (EDA)
  - Modelado predictivo
- Mantener separación clara de responsabilidades entre componentes.
- Evitar lógica analítica directamente dentro del agente principal.
- Garantizar modularidad y reutilización de código.
- Mantener una estructura organizada y escalable del proyecto.
- Centralizar la documentación técnica en el archivo `agente.md`.

---

# 2. Modularización y Refactorización de Skills

## Prompt Utilizado

Refactorice las funcionalidades ya implementadas dentro del proyecto para que cada skill opere de forma independiente dentro de archivos separados.

El ajuste debe cumplir con los siguientes requerimientos:

- Reducir acoplamiento entre componentes.
- Mejorar legibilidad y mantenibilidad del código.
- Organizar funciones según responsabilidad funcional.
- Garantizar compatibilidad con el agente orquestador ya construido.
- Permitir escalabilidad y futuras integraciones.
- Mantener una estructura profesional de carpetas y módulos.

---

# 3. Optimización del Pipeline Analítico

## Prompt Utilizado

Integre mejoras técnicas sobre el pipeline analítico ya desarrollado para fortalecer las etapas de procesamiento, validación y modelado de datos.

El sistema debe cumplir con los siguientes requerimientos:

- Realizar limpieza y transformación de datos.
- Implementar procesos de data wrangling.
- Validar consistencia y calidad de datos.
- Mantener trazabilidad completa del flujo analítico.
- Optimizar el flujo de entrenamiento y validación de modelos.
- Generar datasets preparados para modelado predictivo.

---

# 4. Implementación de Selección Automática de Modelos

## Prompt Utilizado

Implemente un mecanismo automatizado para evaluar, comparar y seleccionar el mejor modelo predictivo dentro del sistema analítico desarrollado.

La implementación debe cumplir con los siguientes requerimientos:

- Comparar múltiples algoritmos de machine learning.
- Evaluar métricas de desempeño relevantes.
- Seleccionar automáticamente el modelo con mejores resultados.
- Generar justificación técnica basada en métricas cuantitativas.
- Mantener registro de resultados obtenidos durante las pruebas.

---

# 5. Mejoras al Análisis Exploratorio de Datos (EDA)

## Prompt Utilizado

Integre funcionalidades avanzadas de análisis exploratorio sobre los módulos analíticos ya implementados dentro del proyecto.

El análisis debe incluir obligatoriamente:

- Detección de outliers.
- Validación de valores nulos (NaN).
- Validación de consistencia de variables.
- Scatter plots.
- Pairplots.
- Matrices de correlación.
- Análisis multivariado.
- Visualizaciones automáticas para interpretación de datos.

---

# 6. Documentación Técnica y Notebook de Ejecución

## Prompt Utilizado

Actualice y complemente la documentación técnica del proyecto incluyendo arquitectura, flujo de ejecución, estructura modular y guía de uso del sistema.

La documentación debe cumplir con los siguientes requerimientos:

- Documentar arquitectura final del agente.
- Explicar responsabilidades de cada skill.
- Describir flujo completo del pipeline analítico.
- Mantener actualizado el archivo `agente.md`.
- Crear notebook Jupyter (`.ipynb`) como guía de ejecución paso a paso.
- Incluir ejemplos de ejecución y resultados obtenidos.

---

# 7. Aplicación de Buenas Prácticas de Desarrollo

## Prompt Utilizado

Refactorice y optimice el proyecto aplicando estándares profesionales de desarrollo para sistemas analíticos basados en agentes.

El proyecto debe cumplir con los siguientes estándares:

- Código limpio y documentado.
- Modularidad y reutilización de componentes.
- Escalabilidad del sistema.
- Manejo de excepciones y validación de errores.
- Separación adecuada de responsabilidades.
- Organización profesional de carpetas y archivos.
- Optimización de mantenibilidad del código.
- Estructura clara para futuras ampliaciones del sistema.

---

# 8. Optimización General del Sistema

## Prompt Utilizado

Realice una revisión técnica general del sistema analítico ya implementado para identificar oportunidades de mejora estructural, funcional y organizacional.

La optimización debe incluir:

- Revisión del flujo del agente orquestador.
- Validación de integración entre skills.
- Optimización de tiempos de ejecución.
- Revisión de consistencia del pipeline.
- Mejora de organización del proyecto.
- Validación final de funcionamiento del sistema completo.

---

# 9. Conversión de Skills Python (.py) a Skills Markdown (.md)

## Prompt Utilizado

Transforme los skills analíticos implementados originalmente en archivos Python (`.py`) hacia una arquitectura basada en documentación modular (`.md`) compatible con Jupyter Notebook y sistemas analíticos orientados por instrucciones.

La conversión debe cumplir obligatoriamente con los siguientes requerimientos:

- Eliminar lógica procedural basada en clases y métodos Python.
- Convertir cada skill en un documento analítico interpretativo.
- Mantener separación clara entre:
  - EDA
  - análisis de correlaciones
  - generación de insights
- Adaptar toda la arquitectura para ejecución directa desde `social_impact_analysis.ipynb`.
- Evitar dependencias de scripts `.py` externos.
- Sustituir lógica hardcodeada por instrucciones analíticas interpretables.
- Mantener compatibilidad conceptual con el agente orquestador documentado en `agent.md`.
- Permitir que el notebook utilice los skills como referencia operativa para ejecutar análisis dinámicos.

La nueva estructura de skills debía incluir:

- Objetivo del análisis
- Variables involucradas
- Pasos analíticos
- Visualizaciones esperadas
- Reglas de interpretación
- Umbrales de decisión
- Insights esperados
- Recomendaciones automáticas

La transformación debía además:

- Optimizar claridad documental.
- Mejorar mantenibilidad del sistema.
- Facilitar reutilización de skills.
- Adaptarse a arquitecturas orientadas a notebooks.
- Mantener un enfoque profesional de Data Science y Analítica.

Los nuevos skills `.md` debían funcionar como:

- especificaciones analíticas
- contexto operativo del notebook
- instrucciones interpretativas
- guía estructurada para ejecución del análisis

sin incluir código ejecutable Python.

---

# 10. Generación del Notebook de Ejecución Analítica

## Prompt Utilizado

Construya un notebook Jupyter profesional (`social_impact_analysis.ipynb`) tomando como referencia el archivo `agent.md` y todos los skills analíticos definidos en la carpeta `skills/`.

El notebook debe funcionar como el agente orquestador principal del sistema analítico y ejecutar todo el flujo de análisis directamente desde Jupyter Notebook, sin depender de scripts `.py` externos.

La implementación debe cumplir obligatoriamente con los siguientes requerimientos:

- Ejecutar todo el análisis directamente dentro del notebook.
- Interpretar conceptualmente las instrucciones contenidas en:
  - `agent.md`
  - `eda_skill.md`
  - `correlation_analysis.md`
  - `insight_generation.md`
- Mantener una estructura modular y profesional orientada a Data Science.
- Organizar el notebook por secciones claramente diferenciadas.
- Mostrar todas las visualizaciones inline dentro de Jupyter Notebook.
- Incluir explicaciones e interpretaciones analíticas en celdas Markdown.

El notebook debía incluir como mínimo las siguientes etapas:

1. Introducción del proyecto
2. Importación de librerías
3. Carga del dataset CSV
4. Vista general del dataset
5. Análisis Exploratorio de Datos (EDA)
6. Análisis de correlaciones
7. Análisis por subgrupos
8. Generación automática de insights
9. Identificación de riesgos
10. Conclusiones finales

Las visualizaciones debían incluir:

- Histogramas
- Heatmaps correlacionales
- Scatter plots
- Boxplots
- Dashboards analíticos
- Comparaciones por categorías

El sistema debía además:

- Detectar patrones relevantes automáticamente.
- Generar conclusiones interpretativas.
- Identificar relaciones entre:
  - uso de redes sociales
  - salud mental
  - horas de sueño
  - impacto académico
- Generar recomendaciones basadas en métricas cuantitativas.

La arquitectura final debía estar completamente orientada a notebooks y basada en skills documentados en archivos `.md`, eliminando dependencias de agentes implementados mediante scripts Python externos.

---
11. Generar notebook completo final

Quiero generar un notebook completo llamado social_impact_analysis.ipynb utilizando Python, pandas, matplotlib y seaborn.

El notebook debe implementar un sistema analítico orientado a agentes basado en un agente orquestador y skills modulares definidos mediante instrucciones .md.

La estructura del notebook debe ser limpia, profesional y organizada mediante secciones markdown y celdas de código claramente separadas.

# Objetivo del Proyecto

Analizar el impacto del uso de redes sociales sobre el bienestar estudiantil utilizando:

* análisis exploratorio de datos (EDA)
* análisis de correlaciones
* generación automática de insights # hayazgos profundos

El notebook debe producir:

* visualizaciones analíticas
* correlaciones relevantes
* alertas automáticas
* insights interpretativos
* recomendaciones basadas en evidencia cuantitativa

# Dataset

Utilizar un dataset CSV relacionado con:

* uso de redes sociales
* salud mental
* horas de sueño
* bienestar estudiantil

Variables principales esperadas:

* Age 
* Avg_Daily_Usage_Hours 
* Sleep_Hours_Per_Night 
* Mental_Health_Score 
* Gender 
* Most_Used_Platform 
* Overall_Impact 

# Estructura del Notebook

El notebook debe contener las siguientes secciones:

1. Introducción del proyecto
2. Importación de librerías
3. Carga y validación del dataset
4. EDA Skill Execution
5. Correlation Analysis Skill Execution
6. Insight Generation Skill Execution
7. Dashboard resumen
8. Conclusiones finales

# Requisitos Técnicos

## Librerías

Usar:

* pandas
* numpy
* matplotlib
* seaborn

## Visualizaciones

Generar:

* histogramas
* heatmaps correlacionales
* boxplots comparativos
* scatter plots con líneas de tendencia
* dashboard resumen en grid 2x2

Las visualizaciones deben ser claras, profesionales y fáciles de interpretar.

# EDA Skill Execution

El notebook debe:

* analizar distribuciones de variables numéricas
* detectar posibles valores atípicos
* identificar patrones iniciales
* comparar grupos por:

  * Gender 
  * Most_Used_Platform 

Agregar markdowns explicativos antes de cada análisis.

# Correlation Analysis Skill Execution

El notebook debe:

* calcular matriz de correlación
* generar heatmap anotado
* analizar relaciones entre:

  * uso de redes sociales y salud mental
  * uso de redes sociales y sueño
  * sueño y salud mental

Agregar scatter plots con líneas de tendencia.

Interpretar correlaciones usando:

* |r| > 0.7 → Muy fuerte
* |r| > 0.5 → Fuerte
* |r| > 0.3 → Moderada
* |r| < 0.3 → Débil

# Alertas Automáticas

El notebook debe generar alertas automáticas si:

* Avg_Daily_Usage_Hours > 6 
* Sleep_Hours_Per_Night < 6 
* Mental_Health_Score < 5 
* correlaciones negativas relevantes < -0.5 

Ejemplo:

``python
if corr_value < -0.5:
    print("⚠️ Posible impacto negativo detectado.")
``

# Insight Generation Skill Execution

El notebook debe:

* generar insights automáticos
* identificar grupos de riesgo
* sintetizar patrones relevantes
* producir recomendaciones interpretativas

Cada insight debe incluir:

* observación
* evidencia cuantitativa
* interpretación contextual

Generar entre 5 y 8 insights automáticos.

# Estilo del Notebook

El notebook debe verse como la ejecución de un agente analítico inteligente y no como código aislado.

Agregar celdas markdown explicativas antes de cada sección importante utilizando lenguaje técnico y profesional.

# Requisitos de Código

* Código limpio y bien comentado
* Uso de funciones cuando sea necesario
* Variables bien nombradas
* Visualizaciones organizadas
* Flujo coherente entre secciones

# Resultado Esperado

Generar un notebook funcional, profesional y listo para sustentación universitaria, mostrando claramente:

* arquitectura orientada a agentes
* ejecución modular basada en skills
* análisis exploratorio
* análisis correlacional
* generación automática de insights