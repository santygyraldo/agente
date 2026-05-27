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

* < 5%:
  - eliminar registros faltantes

* 5% – 20%:
  - imputar mediana (numéricos)
  - imputar moda (categóricos)

* > 20%:
  - evaluar exclusión de variable

---

#### Outliers

* Detectar usando método IQR

* Si representan comportamiento válido:
  - conservar para análisis

* Si representan errores:
  - eliminar o corregir

* Si distorsionan el análisis:
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

* Dataset limpio
* Datos consistentes
* Variables preparadas para análisis
* Reducción de sesgos analíticos