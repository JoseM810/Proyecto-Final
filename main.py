"""Interfaz de consola de la red social (MVP).

Punto de entrada del sistema. Orquesta los módulos de dominio
y permite al usuario navegar mediante un menú de texto.
"""

import sys

from dominio.sistema_red import SistemaRed
from dominio.generador_usuarios import GeneradorUsuarios
from dominio.feed import PublicacionInvalidaError, FinDelFeedError, InicioDelFeedError, PublicacionNoEncontradaError
from estructuras.errores import ComentarioInvalidoError, ComentarioNoEncontradoError
from dominio.feed import PublicacionInvalidaError, FinDelFeedError, InicioDelFeedError


def mostrar_menu():
    """Muestra el menú principal de la aplicación.

    Complejidad: Tiempo O(1), espacio O(1).
    """
    print("\n=== RED SOCIAL - MENÚ PRINCIPAL ===")
    print("1. Listar usuarios")
    print("2. Seleccionar usuario activo")
    print("3. Buscar usuario por nombre")
    print("4. Publicar en mi feed")
    print("5. Ver mi feed")
    print("6. Seguir a un usuario")
    print("7. Dejar de seguir a un usuario")
    print("8. Ver recomendaciones")
    print("9. Ver mis notificaciones")
    print("10. Comentar en una publicación")
    print("11. Responder a un comentario")
    print("12. Ver comentarios de una publicación")
    print("0. Salir")
    print("===================================")


def opcion_no_implementada(opcion):
    """Muestra mensaje para opciones que aún no están implementadas.

    Complejidad: Tiempo O(1), espacio O(1).
    """
    print(f"\nLa opción {opcion} aún no está implementada.")


def salir():
    """Termina la ejecución del programa.

    Complejidad: Tiempo O(1), espacio O(1).
    """
    print("\nSaliendo de la aplicación. ¡Hasta pronto!")
    sys.exit(0)


def cargar_usuarios_iniciales(sistema):
    """Carga usuarios iniciales con semilla fija en el sistema.

    Complejidad: Tiempo O(n·h), espacio O(n), con n la cantidad de usuarios
    y h la altura del BST.
    """
    generador = GeneradorUsuarios(semilla=42)
    datos = generador.generar(100)
    sistema.cargar_desde_generador(datos)
    return sistema


def listar_usuarios(sistema):
    """Muestra los usuarios registrados en orden alfabético.

    Complejidad: Tiempo O(n), espacio O(h), con n la cantidad de usuarios
    y h la altura del BST.
    """
    usuarios = list(sistema.listar_usuarios())
    if not usuarios:
        print("\nNo hay usuarios registrados.")
        return
    print("\n--- Usuarios registrados ---")
    for nombre in usuarios:
        print(f"- {nombre}")
    print(f"Total: {len(usuarios)} usuarios")


def seleccionar_usuario(sistema):
    """Selecciona un usuario como activo para la sesión.

    Complejidad: Tiempo O(h), espacio O(1), con h la altura del BST.
    """
    username = input("Ingrese el nombre de usuario: ").strip()
    usuario = sistema.buscar_usuario_por_nombre(username)
    if usuario is None:
        print(f"\nEl usuario '{username}' no existe.")
        return None
    print(f"\nUsuario activo: {usuario.nombre_visible} (@{usuario.username})")
    return usuario


def buscar_usuario(sistema):
    """Busca un usuario por nombre y muestra su información.

    Complejidad: Tiempo O(h), espacio O(1), con h la altura del BST.
    """
    username = input("Ingrese el nombre de usuario: ").strip()
    usuario = sistema.buscar_usuario_por_nombre(username)
    if usuario is None:
        print(f"\nEl usuario '{username}' no existe.")
        return None
    print(f"\nUsuario encontrado: {usuario.nombre_visible} (@{usuario.username}), ID: {usuario.id}")
    return usuario


def publicar(usuario_activo):
    """Publica en el feed del usuario activo.

    Complejidad: Tiempo O(1), espacio O(1).
    """
    if usuario_activo is None:
        print("\nNo hay usuario activo seleccionado.")
        return
    texto = input("Texto de la publicación: ").strip()
    if not texto:
        print("\nEl texto no puede estar vacío.")
        return
    fecha_str = input("Fecha (entero >= 0): ").strip()
    try:
        fecha = int(fecha_str)
    except ValueError:
        print("\nFecha inválida: debe ser un entero >= 0.")
        return
    if fecha < 0:
        print("\nFecha inválida: debe ser un entero >= 0.")
        return
    try:
        usuario_activo.publicar(texto, fecha)
        print(f"\nPublicación creada: '{texto}'")
    except PublicacionInvalidaError as e:
        print(f"\nError al publicar: {e}")


