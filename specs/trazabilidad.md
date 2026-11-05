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