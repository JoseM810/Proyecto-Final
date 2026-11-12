"""Interfaz de consola de la red social (MVP).

Punto de entrada del sistema. Orquesta los módulos de dominio
y permite al usuario navegar mediante un menú de texto.
"""

import sys

from dominio.sistema_red import SistemaRed
from dominio.generador_usuarios import GeneradorUsuarios
from dominio.historial import Historial
from dominio.feed import PublicacionInvalidaError, FinDelFeedError, InicioDelFeedError, PublicacionNoEncontradaError
from estructuras.errores import ComentarioInvalidoError, ComentarioNoEncontradoError, UsuarioNoExisteError, PantallaInvalidaError, NadaAtrasError, AutoSeguimientoError


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
    print("13. Visitar una pantalla")
    print("14. Volver a la pantalla anterior")
    print("15. Explorar publicaciones de todos los usuarios")
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
    """Selecciona un usuario activo para la sesión.

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


def publicar(usuario_activo, sistema):
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
    try:
        id_publicacion = sistema.publicar(usuario_activo, texto, 0)
        print(f"\nPublicación creada: '{texto}' (ID: {id_publicacion})")
    except PublicacionInvalidaError as e:
        print(f"\nError al publicar: {e}")


def recorrer_feed(usuario_activo, sistema):
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
    print(f"Publicación actual [{feed.actual().id}]: {feed.actual().texto}")
    while True:
        opcion = input("(a)vanzar, (r)etroceder, (s)alir: ").strip().lower()
        if opcion == "a":
            try:
                feed.avanzar()
                print(f"Publicación actual [{feed.actual().id}]: {feed.actual().texto}")
            except FinDelFeedError:
                print("No hay publicaciones más antiguas.")
        elif opcion == "r":
            try:
                feed.retroceder()
                print(f"Publicación actual [{feed.actual().id}]: {feed.actual().texto}")
            except InicioDelFeedError:
                print("No hay publicaciones más recientes.")
        elif opcion == "s":
            break
        else:
            print("Opción inválida.")


def comentar_publicacion(usuario_activo, sistema):
    """Comenta en una publicación del feed del usuario activo.

    Complejidad: Tiempo O(h + g) para buscar la publicación + O(1) para comentar,
    espacio O(1), con h la altura del BST y g el grado del usuario en el grafo.
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
        sistema.comentar_publicacion(id_publicacion, usuario_activo.username, texto)
        print(f"\nComentario agregado a la publicación {id_publicacion}.")
    except PublicacionNoEncontradaError:
        print(f"\nNo existe la publicación con ID {id_publicacion}.")
    except ComentarioInvalidoError as e:
        print(f"\nError al comentar: {e}")


