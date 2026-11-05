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