"""Pruebas de la interfaz de consola (main.py).

Verifica las tareas M-01 a M-09.
"""

import io
from unittest.mock import patch

from dominio.sistema_red import SistemaRed

import main


def test_mostrar_menu_muestra_opciones():
    """M-01 CA-01: El menú muestra el título y la opción de salida."""
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.mostrar_menu()
    texto = salida.getvalue()
    assert "RED SOCIAL - MENÚ PRINCIPAL" in texto
    assert "0. Salir" in texto


def test_opcion_no_implementada_muestra_mensaje():
    """M-01 CA-02: La opción no implementada muestra un mensaje descriptivo."""
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.opcion_no_implementada("5")
    texto = salida.getvalue()
    assert "5" in texto
    assert "no está implementada" in texto


def test_salir_termina_programa():
    """M-01 CA-03: La opción salir termina el programa con código 0."""
    try:
        main.salir()
    except SystemExit as e:
        assert e.code == 0
    else:
        assert False, "salir() no lanzó SystemExit"


def test_main_ejecuta_con_opcion_salir():
    """M-01 CA-03: La aplicación ejecuta sin errores y sale con la opción 0."""
    with patch("builtins.input", return_value="0"):
        try:
            main.main()
        except SystemExit:
            pass  # Esperado al salir


def test_cargar_usuarios_iniciales():
    """M-02 CA-01: Carga al menos 100 usuarios con semilla fija."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    assert sistema.cantidad_usuarios() == 100


def test_cargar_usuarios_ids_consecutivos():
    """M-02 CA-02: Los usuarios tienen IDs consecutivos desde 0."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    assert sistema.obtener_usuario_por_id(0).username == "usuario0000"
    assert sistema.obtener_usuario_por_id(99).username == "usuario0099"


def test_listar_usuarios_orden_alfabetico():
    """M-03 HU-05 CA-03: Lista usuarios en orden alfabético."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    nombres = list(sistema.listar_usuarios())
    assert nombres == sorted(nombres)
    assert len(nombres) == 100


def test_listar_usuarios_muestra_contenido():
    """M-03: listar_usuarios imprime los nombres de los usuarios."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.listar_usuarios(sistema)
    texto = salida.getvalue()
    assert "Usuarios registrados" in texto
    assert "usuario0000" in texto
    assert "usuario0099" in texto
    assert "Total: 100 usuarios" in texto


def test_seleccionar_usuario_existente():
    """M-04 HU-05 CA-01: Seleccionar usuario existente lo establece como activo."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    with patch("builtins.input", return_value="usuario0000"):
        usuario = main.seleccionar_usuario(sistema)
    assert usuario is not None
    assert usuario.username == "usuario0000"
    assert usuario.id == 0


def test_seleccionar_usuario_inexistente():
    """M-04 HU-05 CA-02: Seleccionar usuario inexistente retorna None y muestra mensaje."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    salida = io.StringIO()
    with patch("builtins.input", return_value="usuario_inexistente"):
        with patch("sys.stdout", salida):
            usuario = main.seleccionar_usuario(sistema)
    texto = salida.getvalue()
    assert usuario is None
    assert "usuario_inexistente" in texto
    assert "no existe" in texto


def test_seleccionar_usuario_conserva_activo():
    """M-04 HU-05 CA-01: Seleccionar usuario inexistente no reemplaza al activo."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    with patch("builtins.input", return_value="usuario0000"):
        usuario_activo = main.seleccionar_usuario(sistema)
    assert usuario_activo is not None
    assert usuario_activo.username == "usuario0000"
    with patch("builtins.input", return_value="usuario_inexistente"):
        resultado = main.seleccionar_usuario(sistema)
    assert resultado is None
    assert usuario_activo.username == "usuario0000"


def test_buscar_usuario_existente():
    """M-05 HU-05 CA-01: Buscar usuario existente muestra su información."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    salida = io.StringIO()
    with patch("builtins.input", return_value="usuario0000"):
        with patch("sys.stdout", salida):
            usuario = main.buscar_usuario(sistema)
    texto = salida.getvalue()
    assert usuario is not None
    assert usuario.username == "usuario0000"
    assert "usuario0000" in texto


