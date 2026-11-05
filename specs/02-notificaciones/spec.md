# Especificación — Notificaciones pendientes
**Versión:** 1.0 · **Fecha:** 4 nov 2026 · **Autor:** Jose Miguel Alvarez Ortega

## 1. Propósito
Guarda las notificaciones que le llegan a una persona de la red (nuevo
seguidor, comentario, respuesta) hasta que las lee. Hay una bandeja por
usuario. Soporta la historia HU-07.

## 2. Fuera de alcance
- Decidir cuándo se genera una notificación (lo hace el dominio al seguir,
  comentar o responder; se verifica en la spec del sistema)
- Notificaciones urgentes o con prioridad: todas son iguales
- Guardar las notificaciones entre ejecuciones

## 3. Operaciones

### `agregar(tipo, origen)`
- **Precondiciones:** tipo es NUEVO_SEGUIDOR, COMENTARIO o RESPUESTA;
  origen es el nombre, no vacío, de quien la causó
- **Postcondiciones:** la notificación queda pendiente, como la más
  reciente de todas
- **Errores:** NotificacionInvalidaError si tipo u origen no cumplen

### `leer_siguiente()`
- **Precondiciones:** ninguna
- **Postcondiciones:** devuelve la notificación pendiente más antigua y
  deja de estar pendiente. Si no hay ninguna, devuelve None y no cambia nada.

### `pendientes()`
- **Postcondiciones:** devuelve cuántas notificaciones siguen sin leer.
  No modifica nada.

## 4. Invariantes
- INV-01: pendientes() >= 0 en todo momento
- INV-02: una notificación leída no vuelve a estar pendiente

## 5. Criterios de aceptación
| ID | Criterio | Verificable mediante |
|-------|--------------------------------------------------------|----------------------------------|
| CA-01 | Las notificaciones se leen en el orden en que llegaron | test_leer_en_orden_de_llegada |
| CA-02 | Leer sin pendientes devuelve None y no lanza error | test_leer_sin_pendientes |
| CA-03 | Leer una notificación la quita: pendientes() baja en uno y no se puede leer otra vez | test_leer_la_quita |
| CA-04 | Agregar con tipo u origen inválido lanza NotificacionInvalidaError y no cambia pendientes() | test_agregar_invalida |

## 6. Casos extremos considerados
- Sin notificaciones · una sola · agregar después de haber leído todas ·
  muchas notificaciones seguidas

## 7. Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 4 nov 2026 | Versión inicial | — |