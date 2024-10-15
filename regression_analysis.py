import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from tkinter import simpledialog, messagebox
import tkinter as tk

class RegressionAnalysis:
    """Clase para realizar análisis de regresión.

    Esta clase proporciona métodos para realizar análisis de regresión lineal
    y polinómica, así como interpolación de datos. Las métricas de desempeño
    se pueden calcular y mostrar en una interfaz gráfica.

    Attributes:
        data_ops (DataOperations): Objeto que contiene los datos necesarios
                                    para el análisis de regresión.
    """
  
    def __init__(self, data_ops):
        """Inicializa la clase con el objeto de operaciones de datos.

        Args:
            data_ops (DataOperations): Objeto que contiene los datos necesarios
                                        para el análisis.
        """
        self.data_ops = data_ops

    def calculate_metrics(self, y_true, y_pred):
        """Calcula las métricas de regresión.

        Args:
            y_true (array-like): Valores reales.
            y_pred (array-like): Valores predichos por el modelo.

        Returns:
            tuple: (R², MAE, MSE)

        Warnings:
            Asegúrate de que las dimensiones de `y_true` y `y_pred` coincidan.
        """
        r2 = r2_score(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        return r2, mae, mse

        def show_metrics(self, r2, mae, mse):
        """Muestra las métricas de regresión en una ventana de Tkinter.

        Args:
            r2 (float): Coeficiente de determinación R².
            mae (float): Error absoluto medio.
            mse (float): Error cuadrático medio.
        """
        metrics_window = tk.Toplevel()
        metrics_window.title("Métricas de Regresión")

        lbl_r2 = tk.Label(metrics_window, text=f"R²: {r2:.4f}", font=("Helvetica", 14))
        lbl_r2.pack(pady=5)

        lbl_mae = tk.Label(metrics_window, text=f"MAE: {mae:.4f}", font=("Helvetica", 14))
        lbl_mae.pack(pady=5)

        lbl_mse = tk.Label(metrics_window, text=f"MSE: {mse:.4f}", font=("Helvetica", 14))
        lbl_mse.pack(pady=5)