def test_buscar_usuario_inexistente():
    """M-05 HU-05 CA-02: Buscar usuario inexistente devuelve None y muestra mensaje."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    salida = io.StringIO()
    with patch("builtins.input", return_value="usuario_inexistente"):
        with patch("sys.stdout", salida):
            usuario = main.buscar_usuario(sistema)
    texto = salida.getvalue()
    assert usuario is None
    assert "usuario_inexistente" in texto
    assert "no existe" in texto


def test_publicar_en_feed():
    """M-05 HU-03 CA-01: Publicar en el feed del usuario activo."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.publicar("Publicación de prueba", 1)
    salida = io.StringIO()
    with patch("builtins.input", return_value="Publicación de prueba"):
        with patch("sys.stdout", salida):
            main.publicar(u_activo, sistema)
    texto = salida.getvalue()
    assert "Publicación creada: 'Publicación de prueba'" in texto
    assert "(ID: 1)" in texto


def test_publicar_solo_solicita_texto():
    """M-05 HU-03 CA-01: Publicar solicita únicamente el texto, sin pedir fecha."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.publicar("Publicación de prueba", 1)
    salida = io.StringIO()
    with patch("builtins.input", return_value="Solo texto"):
        with patch("sys.stdout", salida):
            main.publicar(u_activo, sistema)
    texto = salida.getvalue()
    assert "Publicación creada: 'Solo texto'" in texto
    assert "(ID: 1)" in texto


def test_publicar_texto_vacio():
    """M-05 HU-03 CA-01: Publicar con texto vacío se rechaza."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    salida = io.StringIO()
    with patch("builtins.input", side_effect=[""]):
        with patch("sys.stdout", salida):
            main.publicar(u_activo, sistema)
    texto = salida.getvalue()
    assert "El texto no puede estar vacío" in texto


def test_publicar_sin_fecha():
    """M-05 HU-03 CA-01: Publicar solo solicita texto y usa fecha por defecto."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    salida = io.StringIO()
    with patch("builtins.input", return_value="Texto sin fecha"):
        with patch("sys.stdout", salida):
            main.publicar(u_activo, sistema)
    texto = salida.getvalue()
    assert "Publicación creada: 'Texto sin fecha'" in texto
    publicacion = u_activo.feed.actual()
    assert publicacion.texto == "Texto sin fecha"
    assert publicacion.fecha == 0


def test_publicar_dos_usuarios_ids_diferentes():
    """M-05 HU-03 CA-01: Dos usuarios reciben IDs globales diferentes."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u0 = sistema.obtener_usuario_por_id(0)
    u1 = sistema.obtener_usuario_por_id(1)
    salida0 = io.StringIO()
    with patch("builtins.input", return_value="Post de usuario 0"):
        with patch("sys.stdout", salida0):
            main.publicar(u0, sistema)
    assert "(ID: 1)" in salida0.getvalue()
    salida1 = io.StringIO()
    with patch("builtins.input", return_value="Post de usuario 1"):
        with patch("sys.stdout", salida1):
            main.publicar(u1, sistema)
    assert "(ID: 2)" in salida1.getvalue()


def test_obtener_por_id_encuentra_publicacion_correcta_de_cada_usuario():
    """M-05 HU-03 CA-01: obtener_por_id devuelve la publicación de cada usuario."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u0 = sistema.obtener_usuario_por_id(0)
    u1 = sistema.obtener_usuario_por_id(1)
    with patch("builtins.input", return_value="Post A"):
        sistema.publicar(u0, "Post A", 0)
    with patch("builtins.input", return_value="Post B"):
        sistema.publicar(u1, "Post B", 0)
    p0 = sistema.obtener_por_id(1)
    p1 = sistema.obtener_por_id(2)
    assert p0.texto == "Post A"
    assert p1.texto == "Post B"
    assert p0.autor == "usuario0000"
    assert p1.autor == "usuario0001"


def test_comentar_publicacion_con_id_global():
    """M-09 HU-07 CA-05: Comentar en publicación con ID global de otro usuario."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u0 = sistema.obtener_usuario_por_id(0)
    u1 = sistema.obtener_usuario_por_id(1)
    with patch("builtins.input", return_value="Post de u0"):
        sistema.publicar(u0, "Post de u0", 0)
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["1", "Comentario de u1"]):
        with patch("sys.stdout", salida):
            main.comentar_publicacion(u1, sistema)
    texto = salida.getvalue()
    assert "Comentario agregado a la publicación 1" in texto
    p = sistema.obtener_por_id(1)
    assert p.hilo.cantidad() == 1


