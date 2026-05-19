import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

class DataPreparationSkill:
    """Skill 1: Preparación y Limpieza de Datos."""
    
    def __init__(self):
        self.numeric_cols = ['Age', 'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score']
        self.expected_columns = [
            'Student_ID', 'Age', 'Gender', 'Academic_Level', 'Country',
            'Avg_Daily_Usage_Hours', 'Most_Used_Platform',
            'Affects_Academic_Performance', 'Sleep_Hours_Per_Night',
            'Mental_Health_Score', 'Overall_Impact'
        ]

    def _detect_outliers_iqr(self, df, col):
        """Detecta outliers usando el método IQR."""
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        return outliers, lower_bound, upper_bound

    def _validate_rigorous(self, df):
        """Validación rigurosa: rangos, tipos, valores nulos."""
        print("\n  [Validación Rigurosa]")
        
        # Validación de rangos
        validations = {
            'Age': (10, 60),
            'Avg_Daily_Usage_Hours': (0, 24),
            'Sleep_Hours_Per_Night': (0, 12),
            'Mental_Health_Score': (0, 10)
        }
        
        for col, (min_val, max_val) in validations.items():
            if col in df.columns:
                invalid = ((df[col] < min_val) | (df[col] > max_val)).sum()
                if invalid > 0:
                    print(f"    ⚠ {col}: {invalid} valores fuera de rango [{min_val}, {max_val}]")
                else:
                    print(f"    ✓ {col}: Todos los valores en rango válido")
        
        # Validación de tipos
        for col in self.numeric_cols:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    print(f"    ⚠ {col}: Tipo incorrecto ({df[col].dtype})")
                else:
                    print(f"    ✓ {col}: Tipo numérico correcto")

    def _analyze_nan(self, df):
        """Análisis detallado de valores NaN."""
        print("\n  [Análisis de NaN]")
        nan_counts = df.isnull().sum()
        total_cells = df.shape[0] * df.shape[1]
        total_nan = nan_counts.sum()
        nan_percentage = (total_nan / total_cells) * 100
        
        print(f"    Total de NaN: {total_nan} ({nan_percentage:.2f}% del dataset)")
        
        if total_nan > 0:
            print("    NaN por columna:")
            for col, count in nan_counts[nan_counts > 0].items():
                col_pct = (count / len(df)) * 100
                print(f"      - {col}: {count} ({col_pct:.2f}%)")
        else:
            print("    ✓ No se detectaron valores NaN")

    def execute(self, file_path):
        print("[Skill: DataPreparation] Cargando y limpiando datos...")
        try:
            df = pd.read_csv(file_path, sep=';')
            
            # Validación básica de columnas
            missing = [col for col in self.expected_columns if col not in df.columns]
            if missing:
                raise ValueError(f"Faltan columnas: {missing}")

            # Análisis de NaN antes de limpieza
            self._analyze_nan(df)
            
            # Validación rigurosa
            self._validate_rigorous(df)
            
            # Detección de outliers antes de limpieza
            print("\n  [Detección de Outliers (IQR)]")
            for col in self.numeric_cols:
                if col in df.columns:
                    outliers, lower, upper = self._detect_outliers_iqr(df, col)
                    if outliers > 0:
                        print(f"    {col}: {outliers} outliers detectados (límites: [{lower:.2f}, {upper:.2f}])")
                    else:
                        print(f"    {col}: Sin outliers significativos")

            # Limpieza
            df = df.drop_duplicates().dropna()
            
            for col in self.numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df = df.dropna()
            
            # Transformaciones iniciales
            df['Usage_Category'] = pd.cut(
                df['Avg_Daily_Usage_Hours'],
                bins=[0, 4, 6, 24],
                labels=['Bajo uso', 'Uso medio', 'Alto uso'],
                include_lowest=True
            )
            df['Affects_Academic_Binary'] = (df['Affects_Academic_Performance'] == 'Yes').astype(int)
            
            le = LabelEncoder()
            df['Gender_Enc'] = le.fit_transform(df['Gender'])
            df['Platform_Enc'] = le.fit_transform(df['Most_Used_Platform'])
            df['Level_Enc'] = le.fit_transform(df['Academic_Level'])
            
            print(f"\n  Finalizado: {len(df)} registros listos.")
            return df
        except Exception as e:
            print(f"  Error en DataPreparation: {e}")
            return None
