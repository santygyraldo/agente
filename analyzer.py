"""
Agente Orquestador: SocialImpact Orchestrator
Este archivo coordina el pipeline de análisis de impacto de redes sociales
utilizando skills modulares definidas en skills.py.
"""

from skill_preparation import DataPreparationSkill
from skill_eda import EDASkill
from skill_modeling import PredictiveModelingSkill
import os

class SocialImpactOrchestrator:
    """
    Agente Principal (Orquestador).
    Maneja el flujo de ejecución delegando la lógica a las skills.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        # Inicialización de Skills
        self.data_prep = DataPreparationSkill()
        self.eda = EDASkill()
        self.modeling = PredictiveModelingSkill()
        
        self.data = None
        self.model = None

    def run_pipeline(self):
        """Orquesta el flujo explícito de ejecución."""
        print("\n=== INICIANDO PIPELINE DEL AGENTE ORQUESTADOR ===\n")

        # 1. Preparación de datos
        self.data = self.data_prep.execute(self.file_path)
        if self.data is None:
            print("Error: El pipeline se detuvo en la etapa de Preparación.")
            return

        # 2. Análisis exploratorio
        eda_success = self.eda.execute(self.data)
        if not eda_success:
            print("Error: El pipeline se detuvo en la etapa de EDA.")
            return

        # 3. Modelado predictivo
        result = self.modeling.execute(self.data)
        if result is None:
            print("Error: El pipeline se detuvo en la etapa de Modelado.")
            return
        
        self.model, self.justification = result
        
        print("\n--- RESULTADO DE LA SELECCIÓN AUTOMÁTICA ---")
        print(f"Modelo Final: {type(self.model).__name__}")
        print(f"Justificación Técnica: {self.justification}")
        print("-------------------------------------------\n")

        print("\n=== PIPELINE FINALIZADO EXITOSAMENTE ===\n")

if __name__ == "__main__":
    # Punto de entrada
    file_name = 'Data set.csv'
    if not os.path.exists(file_name):
        print(f"Error: No se encuentra el archivo {file_name}")
    else:
        orchestrator = SocialImpactOrchestrator(file_name)
        orchestrator.run_pipeline()