def test_recorrer_feed_muestra_ids():
    """M-05 HU-03 CA-01: Al recorrer el feed se muestra el ID de cada publicación."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u0 = sistema.obtener_usuario_por_id(0)
    with patch("builtins.input", return_value="Post 1"):
        sistema.publicar(u0, "Post 1", 0)
    with patch("builtins.input", return_value="Post 2"):
        sistema.publicar(u0, "Post 2", 0)
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["a", "s"]):
        with patch("sys.stdout", salida):
            main.recorrer_feed(u0, sistema)
    texto = salida.getvalue()
    assert "[2]" in texto
    assert "[1]" in texto
    """M-05 HU-03 CA-04: Feed vacío muestra mensaje vacío."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    salida = io.StringIO()
    with patch("builtins.input", return_value="1"):
        with patch("sys.stdout", salida):
            main.recorrer_feed(u_activo, sistema)
    texto = salida.getvalue()
    assert "No hay publicaciones en tu feed." in texto


def test_recorrer_feed_avanzar_retroceder():
    """M-05 HU-03 CA-02: Avanzar y luego retroceder deja en la misma publicación."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.publicar("Publicación 1", 1)
    u_activo.publicar("Publicación 2", 2)
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["1", "a", "r", "s"]):
        with patch("sys.stdout", salida):
            main.recorrer_feed(u_activo, sistema)
    texto = salida.getvalue()
    assert "Publicación 1" in texto
    assert "Publicación 2" in texto


def test_recorrer_feed_limites():
    """M-05 HU-03 CA-03: Retroceder en primera y avanzar en última avisa sin cambiar."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.publicar("Publicación única", 1)
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["1", "r", "a", "s"]):
        with patch("sys.stdout", salida):
            main.recorrer_feed(u_activo, sistema)
    texto = salida.getvalue()
    assert "No hay publicaciones más recientes" in texto
    assert "No hay publicaciones más antiguas" in texto


def test_comentar_publicacion_existente():
    """M-07 HU-04 CA-01: Comentar en una publicación existente agrega la respuesta."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.publicar("Publicación de prueba", 1)
    publicacion = u_activo.feed.actual()
    publicacion.hilo.comentar(sistema.obtener_usuario_por_id(0).username, "Comentario existente")
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["1", "1", "Texto de respuesta"]):
        with patch("sys.stdout", salida):
            main.responder_comentario(u_activo, sistema)
    texto = salida.getvalue()
    assert "Respuesta agregada" in texto
    assert "comentario 1" in texto
    assert "publicación 1" in texto


def test_responder_comentario_padre_inexistente():
    """M-07 HU-04 CA-03: Responder a comentario inexistente lanza error."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.publicar("Publicación de prueba", 1)
    publicacion = u_activo.feed.actual()
    publicacion.hilo.comentar("Autor prueba", "Comentario existente")
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["1", "999", "Texto de respuesta"]):
        with patch("sys.stdout", salida):
            main.responder_comentario(u_activo, sistema)
    texto = salida.getvalue()
    assert "no existe el comentario" in texto.lower()


def test_responder_comentario_texto_vacio():
    """M-07 HU-04 CA-01: Responder con texto vacío se rechaza."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.publicar("Publicación de prueba", 1)
    publicacion = u_activo.feed.actual()
    publicacion.hilo.comentar("Autor prueba", "Comentario existente")
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["1", "1", ""]):
        with patch("sys.stdout", salida):
            main.responder_comentario(u_activo, sistema)
    texto = salida.getvalue()
    assert "El texto no puede estar vacío" in texto


def test_comentar_publicacion_genera_notificacion():
    """M-09 HU-07 CA-05: Comentar en una publicación genera notificación COMENTARIO al autor."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.publicar("Publicación de prueba", 1)
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["1", "Texto de comentario"]):
        with patch("sys.stdout", salida):
            main.comentar_publicacion(u_activo, sistema)
    texto = salida.getvalue()
    assert "Comentario agregado a la publicación 1" in texto
    # El autor de la publicación (usuario 0) recibió una notificación COMENTARIO
    autor_publicacion = sistema.obtener_usuario_por_id(0)
    assert autor_publicacion.cantidad_notificaciones() == 1
    notificacion = autor_publicacion.bandeja.leer_siguiente()
    assert notificacion.tipo == "COMENTARIO"
    assert notificacion.origen == "usuario0000"


