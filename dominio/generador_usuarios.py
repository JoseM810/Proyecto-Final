"""Generador reproducible de usuarios para la red social.

Genera al menos 100 usuarios con nombres únicos, siempre en el mismo
orden cuando se usa la misma semilla. Soporta HU-01.
"""

import random


class GeneradorUsuarios:
    """Genera usuarios reproducibles con semilla fija."""

    def __init__(self, semilla=42):
        """Crea el generador con una semilla dada.

        Complejidad: Tiempo O(1), espacio O(1).
        """
        self._semilla = semilla

    def generar(self, cantidad=100):
        """Genera datos de usuarios reproducibles.

        Produce siempre la misma secuencia de usuarios para una misma
        semilla. Los nombres de usuario son únicos y secuenciales.

        Complejidad: Tiempo O(n), espacio O(n), con n la cantidad
        de usuarios generados.

        Retorna una lista de tuplas (username, nombre_visible, biografia).
        """
        rng = random.Random(self._semilla)
        datos = []
        for i in range(cantidad):
            username = f"usuario{i:04d}"
            nombre_visible = f"Usuario {i:04d}"
            sufijo = rng.randint(1, 999)
            biografia = (
                f"Biografía de {username}. Perfil #{sufijo} generado "
                f"con semilla {self._semilla}."
            )
            datos.append((username, nombre_visible, biografia))
        return datos
