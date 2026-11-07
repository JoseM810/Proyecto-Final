# Trazabilidad

| Componente | Criterio | Prueba | Código |
|---|---|---|---|
| 01-historial | CA-01 | test_volver_en_orden | dominio/historial.py · volver() |
| 01-historial | CA-02 | test_volver_sin_anterior | dominio/historial.py · volver() |
| 01-historial | CA-03 | test_visitar_tras_volver | dominio/historial.py · volver() |
| 01-historial | CA-04 | test_visitar_invalida_lanza_error_y_no_cambia_cantidad | dominio/historial.py · visitar() |
| 02-notificaciones | CA-01 | test_leer_en_orden_de_llegada | dominio/notificaciones.py · leer_siguiente() |
| 02-notificaciones | CA-02 | test_leer_sin_pendientes | dominio/notificaciones.py · leer_siguiente() |
| 02-notificaciones | CA-03 | test_leer_la_quita | dominio/notificaciones.py · leer_siguiente() |
| 02-notificaciones | CA-04 | test_agregar_invalida_lanza_error_y_no_cambia_pendientes | dominio/notificaciones.py · agregar() |
| 03-feed | CA-01 | test_la_mas_reciente_aparece_primero | dominio/feed.py · publicar(), avanzar() |
| 03-feed | CA-02 | test_avanzar_y_retroceder | dominio/feed.py · avanzar(), retroceder() |
| 03-feed | CA-03 | test_limites_del_feed | dominio/feed.py · avanzar(), retroceder() |
| 03-feed | CA-04 | test_feed_vacio | dominio/feed.py · actual(), cantidad() |
| 03-feed | CA-05 | test_publicar_invalida | dominio/feed.py · publicar() |
| 04-comentarios | CA-01 | test_respuesta_tiene_profundidad_del_padre_mas_uno, test_respuesta_aparece_justo_despues_del_padre | dominio/hilo_comentarios.py · responder(), recorrer() |
| 04-comentarios | CA-02 | test_hilo_en_preorden | dominio/hilo_comentarios.py · recorrer() |
| 04-comentarios | CA-03 | test_responder_inexistente | dominio/hilo_comentarios.py · responder(), _buscar() |
| 04-comentarios | CA-04 | test_respuestas_en_orden_de_llegada | dominio/hilo_comentarios.py · recorrer() |
| 04-comentarios | CA-05 | test_comentario_invalido | dominio/hilo_comentarios.py · comentar(), _validar() |
| 04-comentarios | CA-06 | test_hilo_vacio | dominio/hilo_comentarios.py · recorrer(), cantidad() |
| 04-comentarios | CA-07 | test_obtener_comentario | dominio/hilo_comentarios.py · obtener(), _buscar() |
| 05-indice-usuarios | CA-01 | test_buscar_existente | dominio/indice_usuarios.py · agregar(), buscar() |
| 05-indice-usuarios | CA-02 | test_buscar_inexistente | dominio/indice_usuarios.py · buscar() |
| 05-indice-usuarios | CA-03 | test_listar_en_orden | dominio/indice_usuarios.py · listar() |
| 05-indice-usuarios | CA-04 | test_agregar_duplicado | dominio/indice_usuarios.py · agregar() |
| 05-indice-usuarios | CA-05 | test_agregar_invalido | dominio/indice_usuarios.py · agregar() |
| 05-indice-usuarios | CA-06 | test_indice_vacio | dominio/indice_usuarios.py · listar(), cantidad() |
| 05-indice-usuarios | CA-07 | test_nombres_ya_ordenados | dominio/indice_usuarios.py · buscar(), listar() |
| 06-red | CA-01 | test_ids_consecutivos | dominio/red.py · agregar_usuario() |
| 06-red | CA-02 | test_seguir_y_aparece | dominio/red.py · seguir(), sigue(), seguidos() |
| 06-red | CA-03 | test_seguir_repetido | dominio/red.py · seguir() |
| 06-red | CA-04 | test_seguir_a_si_mismo | dominio/red.py · seguir() |
| 06-red | CA-05 | test_relacion_dirigida | dominio/red.py · sigue() |
| 06-red | CA-06 | test_dejar_de_seguir | dominio/red.py · dejar_de_seguir() |
| 06-red | CA-07 | test_usuario_inexistente | dominio/red.py · _validar() |
| 06-red | CA-08 | test_seguidos_en_orden | dominio/red.py · seguidos() |
| 06-red | CA-09 | test_recomendar_a_dos_saltos | dominio/red.py · recomendar() |
| 06-red | CA-10 | test_recomendar_sin_repetidos_ni_conocidos | dominio/red.py · recomendar() |
| 06-red | CA-11 | test_recomendar_sin_candidatos | dominio/red.py · recomendar() |
| 06-red | CA-12 | test_recomendar_orden | dominio/red.py · recomendar() |
| 03-feed | CA-06 | test_buscar_por_palabra | dominio/feed.py · buscar() |
| 03-feed | CA-07 | test_buscar_sin_coincidencias | dominio/feed.py · buscar() |
| 03-feed | CA-08 | test_buscar_palabra_invalida | dominio/feed.py · buscar() |
| 03-feed | CA-09 | test_buscar_no_modifica_el_feed | dominio/feed.py · buscar() |g