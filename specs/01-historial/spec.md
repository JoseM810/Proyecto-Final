# Especificación — Historial de navegación
**Versión:** 1.0 · **Fecha:** 4 nov 2026 · **Autor:** Jose Miguel Alavarez Ortegagi

## 1. Propósito
Recuerda las pantallas que visita la persona en la consola para que pueda
volver a la anterior. Soporta la historia HU-06.

## 2. Fuera de alcance
- Avanzar de nuevo a una pantalla de la que se volvió
- Guardar el historial entre ejecuciones
- Historiales separados por usuario (hay uno por sesión)

## 3. Operaciones

### `visitar(pantalla)`
- **Precondiciones:** pantalla es un texto no vacío
- **Postcondiciones:** pantalla es la actual; la actual anterior queda
  alcanzable con volver()
- **Errores:** PantallaInvalidaError si pantalla es nula o vacía

### `volver()`
- **Precondiciones:** existe una pantalla anterior a la actual
- **Postcondiciones:** la actual pasa a ser la inmediatamente anterior; la
  que se abandonó deja de ser alcanzable. Devuelve la nueva actual.
- **Errores:** NadaAtrasError si no existe pantalla anterior

### `actual()`
- **Precondiciones:** ninguna
- **Postcondiciones:** devuelve la pantalla actual, o None si nunca se
  visitó ninguna. No modifica el historial.

### `cantidad()`
- **Postcondiciones:** devuelve cuántas pantallas son alcanzables,
  contando la actual.

## 4. Invariantes
- INV-01: cantidad() >= 0 en todo momento
- INV-02: actual() es None si y solo si cantidad() es 0

## 5. Criterios de aceptación
| ID | Criterio | Verificable mediante |
|-------|-----------------------------------------------------------|---------------------------|
| CA-01 | Tras visitar A, B y C, volver lleva a B y luego a A | test_volver_en_orden |
| CA-02 | Volver con cero o una sola pantalla lanza NadaAtrasError | test_volver_sin_anterior |
| CA-03 | Tras visitar A, B, C; volver (B); visitar D; volver lleva a B y C ya no es alcanzable | test_visitar_tras_volver |
| CA-04 | Visitar una pantalla nula o vacía lanza PantallaInvalidaError y no cambia cantidad() | test_visitar_invalida |

## 6. Casos extremos considerados
- Sin pantallas · una sola pantalla · visitar la misma pantalla dos veces
  seguidas (se acepta y cuenta como dos visitas) · muchas visitas seguidas

## 7. Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 4 nov 2026 | Versión inicial | — |