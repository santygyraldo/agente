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