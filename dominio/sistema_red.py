"""Sistema de red social: integra IndiceUsuarios, RedSeguimiento y Usuario.

Orquesta las operaciones entre usuarios, relaciones de seguimiento,
feeds individuales y notificaciones. No modifica las estructuras
existentes; las conecta mediante una capa de integración.
"""

from dominio.indice_usuarios import IndiceUsuarios
from dominio.red import RedSeguimiento
from dominio.usuario import Usuario
from estructuras.errores import NombreDuplicadoError, UsuarioNoExisteError


class SistemaRed:
    """Orquestador de la red social.

    Mantiene la correspondencia entre nombres de usuario, objetos Usuario
    e identificadores de vértice en RedSeguimiento.
    """

    def __init__(self):
        """Crea un sistema de red vacío.

        Complejidad: Tiempo O(1), espacio O(1).
        """
        self._indice = IndiceUsuarios()
        self._red = RedSeguimiento()
        self._usuarios_por_id = []

    def registrar_usuario(self, username, nombre_visible, biografia=""):
        """Registra un nuevo usuario en la red.

        Asigna un identificador entero consecutivo de RedSeguimiento,
        crea el Usuario, lo indexa por nombre y lo guarda por ID.

        Complejidad: Tiempo O(h), espacio O(1), con h la altura del BST.
        """
        id_usuario = self._red.agregar_usuario()
        usuario = Usuario(id_usuario, username, nombre_visible, biografia)
        self._indice.agregar(username, usuario)
        while len(self._usuarios_por_id) <= id_usuario:
            self._usuarios_por_id.append(None)
        self._usuarios_por_id[id_usuario] = usuario
        return usuario

    def buscar_usuario_por_nombre(self, username):
        """Busca un usuario por su nombre de usuario.

        Complejidad: Tiempo O(h), espacio O(1).
        """
        return self._indice.buscar(username)

    def obtener_usuario_por_id(self, id_usuario):
        """Obtiene un usuario por su identificador entero.

        Complejidad: Tiempo O(1), espacio O(1).
        """
        if id_usuario < 0 or id_usuario >= len(self._usuarios_por_id):
            return None
        return self._usuarios_por_id[id_usuario]

    def seguir(self, username_a, username_b):
        """username_a empieza a seguir a username_b.

        Si la relación es nueva, genera una notificación NUEVO_SEGUIDOR
        para username_b.

        Complejidad: Tiempo O(h + g), espacio O(1), con h la altura del
        BST y g el grado del usuario en el grafo.
        """
        usuario_a = self._indice.buscar(username_a)
        usuario_b = self._indice.buscar(username_b)
        if usuario_a is None or usuario_b is None:
            raise UsuarioNoExisteError("uno de los usuarios no existe")
        fue_nuevo = self._red.seguir(usuario_a.id, usuario_b.id)
        if fue_nuevo:
            usuario_b.agregar_notificacion("NUEVO_SEGUIDOR", username_a)
        return fue_nuevo

    def dejar_de_seguir(self, username_a, username_b):
        """username_a deja de seguir a username_b.

        Complejidad: Tiempo O(h + g), espacio O(1), con h la altura del
        BST y g el grado del usuario en el grafo.
        """
        usuario_a = self._indice.buscar(username_a)
        usuario_b = self._indice.buscar(username_b)
        if usuario_a is None or usuario_b is None:
            raise UsuarioNoExisteError("uno de los usuarios no existe")
        return self._red.dejar_de_seguir(usuario_a.id, usuario_b.id)

    def listar_usuarios(self):
        """Entrega los nombres de usuario en orden alfabético.

        Complejidad: Tiempo O(n), espacio O(h).
        """
        return self._indice.listar()

    def cantidad_usuarios(self):
        """Cantidad de usuarios registrados.

        Complejidad: Tiempo O(1), espacio O(1).
        """
        return self._indice.cantidad()

    def cargar_desde_generador(self, datos_usuarios):
        """Carga usuarios desde datos de GeneradorUsuarios.

        Cada entrada es una tupla (username, nombre_visible, biografia).
        Valida que no haya nombres duplicados antes de registrar cualquier
        usuario, evitando cargas parciales.

        Complejidad: Tiempo O(n·h), espacio O(n), con n la cantidad
        de usuarios y h la altura del BST.
        """
        nombres_vistos = []
        for username, nombre_visible, biografia in datos_usuarios:
            if username in nombres_vistos:
                raise NombreDuplicadoError("ya existe un usuario con ese nombre")
            nombres_vistos.append(username)
        for username, nombre_visible, biografia in datos_usuarios:
            self.registrar_usuario(username, nombre_visible, biografia)