def recorrer_feed(usuario_activo):
    """Muestra y navega el feed del usuario activo.

    Complejidad: Tiempo O(1) por operación de navegación, espacio O(1).
    """
    if usuario_activo is None:
        print("\nNo hay usuario activo seleccionado.")
        return
    feed = usuario_activo.feed
    if feed.cantidad() == 0:
        print("\nNo hay publicaciones en tu feed.")
        return
    print("\n--- Tu feed ---")
    print(f"Publicación actual: {feed.actual().texto}")
    while True:
        opcion = input("(a)vanzar, (r)etroceder, (s)alir: ").strip().lower()
        if opcion == "a":
            try:
                feed.avanzar()
                print(f"Publicación actual: {feed.actual().texto}")
            except FinDelFeedError:
                print("No hay publicaciones más antiguas.")
        elif opcion == "r":
            try:
                feed.retroceder()
                print(f"Publicación actual: {feed.actual().texto}")
            except InicioDelFeedError:
                print("No hay publicaciones más recientes.")
        elif opcion == "s":
            break
        else:
            print("Opción inválida.")


def comentar_publicacion(usuario_activo, sistema):
    """Comenta en una publicación del feed del usuario activo.

    Complejidad: Tiempo O(n) para buscar la publicación + O(1) para comentar,
    espacio O(1), con n la cantidad de publicaciones en el feed.
    """
    if usuario_activo is None:
        print("\nNo hay usuario activo seleccionado.")
        return
    id_str = input("ID de la publicación: ").strip()
    try:
        id_publicacion = int(id_str)
    except ValueError:
        print("\nID inválido: debe ser un entero.")
        return
    texto = input("Texto del comentario: ").strip()
    if not texto:
        print("\nEl texto no puede estar vacío.")
        return
    try:
        publicacion = sistema.obtener_por_id(id_publicacion)
    except PublicacionNoEncontradaError:
        print(f"\nNo existe la publicación con ID {id_publicacion}.")
        return
    try:
        publicacion.hilo.comentar(usuario_activo.nombre_visible, texto)
        print(f"\nComentario agregado a la publicación {id_publicacion}.")
    except ComentarioInvalidoError as e:
        print(f"\nError al comentar: {e}")


def ver_comentarios_publicacion(sistema, id_publicacion):
    """Muestra los comentarios y respuestas de una publicación.

    Complejidad: Tiempo O(n), espacio O(n), con n la cantidad de comentarios.
    """
    try:
        publicacion = sistema.obtener_por_id(id_publicacion)
    except PublicacionNoEncontradaError:
        print(f"\nNo existe la publicación con ID {id_publicacion}.")
        return
    hilo = publicacion.hilo
    if hilo.cantidad() == 0:
        print(f"\nLa publicación {id_publicacion} no tiene comentarios.")
        return
    print(f"\n--- Comentarios de la publicación {id_publicacion} ---")
    for comentario in hilo.recorrer():
        indentacion = "  " * comentario.profundidad
        print(f"{indentacion}[{comentario.id}] {comentario.autor}: {comentario.texto}")


def responder_comentario(usuario_activo, sistema):
    """Responde a un comentario de una publicación.

    Complejidad: Tiempo O(n) para buscar la publicación + O(1) para responder,
    espacio O(1), con n la cantidad de publicaciones en el feed.
    """
    if usuario_activo is None:
        print("\nNo hay usuario activo seleccionado.")
        return
    id_str = input("ID de la publicación: ").strip()
    try:
        id_publicacion = int(id_str)
    except ValueError:
        print("\nID inválido: debe ser un entero.")
        return
    try:
        publicacion = sistema.obtener_por_id(id_publicacion)
    except PublicacionNoEncontradaError:
        print(f"\nNo existe la publicación con ID {id_publicacion}.")
        return
    id_str_padre = input("ID del comentario padre: ").strip()
    try:
        id_padre = int(id_str_padre)
    except ValueError:
        print("\nID inválido: debe ser un entero.")
        return
    texto = input("Texto de la respuesta: ").strip()
    if not texto:
        print("\nEl texto no puede estar vacío.")
        return
    try:
        publicacion.hilo.responder(id_padre, usuario_activo.nombre_visible, texto)
        print(f"\nRespuesta agregada al comentario {id_padre} de la publicación {id_publicacion}.")
    except ComentarioNoEncontradoError:
        print(f"\nNo existe el comentario con ID {id_padre}.")
    except ComentarioInvalidoError as e:
        print(f"\nError al responder: {e}")


def main():
    """Función principal de la aplicación de consola.

    Complejidad: Tiempo O(n) donde n es el número de iteraciones del bucle,
    espacio O(1).
    """
    sistema = SistemaRed()
    cargar_usuarios_iniciales(sistema)

    usuario_activo = None

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            salir()
        elif opcion == "1":
            listar_usuarios(sistema)
        elif opcion == "2":
            usuario_seleccionado = seleccionar_usuario(sistema)
            if usuario_seleccionado is not None:
                usuario_activo = usuario_seleccionado
        elif opcion == "3":
            buscar_usuario(sistema)
        elif opcion == "4":
            publicar(usuario_activo)
        elif opcion == "5":
            recorrer_feed(usuario_activo)
        elif opcion == "10":
            comentar_publicacion(usuario_activo, sistema)
        elif opcion == "11":
            responder_comentario(usuario_activo, sistema)
        elif opcion == "12":
            id_str = input("ID de la publicación: ").strip()
            try:
                id_publicacion = int(id_str)
            except ValueError:
                print("\nID inválido: debe ser un entero.")
                continue
            ver_comentarios_publicacion(sistema, id_publicacion)
        else:
            opcion_no_implementada(opcion)


if __name__ == "__main__":
    main()
