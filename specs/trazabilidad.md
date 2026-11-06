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