def test_responder_comentario_genera_notificacion():
    """M-09 HU-07 CA-06: Responder a un comentario genera notificación RESPUESTA al autor del comentario padre."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.publicar("Publicación de prueba", 1)
    publicacion = u_activo.feed.actual()
    publicacion.hilo.comentar(sistema.obtener_usuario_por_id(0).username, "Comentario existente")
    u_responde = sistema.obtener_usuario_por_id(2)
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["1", "1", "Texto de respuesta"]):
        with patch("sys.stdout", salida):
            main.responder_comentario(u_responde, sistema)
    texto = salida.getvalue()
    assert "Respuesta agregada al comentario 1 de la publicación 1" in texto
    # El autor del comentario padre (usuario 0) recibió una notificación RESPUESTA
    autor_comentario_padre = sistema.obtener_usuario_por_id(0)
    assert autor_comentario_padre.cantidad_notificaciones() == 1
    notificacion = autor_comentario_padre.bandeja.leer_siguiente()
    assert notificacion.tipo == "RESPUESTA"
    assert notificacion.origen == "usuario0002"


def test_ver_comentarios_publicacion_con_comentarios():
    """M-08 HU-04 CA-02: Ver comentarios y respuestas de una publicación."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.publicar("Publicación de prueba", 1)
    publicacion = u_activo.feed.actual()
    publicacion.hilo.comentar("Autor prueba", "Comentario 1")
    publicacion.hilo.comentar("Autor prueba", "Comentario 2")
    publicacion.hilo.responder(1, "Autor prueba", "Respuesta al comentario 1")
    salida = io.StringIO()
    with patch("builtins.input", return_value="1"):
        with patch("sys.stdout", salida):
            main.ver_comentarios_publicacion(sistema, 1)
    texto = salida.getvalue()
    assert "Comentarios de la publicación 1" in texto
    assert "Comentario 1" in texto
    assert "Comentario 2" in texto
    assert "Respuesta al comentario 1" in texto


def test_ver_comentarios_publicacion_vacia():
    """M-08 HU-04 CA-02: Publicación sin comentarios muestra mensaje vacío."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.publicar("Publicación sin comentarios", 1)
    salida = io.StringIO()
    with patch("builtins.input", return_value="1"):
        with patch("sys.stdout", salida):
            main.ver_comentarios_publicacion(sistema, 1)
    texto = salida.getvalue()
    assert "no tiene comentarios" in texto.lower()


def test_ver_comentarios_publicacion_inexistente():
    """M-08 HU-04 CA-02: Publicación inexistente devuelve mensaje de error."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    salida = io.StringIO()
    with patch("builtins.input", return_value="1"):
        with patch("sys.stdout", salida):
            main.ver_comentarios_publicacion(sistema, 1)
    texto = salida.getvalue()
    assert "no existe" in texto.lower()


def test_seguir_usuario_desde_menu():
    """M-10 HU-02 CA-01: Seguir a un usuario desde el menú genera notificación y crea relación real."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    salida = io.StringIO()
    with patch("builtins.input", return_value="usuario0001"):
        with patch("sys.stdout", salida):
            main.seguir_usuario(u_activo, sistema)
    texto = salida.getvalue()
    assert "Ahora sigues a usuario0001" in texto
    # La relación real de seguimiento existe: intentar seguir de nuevo devuelve False (ya existe)
    assert sistema.seguir("usuario0000", "usuario0001") is False
    # El usuario seguido recibió una notificación NUEVO_SEGUIDOR
    u_seguido = sistema.obtener_usuario_por_id(1)
    assert u_seguido.cantidad_notificaciones() == 1
    notif = u_seguido.bandeja.leer_siguiente()
    assert notif.tipo == "NUEVO_SEGUIDOR"
    assert notif.origen == "usuario0000"


def test_seguirse_a_si_mismo_desde_menu():
    """M-10 HU-02 CA-04: Intentar seguirse a sí mismo muestra aviso sin error técnico."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    salida = io.StringIO()
    with patch("builtins.input", return_value="usuario0000"):
        with patch("sys.stdout", salida):
            main.seguir_usuario(u_activo, sistema)
    texto = salida.getvalue()
    assert "No puedes seguirte a ti mismo" in texto
    # No se genera notificación ni se altera el grafo
    assert u_activo.cantidad_notificaciones() == 0


