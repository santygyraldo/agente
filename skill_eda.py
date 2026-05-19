import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

class EDASkill:
    """Skill 2: Análisis Exploratorio de Datos."""
    
    def __init__(self, output_dir="analysis_results"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def execute(self, df):
        print("[Skill: EDA] Generando análisis visual...")
        if df is None: return False
        
        # 1. Matriz de correlación
        plt.figure(figsize=(10, 8))
        numeric_df = df.select_dtypes(include=[np.number])
        sns.heatmap(numeric_df.corr(), annot=True, cmap='RdBu_r', center=0)
        plt.title('Matriz de Correlación')
        plt.savefig(f"{self.output_dir}/agente_correlation.png")
        plt.close()

        # 2. Distribución de Salud Mental por Plataforma (Boxplot)
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x='Most_Used_Platform', y='Mental_Health_Score')
        plt.title('Salud Mental por Plataforma')
        plt.savefig(f"{self.output_dir}/agente_mental_health.png")
        plt.close()

        # 3. Scatter Plots (Análisis Bivariado)
        self._generate_scatter_plots(df)

        # 4. Pairplot (Análisis Multivariado)
        self._generate_pairplot(df)

        # 5. Análisis Multivariado Adicional
        self._multivariate_analysis(df)

        print(f"  Análisis guardado en {self.output_dir}/")
        return True

    def _generate_scatter_plots(self, df):
        """Genera scatter plots para análisis bivariado."""
        print("  Generando Scatter Plots...")
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # Uso vs Salud Mental
        axes[0, 0].scatter(df['Avg_Daily_Usage_Hours'], df['Mental_Health_Score'], 
                          alpha=0.6, c='steelblue', edgecolors='white')
        axes[0, 0].set_xlabel('Uso Diario (horas)')
        axes[0, 0].set_ylabel('Salud Mental')
        axes[0, 0].set_title('Uso de Redes vs Salud Mental')
        
        # Uso vs Sueño
        axes[0, 1].scatter(df['Avg_Daily_Usage_Hours'], df['Sleep_Hours_Per_Night'], 
                          alpha=0.6, c='coral', edgecolors='white')
        axes[0, 1].set_xlabel('Uso Diario (horas)')
        axes[0, 1].set_ylabel('Horas de Sueño')
        axes[0, 1].set_title('Uso de Redes vs Horas de Sueño')
        
        # Sueño vs Salud Mental
        axes[1, 0].scatter(df['Sleep_Hours_Per_Night'], df['Mental_Health_Score'], 
                          alpha=0.6, c='seagreen', edgecolors='white')
        axes[1, 0].set_xlabel('Horas de Sueño')
        axes[1, 0].set_ylabel('Salud Mental')
        axes[1, 0].set_title('Horas de Sueño vs Salud Mental')
        
        # Edad vs Uso
        axes[1, 1].scatter(df['Age'], df['Avg_Daily_Usage_Hours'], 
                          alpha=0.6, c='purple', edgecolors='white')
        axes[1, 1].set_xlabel('Edad')
        axes[1, 1].set_ylabel('Uso Diario (horas)')
        axes[1, 1].set_title('Edad vs Uso de Redes')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/agente_scatter_plots.png")
        plt.close()
        print("    ✓ Scatter plots guardados")

    def _generate_pairplot(self, df):
        """Genera pairplot para análisis multivariado."""
        print("  Generando Pairplot (Análisis Multivariado)...")
        
        numeric_cols = ['Age', 'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score']
        pair_df = df[numeric_cols].copy()
        
        pairplot = sns.pairplot(pair_df, diag_kind='kde', plot_kws={'alpha': 0.6})
        pairplot.fig.suptitle('Pairplot: Análisis Multivariado de Variables Numéricas', 
                              y=1.02, fontsize=14, fontweight='bold')
        plt.savefig(f"{self.output_dir}/agente_pairplot.png", dpi=150, bbox_inches='tight')
        plt.close()
        print("    ✓ Pairplot guardado")

    def _multivariate_analysis(self, df):
        """Análisis multivariado adicional con hue por categorías."""
        print("  Generando Análisis Multivariado por Categorías...")
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Scatter multivariado: Uso vs Sueño, coloreado por Impacto General
        if 'Overall_Impact' in df.columns:
            sns.scatterplot(data=df, x='Avg_Daily_Usage_Hours', y='Sleep_Hours_Per_Night',
                           hue='Overall_Impact', s=80, alpha=0.7, ax=axes[0])
            axes[0].set_xlabel('Uso Diario (horas)')
            axes[0].set_ylabel('Horas de Sueño')
            axes[0].set_title('Uso vs Sueño (coloreado por Impacto General)')
            axes[0].legend(title='Impacto')
        
        # Scatter multivariado: Uso vs Salud Mental, coloreado por Género
        if 'Gender' in df.columns:
            sns.scatterplot(data=df, x='Avg_Daily_Usage_Hours', y='Mental_Health_Score',
                           hue='Gender', s=80, alpha=0.7, ax=axes[1])
            axes[1].set_xlabel('Uso Diario (horas)')
            axes[1].set_ylabel('Salud Mental')
            axes[1].set_title('Uso vs Salud Mental (coloreado por Género)')
            axes[1].legend(title='Género')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/agente_multivariate.png")
        plt.close()
        print("    ✓ Análisis multivariado guardado")