def responder_comentario(usuario_activo, sistema):
    """Responde a un comentario de una publicación.

    Complejidad: Tiempo O(h + g) para buscar la publicación + O(1) para responder,
    espacio O(1), con h la altura del BST y g el grado del usuario en el grafo.
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
        sistema.responder_comentario(id_publicacion, id_padre, usuario_activo.username, texto)
        print(f"\nRespuesta agregada al comentario {id_padre} de la publicación {id_publicacion}.")
    except PublicacionNoEncontradaError:
        print(f"\nNo existe la publicación con ID {id_publicacion}.")
    except ComentarioNoEncontradoError:
        print(f"\nNo existe el comentario con ID {id_padre}.")
    except ComentarioInvalidoError as e:
        print(f"\nError al responder: {e}")


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


def seguir_usuario(usuario_activo, sistema):
    """Sigue a otro usuario desde el usuario activo.

    Complejidad: Tiempo O(h + g), espacio O(1).
    """
    if usuario_activo is None:
        print("\nNo hay usuario activo seleccionado.")
        return
    username = input("Ingrese el nombre de usuario a seguir: ").strip()
    if not username:
        print("\nEl nombre de usuario no puede estar vacío.")
        return
    try:
        fue_nuevo = sistema.seguir(usuario_activo.username, username)
        if fue_nuevo:
            print(f"\nAhora sigues a {username}.")
        else:
            print(f"\nYa seguías a {username}.")
    except UsuarioNoExisteError:
        print(f"\nEl usuario '{username}' no existe.")
    except AutoSeguimientoError:
        print("\nNo puedes seguirte a ti mismo.")


def dejar_de_seguir(usuario_activo, sistema):
    """Deja de seguir a otro usuario desde el usuario activo.

    Complejidad: Tiempo O(h + g), espacio O(1).
    """
    if usuario_activo is None:
        print("\nNo hay usuario activo seleccionado.")
        return
    username = input("Ingrese el nombre de usuario a dejar de seguir: ").strip()
    if not username:
        print("\nEl nombre de usuario no puede estar vacío.")
        return
    try:
        sistema.dejar_de_seguir(usuario_activo.username, username)
        print(f"\nHas dejado de seguir a {username}.")
    except UsuarioNoExisteError:
        print(f"\nEl usuario '{username}' no existe.")


def mostrar_recomendaciones(usuario_activo, sistema):
    """Muestra usuarios recomendados para seguir.

    Complejidad: Tiempo O(V + E), espacio O(V).
    """
    if usuario_activo is None:
        print("\nNo hay usuario activo seleccionado.")
        return
    try:
        recomendaciones = list(sistema.recomendar(usuario_activo.username))
        if not recomendaciones:
            print("\nNo hay recomendaciones disponibles.")
            return
        print("\n--- Usuarios recomendados ---")
        for id_usuario in recomendaciones:
            u = sistema.obtener_usuario_por_id(id_usuario)
            print(f"- {u.nombre_visible} (@{u.username})")
    except UsuarioNoExisteError:
        print("\nError al obtener recomendaciones.")


def consultar_notificaciones(usuario_activo):
    """Muestra y consume las notificaciones pendientes del usuario activo.

    Complejidad: Tiempo O(n), espacio O(1).
    """
    if usuario_activo is None:
        print("\nNo hay usuario activo seleccionado.")
        return
    if usuario_activo.cantidad_notificaciones() == 0:
        print("\nNo tienes notificaciones pendientes.")
        return
    print("\n--- Tus notificaciones ---")
    while usuario_activo.cantidad_notificaciones() > 0:
        notificacion = usuario_activo.bandeja.leer_siguiente()
        if notificacion:
            print(f"[{notificacion.tipo}] {notificacion.origen}")


def visitar_pantalla(historial):
    """Visita una pantalla y la registra en el historial.

    Complejidad: Tiempo O(1), espacio O(1).
    """
    pantalla = input("Ingrese el nombre de la pantalla a visitar: ").strip()
    try:
        historial.visitar(pantalla)
        print(f"\nPantalla actual: {historial.actual()}")
    except PantallaInvalidaError as e:
        print(f"\nError al visitar: {e}")


def volver_pantalla(historial):
    """Vuelve a la pantalla anterior del historial.

    Complejidad: Tiempo O(1), espacio O(1).
    """
    try:
        anterior = historial.volver()
        print(f"\nVolviendo a la pantalla: {anterior}")
    except NadaAtrasError:
        print("\nNo hay pantalla anterior a la que volver.")


def explorar_publicaciones(sistema):
    """Muestra las publicaciones de todos los usuarios ordenadas por ID descendente.

    Permite navegar entre todas las publicaciones de la red usando
    'a' para ir a la más antigua y 'r' para la más reciente.

    Complejidad: Tiempo O(1) por operación de navegación, espacio O(m·n).
    """
    todas = sistema.obtener_todas_publicaciones()
    if not todas:
        print("\nNo hay publicaciones en la red.")
        return
    indice = 0
    total = len(todas)
    while True:
        publicacion = todas[indice]
        print(f"\n--- Publicación [{publicacion.id}] de {publicacion.autor} ---")
        print(publicacion.texto)
        opcion = input("(a)ntigua, (r)eciente, (s)alir: ").strip().lower()
        if opcion == "a":
            if indice + 1 < total:
                indice += 1
            else:
                print("No hay publicaciones más antiguas.")
        elif opcion == "r":
            if indice - 1 >= 0:
                indice -= 1
            else:
                print("No hay publicaciones más recientes.")
        elif opcion == "s":
            break
        else:
            print("Opción inválida.")


def main():
    """Función principal de la aplicación de consola.

    Complejidad: Tiempo O(n) donde n es el número de iteraciones del bucle,
    espacio O(1).
    """
    sistema = SistemaRed()
    cargar_usuarios_iniciales(sistema)
    historial = Historial()

    usuario_activo = None

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "0":
            salir()
        elif opcion == "1":
            listar_usuarios(sistema)
        elif opcion == "2":
            usuario_activo = seleccionar_usuario(sistema)
        elif opcion == "3":
            buscar_usuario(sistema)
        elif opcion == "4":
            publicar(usuario_activo, sistema)
        elif opcion == "5":
            recorrer_feed(usuario_activo, sistema)
        elif opcion == "6":
            seguir_usuario(usuario_activo, sistema)
        elif opcion == "7":
            dejar_de_seguir(usuario_activo, sistema)
        elif opcion == "8":
            mostrar_recomendaciones(usuario_activo, sistema)
        elif opcion == "9":
            consultar_notificaciones(usuario_activo)
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
        elif opcion == "13":
            visitar_pantalla(historial)
        elif opcion == "14":
            volver_pantalla(historial)
        elif opcion == "15":
            explorar_publicaciones(sistema)
        else:
            opcion_no_implementada(opcion)


if __name__ == "__main__":
    main()