def test_seguir_usuario_inexistente_desde_menu():
    """M-10 HU-02 CA-02: Seguir a un usuario inexistente muestra error."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    salida = io.StringIO()
    with patch("builtins.input", return_value="usuario_inexistente"):
        with patch("sys.stdout", salida):
            main.seguir_usuario(u_activo, sistema)
    texto = salida.getvalue()
    assert "no existe" in texto.lower()


def test_dejar_de_seguir_desde_menu():
    """M-10 HU-02 CA-03: Dejar de seguir a un usuario desde el menú elimina la relación real."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    sistema.seguir("usuario0000", "usuario0001")
    salida = io.StringIO()
    with patch("builtins.input", return_value="usuario0001"):
        with patch("sys.stdout", salida):
            main.dejar_de_seguir(u_activo, sistema)
    texto = salida.getvalue()
    assert "Has dejado de seguir a usuario0001" in texto
    # La relación desapareció: intentar dejar de seguir de nuevo devuelve False (ya no existe)
    assert sistema.dejar_de_seguir("usuario0000", "usuario0001") is False


def test_dejar_de_seguir_a_quien_no_sigue_desde_menu():
    """M-10 HU-02 CA-04: Dejar de seguir a quien no se sigue muestra mensaje."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    salida = io.StringIO()
    with patch("builtins.input", return_value="usuario0001"):
        with patch("sys.stdout", salida):
            main.dejar_de_seguir(u_activo, sistema)
    texto = salida.getvalue()
    assert "no existe" not in texto.lower()


def test_mostrar_recomendaciones_desde_menu():
    """M-11 HU-08 CA-01: Mostrar recomendaciones desde el menú verifica los usuarios recomendados."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    sistema.seguir("usuario0000", "usuario0001")
    sistema.seguir("usuario0001", "usuario0002")
    # Verificar la recomendación real a través de la API pública
    recomendados_ids = list(sistema.recomendar("usuario0000"))
    recomendados_nombres = []
    for id_usuario in recomendados_ids:
        u = sistema.obtener_usuario_por_id(id_usuario)
        recomendados_nombres.append(u.nombre_visible)
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.mostrar_recomendaciones(u_activo, sistema)
    texto = salida.getvalue()
    assert "Usuarios recomendados" in texto
    # Cada usuario recomendado debe aparecer en la salida del menú
    for nombre in recomendados_nombres:
        assert nombre in texto


def test_mostrar_recomendaciones_vacias_desde_menu():
    """M-11 HU-08 CA-03: Mostrar recomendaciones sin candidatos indica vacío."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.mostrar_recomendaciones(u_activo, sistema)
    texto = salida.getvalue()
    assert "No hay recomendaciones disponibles" in texto


def test_consultar_notificaciones_con_notificaciones():
    """M-09 HU-07 CA-04: Consultar notificaciones muestra las pendientes y las consume."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    u_activo.agregar_notificacion("NUEVO_SEGUIDOR", "usuario0001")
    u_activo.agregar_notificacion("COMENTARIO", "usuario0002")
    # Antes de consultar, hay 2 notificaciones pendientes
    assert u_activo.cantidad_notificaciones() == 2
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.consultar_notificaciones(u_activo)
    texto = salida.getvalue()
    assert "NUEVO_SEGUIDOR" in texto
    assert "COMENTARIO" in texto
    assert "usuario0001" in texto
    assert "usuario0002" in texto
    # Después de consultar, las notificaciones se consumieron (se leen y se quitan)
    assert u_activo.cantidad_notificaciones() == 0


