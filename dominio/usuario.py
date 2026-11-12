"""Entidad Usuario de la red social.

Agrupa la identidad de un usuario con su feed de publicaciones y su
bandeja de notificaciones. Cada usuario tiene un identificador entero
que coincide con su vértice en RedSeguimiento.
"""

from dominio.feed import Feed
from dominio.notificaciones import BandejaNotificaciones


class Usuario:
    """Usuario de la red con feed y bandeja de notificaciones propios.

    Atributos:
        id: Identificador entero del usuario. Coincide con su vértice
            en RedSeguimiento.
        username: Nombre de usuario único. Clave en IndiceUsuarios.
        nombre_visible: Nombre visible mostrado en el perfil.
        biografia: Texto biográfico del usuario.
        feed: Feed de publicaciones del usuario.
        bandeja: Bandeja de notificaciones del usuario.
    """

    def __init__(self, id_usuario, username, nombre_visible, biografia=""):
        """Crea un usuario con feed y bandeja vacíos.

        Complejidad: Tiempo O(1), espacio O(1).
        """
        self.id = id_usuario
        self.username = username
        self.nombre_visible = nombre_visible
        self.biografia = biografia
        self.feed = Feed()
        self.bandeja = BandejaNotificaciones()

    def publicar(self, texto, fecha):
        """Publica en el feed propio.

        Complejidad: Tiempo O(1), espacio O(1).
        """
        self.feed.publicar(texto, fecha, self.username)

    def agregar_notificacion(self, tipo, origen):
        """Agrega una notificación a la bandeja propia.

        Complejidad: Tiempo O(1), espacio O(1).
        """
        self.bandeja.agregar(tipo, origen)

    def cantidad_notificaciones(self):
        """Cantidad de notificaciones pendientes.

        Complejidad: Tiempo O(1), espacio O(1).
        """
        return self.bandeja.pendientes()
