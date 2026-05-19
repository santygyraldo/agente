from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

class PredictiveModelingSkill:
    """Skill 3: Modelado Predictivo."""

    def execute(self, df):
        print("[Skill: PredictiveModeling] Entrenando y comparando modelos...")
        if df is None: return None
        
        features = ['Age', 'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 
                    'Mental_Health_Score', 'Affects_Academic_Binary',
                    'Gender_Enc', 'Platform_Enc', 'Level_Enc']
        
        X = df[features]
        y = df['Overall_Impact']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y
        )
        
        # 1. Modelo A: Random Forest
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
        rf_model.fit(X_train, y_train)
        y_pred_rf = rf_model.predict(X_test)
        acc_rf = accuracy_score(y_test, y_pred_rf)
        
        # 2. Modelo B: Regresión Logística
        lr_model = LogisticRegression(max_iter=1000, random_state=42)
        lr_model.fit(X_train, y_train)
        y_pred_lr = lr_model.predict(X_test)
        acc_lr = accuracy_score(y_test, y_pred_lr)
        
        print(f"\n  Comparación de Modelos:")
        print(f"    - Random Forest Accuracy: {acc_rf:.4f}")
        print(f"    - Logistic Regression Accuracy: {acc_lr:.4f}")
        
        # Selección del modelo final con justificación técnica detallada
        if acc_rf >= acc_lr:
            final_model = rf_model
            diff = acc_rf - acc_lr
            reason = (f"Random Forest seleccionado automáticamente. Superó a la Regresión Logística por un margen de {diff:.4f} en accuracy. "
                      "La justificación radica en su capacidad para modelar interacciones no lineales y su resistencia al sobreajuste mediante el uso de múltiples árboles de decisión.")
        else:
            final_model = lr_model
            diff = acc_lr - acc_rf
            reason = (f"Regresión Logística seleccionada automáticamente. Superó al Random Forest por un margen de {diff:.4f} en accuracy. "
                      "La justificación es su mejor capacidad de generalización en este dataset específico, ofreciendo una frontera de decisión lineal más robusta para las variables analizadas.")
            
        print(f"\n  MODELO FINAL SELECCIONADO: {type(final_model).__name__}")
        print(f"  JUSTIFICACIÓN: {reason}")
        print("\n  Reporte de Clasificación (Modelo Final):")
        print(classification_report(y_test, final_model.predict(X_test)))
        
        return final_model, reason