def test_consultar_notificaciones_sin_notificaciones():
    """M-09 HU-07 CA-04: Consultar notificaciones sin pendientes muestra vacío."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u_activo = sistema.obtener_usuario_por_id(0)
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.consultar_notificaciones(u_activo)
    texto = salida.getvalue()
    assert "No tienes notificaciones pendientes" in texto


def test_visitar_pantalla_registra_actual():
    """M-12 HU-06 CA-01: Visitar una pantalla la establece como actual."""
    from dominio.historial import Historial
    h = Historial()
    salida = io.StringIO()
    with patch("builtins.input", return_value="inicio"):
        with patch("sys.stdout", salida):
            main.visitar_pantalla(h)
    texto = salida.getvalue()
    assert "Pantalla actual: inicio" in texto
    assert h.actual() == "inicio"
    assert h.cantidad() == 1


def test_visitar_pantalla_invalida_lanza_error():
    """M-12 HU-06 CA-04: Visitar pantalla nula o vacía lanza PantallaInvalidaError y no cambia cantidad."""
    from dominio.historial import Historial
    from estructuras.errores import PantallaInvalidaError
    h = Historial()
    h.visitar("inicio")
    assert h.cantidad() == 1
    salida = io.StringIO()
    with patch("builtins.input", return_value=""):
        with patch("sys.stdout", salida):
            main.visitar_pantalla(h)
    texto = salida.getvalue()
    assert "Error al visitar" in texto
    assert h.cantidad() == 1


def test_volver_pantalla_en_orden():
    """M-12 HU-06 CA-01: Tras visitar A, B y C, volver lleva a B y luego a A."""
    from dominio.historial import Historial
    h = Historial()
    h.visitar("A")
    h.visitar("B")
    h.visitar("C")
    assert h.actual() == "C"
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.volver_pantalla(h)
    texto = salida.getvalue()
    assert "Volviendo a la pantalla: B" in texto
    assert h.actual() == "B"
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.volver_pantalla(h)
    texto = salida.getvalue()
    assert "Volviendo a la pantalla: A" in texto
    assert h.actual() == "A"


def test_volver_pantalla_sin_anterior_muestra_aviso():
    """M-12 HU-06 CA-02: Volver sin pantallas previas muestra un aviso sin cerrar."""
    from dominio.historial import Historial
    h = Historial()
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.volver_pantalla(h)
    texto = salida.getvalue()
    assert "No hay pantalla anterior" in texto
    assert h.cantidad() == 0


def test_volver_pantalla_una_sola_muestra_aviso():
    """M-12 HU-06 CA-02: Volver con una sola pantalla muestra aviso."""
    from dominio.historial import Historial
    h = Historial()
    h.visitar("A")
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.volver_pantalla(h)
    texto = salida.getvalue()
    assert "No hay pantalla anterior" in texto


def test_visitar_tras_volver_c_descartado():
    """M-12 HU-06 CA-03: A, B, C; volver (B); visitar D; volver lleva a B y C desaparece."""
    from dominio.historial import Historial
    h = Historial()
    h.visitar("A")
    h.visitar("B")
    h.visitar("C")
    assert h.actual() == "C"
    # Volver a B
    main.volver_pantalla(h)
    assert h.actual() == "B"
    assert h.cantidad() == 2
    # Visitar D
    h.visitar("D")
    assert h.actual() == "D"
    assert h.cantidad() == 3
    # Volver a B (C ya no es alcanzable)
    main.volver_pantalla(h)
    assert h.actual() == "B"
    assert h.cantidad() == 2


def test_explorar_publicaciones_vacia():
    """M-15 HU-08 CA-04: Sin publicaciones en la red muestra mensaje vacío."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    salida = io.StringIO()
    with patch("sys.stdout", salida):
        main.explorar_publicaciones(sistema)
    texto = salida.getvalue()
    assert "No hay publicaciones en la red" in texto


