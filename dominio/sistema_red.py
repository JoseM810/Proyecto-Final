"""Sistema de red social: integra IndiceUsuarios, RedSeguimiento y Usuario.

Orquesta las operaciones entre usuarios, relaciones de seguimiento,
feeds individuales y notificaciones. No modifica las estructuras
existentes; las conecta mediante una capa de integración.
"""

from dominio.indice_usuarios import IndiceUsuarios
from dominio.red import RedSeguimiento
from dominio.usuario import Usuario
from estructuras.errores import NombreDuplicadoError, UsuarioNoExisteError, PublicacionNoEncontradaError, AutoSeguimientoError


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
        self._siguiente_id_publicacion = 1

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
        if usuario_a.id == usuario_b.id:
            raise AutoSeguimientoError("un usuario no puede seguirse a sí mismo")
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

    def publicar(self, usuario, texto, fecha):
        """Publica en el feed del usuario con un ID global único.

        Asigna el siguiente identificador entero disponible en toda la red,
        lo registra en la publicación y lo devuelve.

        Complejidad: Tiempo O(1), espacio O(1).
        Lanza PublicacionInvalidaError si texto o fecha no cumplen
        (delegado en Feed).
        """
        id_publicacion = self._siguiente_id_publicacion
        self._siguiente_id_publicacion += 1
        usuario.feed.publicar(texto, fecha, usuario.username, id_publicacion)
        return id_publicacion

    def obtener_por_id(self, id_publicacion):
        """Busca una publicación por su ID en los feeds de todos los usuarios.

        Complejidad: Tiempo O(n·m) donde n es la cantidad de usuarios y
        m la cantidad de publicaciones por feed, espacio O(1).
        Lanza PublicacionNoEncontradaError si no se encuentra.
        """
        for nombre in self._indice.listar():
            usuario = self._indice.buscar(nombre)
            for publicacion in usuario.feed.recorrer():
                if publicacion.id == id_publicacion:
                    return publicacion
        raise PublicacionNoEncontradaError("no existe una publicación con ese ID")

    def obtener_todas_publicaciones(self):
        """Obtiene todas las publicaciones de todos los usuarios ordenadas por ID descendente.

        Recorre los feeds de todos los usuarios y devuelve las publicaciones
        ordenadas de la más reciente (ID mayor) a la más antigua (ID menor).

        Complejidad: Tiempo O(n·m log m) donde n es la cantidad de usuarios y
        m la cantidad de publicaciones por feed, espacio O(m·n).
        """
        todas = []
        for nombre in self._indice.listar():
            usuario = self._indice.buscar(nombre)
            for publicacion in usuario.feed.recorrer():
                todas.append(publicacion)
        todas.sort(key=lambda p: p.id, reverse=True)
        return todas

    def recomendar(self, username):
        """Entrega recomendaciones de usuarios para seguir a partir de un username.

        Complejidad: Tiempo O(V + E), espacio O(V).
        Lanza UsuarioNoExisteError si el username no existe.
        """
        usuario = self._indice.buscar(username)
        if usuario is None:
            raise UsuarioNoExisteError("usuario no existe")
        return self._red.recomendar(usuario.id)

    def comentar_publicacion(self, id_publicacion, autor_comentario, texto):
        """Comenta en una publicación y genera notificación COMENTARIO al autor.

        Complejidad: Tiempo O(n·m) donde n es la cantidad de usuarios y
        m la cantidad de publicaciones por feed, espacio O(1).
        Lanza PublicacionNoEncontradaError si no se encuentra la publicación.
        """
        publicacion = self.obtener_por_id(id_publicacion)
        publicacion.hilo.comentar(autor_comentario, texto)
        autor_publicacion = self._indice.buscar(publicacion.autor)
        autor_publicacion.agregar_notificacion("COMENTARIO", autor_comentario)

    def responder_comentario(self, id_publicacion, id_padre, autor_responde, texto):
        """Responde a un comentario y genera notificación RESPUESTA al autor del
        comentario padre.

        Complejidad: Tiempo O(n·m) donde n es la cantidad de usuarios y
        m la cantidad de publicaciones por feed, espacio O(1).
        Lanza PublicacionNoEncontradaError si no se encuentra la publicación.
        """
        publicacion = self.obtener_por_id(id_publicacion)
        publicacion.hilo.responder(id_padre, autor_responde, texto)
        comentario_padre = publicacion.hilo.obtener(id_padre)
        autor_comentario_padre = self._indice.buscar(comentario_padre.autor)
        autor_comentario_padre.agregar_notificacion("RESPUESTA", autor_responde)