"""
SocialImpact Analyzer - Agente de Análisis de Impacto de Redes Sociales en Estudiantes

Arquitectura modular basada en el diseño definido en README.md:
    DataLoader         → Carga del CSV y validación de estructura
    DataCleaner        → Limpieza de datos
    FeatureEngineer    → Transformación de variables
    EDAEngine          → Análisis exploratorio
    CorrelationEngine  → Análisis de correlaciones
    InsightGenerator   → Generación de conclusiones automáticas
    ReportGenerator    → Presentación de resultados
    SocialImpactAnalyzer → Orquestador del pipeline

Dataset: Data set.csv (separado por ";")
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURACIÓN GLOBAL DE VISUALIZACIÓN
# ==============================================================================
plt.rcParams['figure.dpi'] = 100    # Resolución de las figuras
plt.rcParams['savefig.dpi'] = 150   # Resolución de las figuras guardadas
plt.rcParams['font.size'] = 11      # Tamaño de la fuente
sns.set_theme(style="whitegrid", palette="muted")


# ==============================================================================
# UTILIDADES DE FORMATO
# ==============================================================================
def separador(titulo):
    """Imprime un separador principal con el título dado."""
    print(f"\n{'='*70}")    # esto hace que se vea mejor
    print(f"  {titulo}")    
    print(f"{'='*70}\n") # significa que terminó la sección


def subseparador(titulo):
    """Imprime un sub-separador con el título dado."""
    print(f"\n{'─'*50}")
    print(f"  {titulo}")
    print(f"{'─'*50}")


# ==============================================================================
# 1. DATA LOADER - Carga del archivo CSV y validación de estructura
# ==============================================================================
class DataLoader:
    """
    Componente encargado de cargar el dataset desde un archivo CSV
    y validar que la estructura coincida con el esquema esperado.
    """

    # Esquema esperado según el diseño del agente
    EXPECTED_COLUMNS = [
        'Student_ID', 'Age', 'Gender', 'Academic_Level', 'Country',
        'Avg_Daily_Usage_Hours', 'Most_Used_Platform',
        'Affects_Academic_Performance', 'Sleep_Hours_Per_Night',
        'Mental_Health_Score', 'Overall_Impact'
    ]

    def __init__(self, file_path, delimiter=';'):
        self.file_path = file_path
        self.delimiter = delimiter
        self.df = None

    def load(self):
        """
        Carga el dataset desde el archivo CSV usando el delimitador especificado.
        Retorna el DataFrame o None si hay error.
        """
        try:
            self.df = pd.read_csv(self.file_path, sep=self.delimiter)
            print(f"[DataLoader] Dataset cargado exitosamente.")
            print(f"  Filas: {len(self.df)} | Columnas: {len(self.df.columns)}")
            return self.df
        except Exception as e:
            print(f"[DataLoader] Error al cargar el archivo: {e}")
            return None

    def validate(self):
        """
        Valida que el dataset contenga las 11 columnas esperadas
        según el esquema definido en el diseño del agente.
        Retorna True si la validación es exitosa.
        """
        if self.df is None:
            print("[DataLoader] No hay datos cargados para validar.")
            return False

        missing = [col for col in self.EXPECTED_COLUMNS if col not in self.df.columns]
        extra = [col for col in self.df.columns if col not in self.EXPECTED_COLUMNS]

        if not missing:
            print(f"[DataLoader] Validación exitosa. Las 11 columnas esperadas están presentes.")
        else:
            print(f"[DataLoader] Columnas faltantes: {missing}")

        if extra:
            print(f"  Columnas adicionales detectadas: {extra}")

        # Mostrar tipos de datos actuales
        print("\n  Tipos de datos detectados:")
        for col in self.df.columns:
            print(f"    {col}: {self.df[col].dtype}")

        return len(missing) == 0


# ==============================================================================
# 2. DATA CLEANER - Limpieza de datos
# ==============================================================================
class DataCleaner:
    """
    Componente encargado de limpiar los datos:
    eliminación de duplicados, manejo de nulos y conversión de tipos.
    """

    NUMERIC_COLS = ['Age', 'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score']

    def __init__(self, df):
        self.df = df.copy()

    def clean(self):
        """
        Ejecuta el proceso completo de limpieza:
        1. Elimina duplicados.
        2. Elimina filas con valores nulos.
        3. Convierte columnas numéricas al tipo correcto.
        Retorna el DataFrame limpio.
        """
        n_before = len(self.df)

        # Eliminar duplicados
        dupes = self.df.duplicated().sum()
        self.df = self.df.drop_duplicates()

        # Eliminar registros con valores faltantes
        self.df = self.df.dropna()

        # Convertir columnas numéricas
        for col in self.NUMERIC_COLS:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        # Segunda pasada: eliminar NaN generados por conversión fallida
        self.df = self.df.dropna()

        n_after = len(self.df)
        eliminados = n_before - n_after

        print(f"[DataCleaner] Limpieza completada.")
        print(f"  Duplicados eliminados: {dupes}")
        print(f"  Registros eliminados por datos faltantes: {eliminados - dupes}")
        print(f"  Dataset final: {len(self.df)} filas")

        return self.df


# ==============================================================================
# 3. FEATURE ENGINEER - Transformación de variables
# ==============================================================================
class FeatureEngineer:
    """
    Componente encargado de transformar y crear nuevas variables:
    segmentación de uso, codificación binaria y codificación de categóricas.
    """

    def __init__(self, df):
        self.df = df.copy()
        self._le_gender = None
        self._le_platform = None
        self._le_level = None

    def transform(self):
        """
        Ejecuta las transformaciones:
        1. Crea variable Usage_Category (Bajo/Medio/Alto uso).
        2. Codifica Affects_Academic_Performance como binaria.
        3. Codifica variables categóricas con LabelEncoder.
        Retorna el DataFrame transformado.
        """
        # Segmentación de uso: Bajo uso (<4h), Uso medio (4-6h), Alto uso (>6h)
        self.df['Usage_Category'] = pd.cut(
            self.df['Avg_Daily_Usage_Hours'],
            bins=[0, 4, 6, 24],
            labels=['Bajo uso (<4h)', 'Uso medio (4-6h)', 'Alto uso (>6h)'],
            include_lowest=True
        )

        # Codificación binaria: Affects_Academic_Performance (Yes=1, No=0)
        self.df['Affects_Academic_Binary'] = (self.df['Affects_Academic_Performance'] == 'Yes').astype(int)

        # Codificación de variables categóricas para modelos
        self._le_gender = LabelEncoder()
        self._le_platform = LabelEncoder()
        self._le_level = LabelEncoder()
        self.df['Gender_Enc'] = self._le_gender.fit_transform(self.df['Gender'])
        self.df['Platform_Enc'] = self._le_platform.fit_transform(self.df['Most_Used_Platform'])
        self.df['Level_Enc'] = self._le_level.fit_transform(self.df['Academic_Level'])

        print(f"[FeatureEngineer] Transformación completada.")
        print(f"  Nuevas variables: Usage_Category, Affects_Academic_Binary, Gender_Enc, Platform_Enc, Level_Enc")

        return self.df


# ==============================================================================
# 4. EDA ENGINE - Análisis exploratorio de datos
# ==============================================================================
class EDAEngine:
    """
    Componente encargado del análisis exploratorio:
    estadísticas descriptivas, distribuciones, outliers y análisis por categóricas.
    """

    NUMERIC_COLS = ['Age', 'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score']

    def __init__(self, df, output_dir):
        self.df = df
        self.output_dir = output_dir

    def run(self, insight_gen):
        """
        Ejecuta el análisis exploratorio completo y genera insights.
        Recibe un InsightGenerator para registrar hallazgos automáticamente.
        """
        separador("ANALISIS EXPLORATORIO DE DATOS (EDA)")

        self._estadisticas_descriptivas(insight_gen)
        self._distribuciones()
        self._deteccion_outliers()
        self._analisis_categoricas()
        self._tablas_cruzadas(insight_gen)

    def _estadisticas_descriptivas(self, insight_gen):
        """Calcula e imprime estadísticas descriptivas de las variables numéricas."""
        subseparador("Estadísticas Descriptivas Generales")
        desc = self.df[self.NUMERIC_COLS].describe().round(2)
        print(desc.to_string())

        # Interpretación automática
        media_uso = self.df['Avg_Daily_Usage_Hours'].mean()
        media_sueno = self.df['Sleep_Hours_Per_Night'].mean()
        media_sm = self.df['Mental_Health_Score'].mean()
        insight_gen.add(
            f"Se observa que el promedio de uso diario de redes sociales es de {media_uso:.1f} horas, "
            f"el promedio de sueño es de {media_sueno:.1f} horas y el puntaje promedio de salud mental es {media_sm:.1f}/10."
        )

    def _distribuciones(self):
        """Genera histogramas con curva KDE para cada variable numérica."""
        subseparador("Distribución de Variables Numéricas")
        colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        for ax, col, color in zip(axes.flatten(), self.NUMERIC_COLS, colores):
            sns.histplot(self.df[col], kde=True, ax=ax, color=color, edgecolor='white')
            ax.set_title(f'Distribución de {col}', fontsize=13, fontweight='bold')
            ax.axvline(self.df[col].mean(), color='black', linestyle='--',
                       label=f'Media: {self.df[col].mean():.1f}')
            ax.legend()
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/01_histogramas.png")
        plt.close()
        print("  Histogramas guardados: 01_histogramas.png")

    def _deteccion_outliers(self):
        """Genera boxplots y detecta valores atípicos usando el método IQR."""
        subseparador("Detección de Valores Atípicos (Boxplots)")
        colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        for ax, col, color in zip(axes.flatten(), self.NUMERIC_COLS, colores):
            sns.boxplot(x=self.df[col], ax=ax, color=color)
            ax.set_title(f'Boxplot de {col}', fontsize=13, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/02_boxplots.png")
        plt.close()
        print("  Boxplots guardados: 02_boxplots.png")

        # Contar outliers por IQR
        for col in self.NUMERIC_COLS:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.df[col] < Q1 - 1.5 * IQR) | (self.df[col] > Q3 + 1.5 * IQR)).sum()
            if outliers > 0:
                print(f"  {col}: {outliers} valores atípicos detectados")
            else:
                print(f"  {col}: Sin valores atípicos significativos")

    def _analisis_categoricas(self):
        """Analiza la distribución de variables categóricas y genera gráficos."""
        subseparador("Análisis por Variable Categórica")

        # Gender
        print("\n  Distribución por Género:")
        gender_counts = self.df['Gender'].value_counts()
        gender_pct = (gender_counts / len(self.df) * 100).round(1)
        for g, c in gender_counts.items():
            print(f"    {g}: {c} estudiantes ({gender_pct[g]}%)")

        # Academic_Level
        print("\n  Distribución por Nivel Académico:")
        level_counts = self.df['Academic_Level'].value_counts()
        level_pct = (level_counts / len(self.df) * 100).round(1)
        for l, c in level_counts.items():
            print(f"    {l}: {c} estudiantes ({level_pct[l]}%)")

        # Most_Used_Platform
        print("\n  Distribución por Plataforma Más Usada:")
        plat_counts = self.df['Most_Used_Platform'].value_counts()
        plat_pct = (plat_counts / len(self.df) * 100).round(1)
        for p, c in plat_counts.items():
            print(f"    {p}: {c} estudiantes ({plat_pct[p]}%)")

        # Gráfico de variables categóricas
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        sns.countplot(data=self.df, x='Gender', ax=axes[0], palette='Set2')
        axes[0].set_title('Distribución por Género', fontweight='bold')
        sns.countplot(data=self.df, x='Academic_Level', ax=axes[1], palette='Set3')
        axes[1].set_title('Distribución por Nivel Académico', fontweight='bold')
        axes[1].tick_params(axis='x', rotation=30)
        sns.countplot(data=self.df, x='Most_Used_Platform', ax=axes[2], palette='Set1')
        axes[2].set_title('Distribución por Plataforma', fontweight='bold')
        axes[2].tick_params(axis='x', rotation=30)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/03_categoricas.png")
        plt.close()
        print("\n  Gráficos categóricos guardados: 03_categoricas.png")

    def _tablas_cruzadas(self, insight_gen):
        """Genera tablas cruzadas entre variables categóricas clave."""
        subseparador("Tablas Cruzadas (Crosstab)")

        print("\n  Afectación Académica por Género (%):")
        ct1 = pd.crosstab(self.df['Gender'], self.df['Affects_Academic_Performance'], normalize='index') * 100
        print(ct1.round(1).to_string())

        print("\n  Afectación Académica por Nivel Académico (%):")
        ct2 = pd.crosstab(self.df['Academic_Level'], self.df['Affects_Academic_Performance'], normalize='index') * 100
        print(ct2.round(1).to_string())

        print("\n  Impacto General por Plataforma (%):")
        ct3 = pd.crosstab(self.df['Most_Used_Platform'], self.df['Overall_Impact'], normalize='index') * 100
        print(ct3.round(1).to_string())

        print("\n  Impacto General por Categoría de Uso (%):")
        ct4 = pd.crosstab(self.df['Usage_Category'], self.df['Overall_Impact'], normalize='index') * 100
        print(ct4.round(1).to_string())

        # Insight: plataforma con mayor impacto negativo
        neg_por_plat = ct3.get('Negative', pd.Series(0, index=ct3.index))
        plat_mas_neg = neg_por_plat.idxmax()
        insight_gen.add(
            f"La plataforma con mayor porcentaje de impacto negativo es {plat_mas_neg} "
            f"({neg_por_plat[plat_mas_neg]:.1f}% de sus usuarios reportan impacto negativo)."
        )


# ==============================================================================
# 5. CORRELATION ENGINE - Análisis de correlaciones
# ==============================================================================
class CorrelationEngine:
    """
    Componente encargado del análisis de relaciones entre variables:
    matriz de correlación, heatmap, scatter plots y segmentación comparativa.
    """

    def __init__(self, df, output_dir):
        self.df = df
        self.output_dir = output_dir

    def run(self, insight_gen):
        """
        Ejecuta el análisis completo de correlaciones y segmentación.
        Recibe un InsightGenerator para registrar hallazgos automáticamente.
        """
        separador("ANALISIS DE CORRELACIONES")

        self._matriz_correlacion(insight_gen)
        self._uso_vs_rendimiento(insight_gen)
        self._uso_vs_sueno(insight_gen)
        self._uso_vs_salud_mental(insight_gen)
        self._boxplots_impacto()
        self._segmentacion(insight_gen)

    def _interpretar_correlacion(self, r, var1, var2):
        """Interpreta el valor de correlación en lenguaje natural."""
        if abs(r) >= 0.7:
            fuerza = "fuerte"
        elif abs(r) >= 0.4:
            fuerza = "moderada"
        elif abs(r) >= 0.2:
            fuerza = "débil"
        else:
            fuerza = "muy débil o nula"
        direccion = "positiva" if r > 0 else "negativa"
        return f"Existe una correlación {fuerza} {direccion} entre {var1} y {var2} (r={r:.3f})."

    def _matriz_correlacion(self, insight_gen):
        """Calcula y visualiza la matriz de correlación completa."""
        subseparador("Matriz de Correlación Completa")

        numeric_cols = ['Age', 'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night',
                        'Mental_Health_Score', 'Affects_Academic_Binary']
        corr = self.df[numeric_cols].corr().round(3)
        print(corr.to_string())

        # Heatmap
        plt.figure(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, mask=mask,
                    square=True, linewidths=0.5, fmt='.2f', vmin=-1, vmax=1)
        plt.title('Matriz de Correlación entre Variables Numéricas', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/04_heatmap_correlacion.png")
        plt.close()
        print("  Heatmap guardado: 04_heatmap_correlacion.png")

        # Interpretación automática de correlaciones clave
        corr_uso_sueno = self.df['Avg_Daily_Usage_Hours'].corr(self.df['Sleep_Hours_Per_Night'])
        corr_uso_sm = self.df['Avg_Daily_Usage_Hours'].corr(self.df['Mental_Health_Score'])
        corr_sueno_sm = self.df['Sleep_Hours_Per_Night'].corr(self.df['Mental_Health_Score'])
        corr_uso_acad = self.df['Avg_Daily_Usage_Hours'].corr(self.df['Affects_Academic_Binary'])

        insight_gen.add(self._interpretar_correlacion(corr_uso_sueno, "uso de redes", "horas de sueño"))
        insight_gen.add(self._interpretar_correlacion(corr_uso_sm, "uso de redes", "salud mental"))
        insight_gen.add(self._interpretar_correlacion(corr_sueno_sm, "horas de sueño", "salud mental"))
        insight_gen.add(self._interpretar_correlacion(corr_uso_acad, "uso de redes", "afectación académica"))

    def _uso_vs_rendimiento(self, insight_gen):
        """Analiza la relación entre uso de redes y rendimiento académico."""
        subseparador("Uso de Redes vs Rendimiento Académico")

        uso_si = self.df[self.df['Affects_Academic_Performance'] == 'Yes']['Avg_Daily_Usage_Hours']
        uso_no = self.df[self.df['Affects_Academic_Performance'] == 'No']['Avg_Daily_Usage_Hours']

        tabla_acad = pd.DataFrame({
            'Afecta Sí': uso_si.describe().round(2),
            'Afecta No': uso_no.describe().round(2)
        })
        print(tabla_acad.to_string())
        print(f"\n  Promedio de uso (Afecta Sí): {uso_si.mean():.2f} horas")
        print(f"  Promedio de uso (Afecta No): {uso_no.mean():.2f} horas")
        print(f"  Diferencia: {abs(uso_si.mean() - uso_no.mean()):.2f} horas")

        insight_gen.add(
            f"Los estudiantes que reportan que las redes afectan su rendimiento académico "
            f"tienen un promedio de uso de {uso_si.mean():.1f} horas, frente a {uso_no.mean():.1f} horas "
            f"de quienes no reportan afectación."
        )

        # Scatter plot con línea de tendencia
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=self.df, x='Avg_Daily_Usage_Hours', y='Affects_Academic_Binary',
                        hue='Overall_Impact', ax=ax, s=80, alpha=0.7)
        sns.regplot(data=self.df, x='Avg_Daily_Usage_Hours', y='Affects_Academic_Binary',
                    scatter=False, color='red', ax=ax)
        ax.set_title('Uso Diario de Redes vs Afectación Académica', fontsize=13, fontweight='bold')
        ax.set_ylabel('Afecta Rendimiento (0=No, 1=Yes)')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/05_uso_vs_rendimiento.png")
        plt.close()
        print("  Gráfico guardado: 05_uso_vs_rendimiento.png")

    def _uso_vs_sueno(self, insight_gen):
        """Analiza la relación entre uso de redes y horas de sueño."""
        subseparador("Uso de Redes vs Horas de Sueño")

        corr = self.df['Avg_Daily_Usage_Hours'].corr(self.df['Sleep_Hours_Per_Night'])

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.regplot(data=self.df, x='Avg_Daily_Usage_Hours', y='Sleep_Hours_Per_Night',
                    scatter_kws={'alpha': 0.5, 's': 60}, line_kws={'color': 'red'})
        ax.set_title('Relación: Uso Diario de Redes vs Horas de Sueño', fontsize=13, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/06_uso_vs_sueno.png")
        plt.close()
        print("  Gráfico guardado: 06_uso_vs_sueno.png")

        if corr < -0.3:
            insight_gen.add(
                f"Se observa una relación negativa considerable: a mayor uso de redes sociales, "
                f"menores horas de sueño (r={corr:.3f}). Esto sugiere que el tiempo en redes "
                f"desplaza horas de descanso nocturno."
            )
        elif corr < 0:
            insight_gen.add(
                f"Se observa una tendencia negativa leve entre uso de redes y horas de sueño "
                f"(r={corr:.3f}), aunque la relación no es muy fuerte."
            )

    def _uso_vs_salud_mental(self, insight_gen):
        """Analiza la relación entre uso de redes y salud mental."""
        subseparador("Uso de Redes vs Salud Mental")

        corr = self.df['Avg_Daily_Usage_Hours'].corr(self.df['Mental_Health_Score'])

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=self.df, x='Avg_Daily_Usage_Hours', y='Mental_Health_Score',
                        hue='Overall_Impact', s=80, alpha=0.7)
        sns.regplot(data=self.df, x='Avg_Daily_Usage_Hours', y='Mental_Health_Score',
                    scatter=False, color='red')
        ax.set_title('Relación: Uso Diario de Redes vs Puntaje de Salud Mental', fontsize=13, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/07_uso_vs_salud_mental.png")
        plt.close()
        print("  Gráfico guardado: 07_uso_vs_salud_mental.png")

        if corr < -0.3:
            insight_gen.add(
                f"Existe una relación negativa significativa entre el uso de redes y la salud mental "
                f"(r={corr:.3f}). Los estudiantes con mayor uso tienden a reportar puntajes "
                f"más bajos de bienestar psicológico."
            )

    def _boxplots_impacto(self):
        """Genera boxplots comparativos por impacto general y por plataforma."""
        subseparador("Boxplots Comparativos por Impacto General")

        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        sns.boxplot(data=self.df, x='Overall_Impact', y='Avg_Daily_Usage_Hours', ax=axes[0], palette='Set2')
        axes[0].set_title('Uso Diario por Impacto', fontweight='bold')
        sns.boxplot(data=self.df, x='Overall_Impact', y='Sleep_Hours_Per_Night', ax=axes[1], palette='Set2')
        axes[1].set_title('Horas de Sueño por Impacto', fontweight='bold')
        sns.boxplot(data=self.df, x='Overall_Impact', y='Mental_Health_Score', ax=axes[2], palette='Set2')
        axes[2].set_title('Salud Mental por Impacto', fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/08_boxplots_impacto.png")
        plt.close()
        print("  Gráfico guardado: 08_boxplots_impacto.png")

        # Boxplot de salud mental por plataforma
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=self.df, x='Most_Used_Platform', y='Mental_Health_Score', palette='Set3')
        plt.title('Salud Mental por Plataforma Más Usada', fontsize=13, fontweight='bold')
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/09_salud_mental_plataforma.png")
        plt.close()
        print("  Gráfico guardado: 09_salud_mental_plataforma.png")

    def _segmentacion(self, insight_gen):
        """Compara indicadores entre grupos de uso (Bajo/Medio/Alto)."""
        subseparador("Segmentación: Comparación por Nivel de Uso")

        seg_table = self.df.groupby('Usage_Category', observed=True).agg(
            N_Estudiantes=('Student_ID', 'count'),
            Promedio_Uso=('Avg_Daily_Usage_Hours', 'mean'),
            Promedio_Sueno=('Sleep_Hours_Per_Night', 'mean'),
            Promedio_Salud_Mental=('Mental_Health_Score', 'mean'),
            Pct_Afecta_Academico=('Affects_Academic_Binary', 'mean'),
            Edad_Promedio=('Age', 'mean')
        ).round(2)

        seg_table['Pct_Afecta_Academico'] = (seg_table['Pct_Afecta_Academico'] * 100).round(1)
        seg_table = seg_table.rename(columns={
            'N_Estudiantes': 'N° Estudiantes',
            'Promedio_Uso': 'Uso Diario (h)',
            'Promedio_Sueno': 'Sueño (h)',
            'Promedio_Salud_Mental': 'Salud Mental',
            'Pct_Afecta_Academico': '% Afecta Académico',
            'Edad_Promedio': 'Edad Prom.'
        })
        print(seg_table.to_string())

        # Impacto por categoría
        print("\n  Distribución de Impacto General por Categoría de Uso (%):")
        impact_table = pd.crosstab(self.df['Usage_Category'], self.df['Overall_Impact'], normalize='index') * 100
        print(impact_table.round(1).to_string())

        # Insight comparativo
        alto_uso = self.df[self.df['Usage_Category'] == 'Alto uso (>6h)']
        bajo_uso = self.df[self.df['Usage_Category'].astype(str).str.contains('Bajo')]
        if len(alto_uso) > 0 and len(bajo_uso) > 0:
            diff_sm = bajo_uso['Mental_Health_Score'].mean() - alto_uso['Mental_Health_Score'].mean()
            diff_sueno = bajo_uso['Sleep_Hours_Per_Night'].mean() - alto_uso['Sleep_Hours_Per_Night'].mean()
            insight_gen.add(
                f"Los estudiantes con alto uso (>6h) duermen en promedio {diff_sueno:.1f} horas menos "
                f"y tienen un puntaje de salud mental {diff_sm:.1f} puntos más bajo que los de bajo uso (<4h)."
            )

        # Visualización de segmentación
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        cat_order = ['Bajo uso (<4h)', 'Uso medio (4-6h)', 'Alto uso (>6h)']

        sns.barplot(data=self.df, x='Usage_Category', y='Avg_Daily_Usage_Hours',
                    ax=axes[0], order=cat_order, palette='Blues_d', errorbar=None)
        axes[0].set_title('Promedio de Uso por Grupo', fontweight='bold')
        axes[0].tick_params(axis='x', rotation=15)

        sns.barplot(data=self.df, x='Usage_Category', y='Mental_Health_Score',
                    ax=axes[1], order=cat_order, palette='Reds_d', errorbar=None)
        axes[1].set_title('Salud Mental por Grupo', fontweight='bold')
        axes[1].tick_params(axis='x', rotation=15)

        sns.barplot(data=self.df, x='Usage_Category', y='Sleep_Hours_Per_Night',
                    ax=axes[2], order=cat_order, palette='Greens_d', errorbar=None)
        axes[2].set_title('Horas de Sueño por Grupo', fontweight='bold')
        axes[2].tick_params(axis='x', rotation=15)

        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/10_segmentacion.png")
        plt.close()
        print("  Gráfico guardado: 10_segmentacion.png")

        # Tabla cruzada por género y nivel académico
        print("\n  Promedio de uso diario por Género y Nivel Académico:")
        cross_mean = self.df.pivot_table(
            values='Avg_Daily_Usage_Hours', index='Academic_Level',
            columns='Gender', aggfunc='mean'
        ).round(2)
        print(cross_mean.to_string())

        print("\n  Promedio de salud mental por Género y Nivel Académico:")
        cross_sm = self.df.pivot_table(
            values='Mental_Health_Score', index='Academic_Level',
            columns='Gender', aggfunc='mean'
        ).round(2)
        print(cross_sm.to_string())


# ==============================================================================
# 6. INSIGHT GENERATOR - Generación de conclusiones automáticas
# ==============================================================================
class InsightGenerator:
    """
    Componente encargado de recopilar y presentar insights automáticos
    generados durante el análisis, en español.
    """

    def __init__(self):
        self.insights = []

    def add(self, texto):
        """Agrega un insight y lo imprime inmediatamente."""
        self.insights.append(texto)
        print(f"  INSIGHT: {texto}\n")

    def show_all(self):
        """Muestra todos los insights recopilados en una sección consolidada."""
        separador("INSIGHTS AUTOMATICOS GENERADOS")
        for i, insight in enumerate(self.insights, 1):
            print(f"  {i}. {insight}\n")

    def count(self):
        """Retorna la cantidad de insights generados."""
        return len(self.insights)


# ==============================================================================
# 7. REPORT GENERATOR - Presentación de resultados
# ==============================================================================
class ReportGenerator:
    """
    Componente encargado de generar las tablas resumen finales
    y las conclusiones del análisis.
    """

    def __init__(self, df, insight_gen):
        self.df = df
        self.insight_gen = insight_gen

    def run(self):
        """Ejecuta la generación completa de reportes."""
        self._tablas_finales()
        self._clustering()
        self._modelo_predictivo()
        self._conclusiones()

    def _tablas_finales(self):
        """Genera las tablas resumen comparativas finales."""
        separador("RESULTADOS - TABLAS RESUMEN FINALES")

        # Tabla 1: Uso de redes vs Rendimiento académico
        subseparador("Tabla 1: Uso de Redes vs Rendimiento Académico")
        t1 = self.df.groupby('Affects_Academic_Performance').agg(
            N=('Student_ID', 'count'),
            Uso_Promedio=('Avg_Daily_Usage_Hours', 'mean'),
            Sueno_Promedio=('Sleep_Hours_Per_Night', 'mean'),
            Salud_Mental_Prom=('Mental_Health_Score', 'mean')
        ).round(2)
        print(t1.to_string())

        # Tabla 2: Uso vs Salud Mental por Categoría de Uso
        subseparador("Tabla 2: Uso vs Salud Mental por Categoría de Uso")
        t2 = self.df.groupby('Usage_Category', observed=True).agg(
            N=('Student_ID', 'count'),
            Uso_Promedio=('Avg_Daily_Usage_Hours', 'mean'),
            Salud_Mental_Prom=('Mental_Health_Score', 'mean'),
            Sueno_Promedio=('Sleep_Hours_Per_Night', 'mean')
        ).round(2)
        print(t2.to_string())

        # Tabla 3: Impacto por Plataforma
        subseparador("Tabla 3: Impacto por Plataforma")
        t3 = self.df.groupby('Most_Used_Platform').agg(
            N=('Student_ID', 'count'),
            Uso_Promedio=('Avg_Daily_Usage_Hours', 'mean'),
            Salud_Mental_Prom=('Mental_Health_Score', 'mean'),
            Sueno_Promedio=('Sleep_Hours_Per_Night', 'mean'),
            Pct_Negativo=('Overall_Impact', lambda x: (x == 'Negative').mean() * 100)
        ).round(2)
        t3 = t3.rename(columns={'Pct_Negativo': '% Impacto Negativo'})
        print(t3.to_string())

        # Tabla 4: Impacto por Tipo de Estudiante
        subseparador("Tabla 4: Impacto por Tipo de Estudiante (Género x Nivel Académico)")
        t4 = self.df.pivot_table(
            values='Mental_Health_Score', index='Academic_Level',
            columns='Gender', aggfunc='mean'
        ).round(2)
        print(t4.to_string())

        print("\n  Distribución de Impacto General por Género (%):")
        t4b = pd.crosstab(self.df['Gender'], self.df['Overall_Impact'], normalize='index') * 100
        print(t4b.round(1).to_string())

    def _clustering(self):
        """Aplica K-Means para identificar perfiles de estudiantes."""
        subseparador("Clustering K-Means: Identificación de Perfiles de Estudiantes")

        features_cluster = ['Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score']
        X = self.df[features_cluster].copy()

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Método del codo
        inertias = []
        K_range = range(2, 7)
        for k in K_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            km.fit(X_scaled)
            inertias.append(km.inertia_)

        output_dir = "analysis_results"
        plt.figure(figsize=(8, 5))
        plt.plot(K_range, inertias, 'bo-', linewidth=2, markersize=8)
        plt.xlabel('Número de Clusters (K)')
        plt.ylabel('Inercia')
        plt.title('Método del Codo para K Óptimo', fontsize=13, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/11_metodo_codo.png")
        plt.close()
        print("  Gráfico del codo guardado: 11_metodo_codo.png")

        # Aplicar K=3
        k_optimo = 3
        kmeans = KMeans(n_clusters=k_optimo, random_state=42, n_init=10)
        self.df['Cluster'] = kmeans.fit_predict(X_scaled)

        # Describir clusters
        print(f"\n  Características de cada Cluster (K={k_optimo}):")
        cluster_summary = self.df.groupby('Cluster')[features_cluster].mean().round(2)
        cluster_counts = self.df['Cluster'].value_counts().sort_index()

        # Asignar nombres interpretativos
        cluster_names = {}
        for c in range(k_optimo):
            row = cluster_summary.loc[c]
            uso = row['Avg_Daily_Usage_Hours']
            sm = row['Mental_Health_Score']
            if uso > 5 and sm < 6:
                nombre = "Alto Riesgo"
            elif uso < 4 and sm > 7:
                nombre = "Bajo Riesgo"
            else:
                nombre = "Riesgo Moderado"
            cluster_names[c] = nombre

        cluster_summary['N_Estudiantes'] = cluster_counts
        cluster_summary['Perfil'] = cluster_summary.index.map(cluster_names)
        print(cluster_summary.to_string())

        # Visualización de clusters
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        scatter1 = axes[0].scatter(
            self.df['Avg_Daily_Usage_Hours'], self.df['Mental_Health_Score'],
            c=self.df['Cluster'], cmap='Set1', alpha=0.6, s=60, edgecolors='white'
        )
        axes[0].set_xlabel('Uso Diario (horas)')
        axes[0].set_ylabel('Salud Mental')
        axes[0].set_title('Clusters: Uso vs Salud Mental', fontweight='bold')
        legend1 = axes[0].legend(*scatter1.legend_elements(), title='Cluster')
        axes[0].add_artist(legend1)

        scatter2 = axes[1].scatter(
            self.df['Avg_Daily_Usage_Hours'], self.df['Sleep_Hours_Per_Night'],
            c=self.df['Cluster'], cmap='Set1', alpha=0.6, s=60, edgecolors='white'
        )
        axes[1].set_xlabel('Uso Diario (horas)')
        axes[1].set_ylabel('Horas de Sueño')
        axes[1].set_title('Clusters: Uso vs Sueño', fontweight='bold')
        legend2 = axes[1].legend(*scatter2.legend_elements(), title='Cluster')
        axes[1].add_artist(legend2)

        plt.tight_layout()
        plt.savefig(f"{output_dir}/12_clusters.png")
        plt.close()
        print("  Gráfico de clusters guardado: 12_clusters.png")

        # Insights de clustering
        for c, nombre in cluster_names.items():
            row = cluster_summary.loc[c]
            n = int(row['N_Estudiantes'])
            self.insight_gen.add(
                f"Cluster {c} ({nombre}): {n} estudiantes con uso promedio de "
                f"{row['Avg_Daily_Usage_Hours']:.1f}h, sueño de "
                f"{row['Sleep_Hours_Per_Night']:.1f}h y salud mental de "
                f"{row['Mental_Health_Score']:.1f}/10."
            )

    def _modelo_predictivo(self):
        """Aplica un modelo de clasificación para predecir el impacto general."""
        subseparador("Modelo Predictivo: Clasificación de Impacto General")

        features_model = ['Age', 'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night',
                          'Mental_Health_Score', 'Affects_Academic_Binary',
                          'Gender_Enc', 'Platform_Enc', 'Level_Enc']
        X_model = self.df[features_model].copy()
        y = self.df['Overall_Impact']

        X_train, X_test, y_train, y_test = train_test_split(
            X_model, y, test_size=0.25, random_state=42, stratify=y
        )

        clf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)

        accuracy = (y_pred == y_test).mean()
        print(f"\n  Precisión del modelo: {accuracy:.1%}")
        print(f"\n  Reporte de Clasificación:")
        print(classification_report(y_test, y_pred))

        # Importancia de variables
        importances = pd.Series(clf.feature_importances_, index=X_model.columns).sort_values(ascending=False)
        print("  Importancia de Variables en el Modelo:")
        for feat, imp in importances.items():
            bar = '█' * int(imp * 50)
            print(f"    {feat:35s} {imp:.3f} {bar}")

        # Visualización
        output_dir = "analysis_results"
        plt.figure(figsize=(10, 6))
        importances.plot(kind='barh', color='steelblue')
        plt.title('Importancia de Variables para Predecir Impacto General', fontsize=13, fontweight='bold')
        plt.xlabel('Importancia')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(f"{output_dir}/13_importancia_variables.png")
        plt.close()
        print("  Gráfico guardado: 13_importancia_variables.png")

        top_feat = importances.index[0]
        top_imp = importances.iloc[0]
        self.insight_gen.add(
            f"El modelo de clasificación logra una precisión del {accuracy:.0%}. "
            f"La variable más importante para predecir el impacto general es '{top_feat}' "
            f"(importancia: {top_imp:.3f}), lo que indica que esta variable es clave "
            f"para determinar si el uso de redes tiene un efecto positivo, neutral o negativo."
        )

    def _conclusiones(self):
        """Genera las conclusiones finales basadas en todo el análisis."""
        separador("CONCLUSIONES")

        # Recopilar datos clave
        media_uso = self.df['Avg_Daily_Usage_Hours'].mean()
        media_sueno = self.df['Sleep_Hours_Per_Night'].mean()
        media_sm = self.df['Mental_Health_Score'].mean()
        corr_uso_sueno = self.df['Avg_Daily_Usage_Hours'].corr(self.df['Sleep_Hours_Per_Night'])
        corr_uso_sm = self.df['Avg_Daily_Usage_Hours'].corr(self.df['Mental_Health_Score'])
        pct_afecta = (self.df['Affects_Academic_Performance'] == 'Yes').mean() * 100
        pct_neg = (self.df['Overall_Impact'] == 'Negative').mean() * 100
        alto_uso = self.df[self.df['Usage_Category'] == 'Alto uso (>6h)']
        bajo_uso = self.df[self.df['Usage_Category'].astype(str).str.contains('Bajo')]

        # Conclusiones generales
        print("  CONCLUSIONES GENERALES:\n")
        print(f"    1. El promedio de uso diario de redes sociales entre los estudiantes")
        print(f"       analizados es de {media_uso:.1f} horas, lo cual representa una porción")
        print(f"       significativa del día y sugiere un alto nivel de dependencia digital.\n")
        print(f"    2. El {pct_afecta:.1f}% de los estudiantes reporta que el uso de redes sociales")
        print(f"       afecta negativamente su rendimiento académico, y el {pct_neg:.1f}%")
        print(f"       percibe un impacto general negativo.\n")
        print(f"    3. Existe una correlación de r={corr_uso_sueno:.3f} entre el uso de redes")
        print(f"       y las horas de sueño, indicando que a mayor tiempo en redes, menor")
        print(f"       descanso nocturno, lo cual puede comprometer la capacidad cognitiva.\n")
        print(f"    4. La correlación entre uso de redes y salud mental es de r={corr_uso_sm:.3f},")
        print(f"       lo que sugiere que el uso excesivo de redes se asocia con puntajes")
        print(f"       más bajos de bienestar psicológico.\n")

        # Hallazgos clave
        print("\n  HALLAZGOS CLAVE:\n")
        if len(alto_uso) > 0 and len(bajo_uso) > 0:
            diff_sm = bajo_uso['Mental_Health_Score'].mean() - alto_uso['Mental_Health_Score'].mean()
            diff_sueno = bajo_uso['Sleep_Hours_Per_Night'].mean() - alto_uso['Sleep_Hours_Per_Night'].mean()
            print(f"    1. Los estudiantes con alto uso (>6h diarias) presentan en promedio")
            print(f"       {diff_sm:.1f} puntos menos en salud mental y {diff_sueno:.1f} horas")
            print(f"       menos de sueño que los de bajo uso (<4h).\n")

        neg_por_plat = self.df.groupby('Most_Used_Platform')['Overall_Impact'].apply(
            lambda x: (x == 'Negative').mean()
        )
        plat_mas_riesgo = neg_por_plat.idxmax()
        pct_riesgo = neg_por_plat.max() * 100
        print(f"    2. La plataforma {plat_mas_riesgo} presenta la mayor proporción")
        print(f"       de impacto negativo ({pct_riesgo:.1f}%), lo que podría estar")
        print(f"       relacionado con el tipo de contenido y la forma de interacción")
        print(f"       que promueve dicha plataforma.\n")

        corr_sueno_sm = self.df['Sleep_Hours_Per_Night'].corr(self.df['Mental_Health_Score'])
        print(f"    3. La correlación entre horas de sueño y salud mental es de r={corr_sueno_sm:.3f},")
        print(f"       confirmando que el descanso adecuado es un factor protector")
        print(f"       para el bienestar psicológico estudiantil.\n")

        # Implicaciones académicas
        print("\n  IMPLICACIONES ACADÉMICAS:\n")
        print(f"    1. Las instituciones educativas deberían implementar programas de")
        print(f"       educación digital que promuevan un uso consciente y limitado de redes.\n")
        print(f"    2. Los resultados sugieren que reducir el uso de redes por debajo de")
        print(f"       4 horas diarias podría mejorar significativamente tanto el rendimiento")
        print(f"       académico como la salud mental de los estudiantes.\n")
        print(f"    3. Es fundamental abordar la relación entre uso de redes y sueño,")
        print(f"       ya que la privación de descanso tiene efectos documentados sobre")
        print(f"       la concentración, la memoria y el aprendizaje.\n")

        # Recomendaciones
        print("\n  RECOMENDACIONES BASADAS EN DATOS:\n")
        print(f"    1. Establecer límites de uso diario: los datos sugieren que menos de")
        print(f"       4 horas diarias se asocian con mejores indicadores en todas las áreas.\n")
        print(f"    2. Fomentar hábitos de sueño saludables: evitar el uso de redes antes")
        print(f"       de dormir para garantizar al menos 7-8 horas de descanso.\n")
        print(f"    3. Prestar atención especial a los usuarios de plataformas con mayor")
        print(f"       impacto negativo ({plat_mas_riesgo}), implementando estrategias de")
        print(f"       intervención temprana.\n")
        print(f"    4. Realizar seguimiento periódico del bienestar estudiantil mediante")
        print(f"       encuestas similares para evaluar la efectividad de las medidas adoptadas.\n")
        print(f"    5. Considerar la integración de herramientas de bienestar digital en los")
        print(f"       programas institucionales de apoyo estudiantil.\n")


# ==============================================================================
# 8. SOCIAL IMPACT ANALYZER - Orquestador del pipeline
# ==============================================================================
class SocialImpactAnalyzer:
    """
    Agente orquestador que coordina todos los componentes del sistema
    siguiendo el pipeline definido en el diseño:

    1. Carga del archivo CSV (DataLoader)
    2. Validación de estructura (DataLoader)
    3. Limpieza de datos (DataCleaner)
    4. Transformación de variables (FeatureEngineer)
    5. Análisis exploratorio (EDAEngine)
    6. Análisis de correlaciones (CorrelationEngine)
    7. Generación de insights (InsightGenerator)
    8. Creación de reportes (ReportGenerator)
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.output_dir = "analysis_results"
        self.df = None
        self.insight_gen = InsightGenerator()

        # Crear carpeta de resultados si no existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def run(self):
        """
        Ejecuta el pipeline completo del agente. # pipeline es el proceso completo que se ejecuta al iniciar el programa
        """
        separador("AGENTE: ANALISIS DE IMPACTO DE REDES SOCIALES EN ESTUDIANTES")

        # Paso 1: Carga del archivo CSV
        loader = DataLoader(self.file_path, delimiter=';') # delimiter es el separador de columnas
        self.df = loader.load() # carga el archivo CSV
        if self.df is None: # si no se carga el archivo
            return 

        # Paso 2: Validación de estructura
        loader.validate() # valida la estructura del archivo

        # Paso 3: Limpieza de datos
        cleaner = DataCleaner(self.df) # crea el objeto DataCleaner
        self.df = cleaner.clean() # limpia el archivo

        # Paso 4: Transformación de variables
        engineer = FeatureEngineer(self.df) # crea el objeto FeatureEngineer
        self.df = engineer.transform() # transforma las variables

        # Paso 5: Análisis exploratorio (EDA)
        eda = EDAEngine(self.df, self.output_dir) # crea el objeto EDAEngine
        eda.run(self.insight_gen) # ejecuta el análisis exploratorio

        # Paso 6: Análisis de correlaciones
        correlation = CorrelationEngine(self.df, self.output_dir) # crea el objeto CorrelationEngine
        correlation.run(self.insight_gen) # ejecuta el análisis de correlaciones

        # Paso 7: Generación de insights  # insights son las conclusiones del análisis
        self.insight_gen.show_all()

        # Paso 8: Creación de reportes
        reporter = ReportGenerator(self.df, self.insight_gen)
        reporter.run()

        # Resumen final
        separador("ANALISIS COMPLETADO")
        print(f"  Visualizaciones guardadas en: '{self.output_dir}/'")
        print(f"  Total de gráficos generados: 13")
        print(f"  Total de insights generados: {self.insight_gen.count()}")
        print(f"\n  Analisis finalizado exitosamente.\n")


# ==============================================================================
# PUNTO DE ENTRADA
# ==============================================================================
if __name__ == "__main__":
    analyzer = SocialImpactAnalyzer('Data set.csv')
    analyzer.run()