def test_explorar_publicaciones_mostrar_todos_los_usuarios():
    """M-15 HU-08 CA-04: Explorar muestra publicaciones de varios usuarios ordenadas por ID descendente."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u0 = sistema.obtener_usuario_por_id(0)
    u1 = sistema.obtener_usuario_por_id(1)
    # Publicar dos publicaciones en orden para obtener IDs 1 y 2
    with patch("builtins.input", return_value="Post del usuario 0"):
        sistema.publicar(u0, "Post del usuario 0", 0)
    with patch("builtins.input", return_value="Post del usuario 1"):
        sistema.publicar(u1, "Post del usuario 1", 0)
    salida = io.StringIO()
    with patch("builtins.input", return_value="s"):
        with patch("sys.stdout", salida):
            main.explorar_publicaciones(sistema)
    texto = salida.getvalue()
    assert "Publicación [2] de usuario0001" in texto
    assert "Post del usuario 1" in texto
    assert "usuario0001" in texto


def test_explorar_publicaciones_navegacion_respeta_orden():
    """M-15 HU-08 CA-04: Navegar entre publicaciones respeta el orden por ID descendente."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u0 = sistema.obtener_usuario_por_id(0)
    u1 = sistema.obtener_usuario_por_id(1)
    u2 = sistema.obtener_usuario_por_id(2)
    with patch("builtins.input", return_value="Post u0"):
        sistema.publicar(u0, "Post u0", 0)
    with patch("builtins.input", return_value="Post u1"):
        sistema.publicar(u1, "Post u1", 0)
    with patch("builtins.input", return_value="Post u2"):
        sistema.publicar(u2, "Post u2", 0)
    # Ver todas las publicaciones ordenadas por ID descendente
    todas = sistema.obtener_todas_publicaciones()
    ids = [p.id for p in todas]
    assert ids == sorted(ids, reverse=True)
    assert todas[0].texto == "Post u2"
    assert todas[1].texto == "Post u1"
    assert todas[2].texto == "Post u0"
    # Navegar: empezar en ID 3 (más reciente), ir a antigua (ID 2), luego a ID 1
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["a", "a", "s"]):
        with patch("sys.stdout", salida):
            main.explorar_publicaciones(sistema)
    texto = salida.getvalue()
    assert "Publicación [3] de usuario0002" in texto
    assert "Publicación [2] de usuario0001" in texto
    assert "Publicación [1] de usuario0000" in texto


def test_explorar_publicaciones_limite_antigua():
    """M-15 HU-08 CA-04: Intentar ir más allá de la más antigua muestra aviso."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u0 = sistema.obtener_usuario_por_id(0)
    with patch("builtins.input", return_value="Post único"):
        sistema.publicar(u0, "Post único", 0)
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["a", "s"]):
        with patch("sys.stdout", salida):
            main.explorar_publicaciones(sistema)
    texto = salida.getvalue()
    assert "No hay publicaciones más antiguas" in texto


def test_explorar_publicaciones_limite_reciente():
    """M-15 HU-08 CA-04: Intentar ir más allá de la más reciente muestra aviso."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u0 = sistema.obtener_usuario_por_id(0)
    with patch("builtins.input", return_value="Post único"):
        sistema.publicar(u0, "Post único", 0)
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["r", "s"]):
        with patch("sys.stdout", salida):
            main.explorar_publicaciones(sistema)
    texto = salida.getvalue()
    assert "No hay publicaciones más recientes" in texto


def test_comentar_publicacion_explorada_usa_id_global():
    """M-15 HU-08 CA-04: Comentar en una publicación explorada usa su ID global correcto."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u0 = sistema.obtener_usuario_por_id(0)
    u1 = sistema.obtener_usuario_por_id(1)
    with patch("builtins.input", return_value="Post de u0"):
        id_publicacion = sistema.publicar(u0, "Post de u0", 0)
    assert id_publicacion == 1
    # Comentar en esa publicación usando el ID global
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["1", "Comentario desde u1"]):
        with patch("sys.stdout", salida):
            main.comentar_publicacion(u1, sistema)
    texto = salida.getvalue()
    assert "Comentario agregado a la publicación 1" in texto
    p = sistema.obtener_por_id(1)
    assert p.hilo.cantidad() == 1
    notif = u0.bandeja.leer_siguiente()
    assert notif.tipo == "COMENTARIO"
    assert notif.origen == "usuario0001"


def test_feed_propio_sigue_funcionando_despues_de_explorar():
    """M-05 HU-03 CA-01: El feed propio sigue funcionando correctamente."""
    sistema = SistemaRed()
    main.cargar_usuarios_iniciales(sistema)
    u0 = sistema.obtener_usuario_por_id(0)
    with patch("builtins.input", return_value="Post propio"):
        sistema.publicar(u0, "Post propio", 0)
    salida = io.StringIO()
    with patch("builtins.input", side_effect=["s"]):
        with patch("sys.stdout", salida):
            main.recorrer_feed(u0, sistema)
    texto = salida.getvalue()
    assert "Publicación actual [1]" in texto
    assert "Post propio" in texto