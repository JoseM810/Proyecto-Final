# Especificación — Generador de Usuarios
**Versión:** 1.0 · **Fecha:** 12 nov 2026 · **Autor:** Jose Miguel Alvarez Ortega

## 1. Propósito
Genera datos de usuarios reproducibles con semilla fija, para que la red
arranque siempre con los mismos usuarios en el mismo orden. Soporta la
historia HU-01 (datos de prueba reproducibles).

## 2. Fuera de alcance
- Crear objetos Usuario: solo retorna datos (tuplas), no instancias.
- Registrar usuarios en IndiceUsuarios o RedSeguimiento: eso lo hace
  SistemaRed.cargar_desde_generador().
- Guardar los usuarios generados entre ejecuciones: se regeneran con la semilla.

## 3. Operaciones

### `__init__(semilla=42)`
- **Precondiciones esperadas:** semilla es un valor válido para random.Random.
- **Validaciones implementadas:** el constructor no valida la semilla; la almacena directamente. random.Random lanzará su propio error si la semilla no es válida.
- **Postcondiciones:** almacena la semilla para uso posterior.
- **Complejidad:** Tiempo O(1), espacio O(1).

### `generar(cantidad=100)`
- **Precondiciones esperadas:** cantidad es un entero >= 0.
- **Validaciones implementadas:** el método no valida cantidad; si se pasa un entero negativo, range() no itera y retorna una lista vacía. No hay validación explícita.
- **Postcondiciones:** retorna una lista de tuplas (username, nombre_visible, biografia) con nombres únicos y secuenciales (usuario0000, usuario0001, …). Misma semilla produce la misma secuencia.
- **Complejidad:** Tiempo O(n), espacio O(n), con n la cantidad de usuarios.

## 4. Invariantes
- INV-01: los nombres de usuario son únicos dentro de una generación.
- INV-02: misma semilla produce la misma secuencia en el mismo orden.
- INV-03: los nombres siguen el patrón usuario{i:04d}.

## 5. Criterios de aceptación
| ID | Criterio | Verificable mediante |
|-------|-----------------------------------------------------------|---------------------------|
| CA-01 | Misma semilla genera mismos usuarios en mismo orden | test_generador_produce_mismos_usuarios_con_misma_semilla |
| CA-02 | Se generan al menos 100 usuarios, cada uno con nombre único | test_generador_produce_al_menos_100_usuarios, test_generador_nombres_unicos |

## 6. Casos extremos considerados
- Cantidad personalizable (no solo 100).
- Semillas diferentes producen biografías diferentes (por el sufijo aleatorio).
- Cada entrada tiene username, nombre_visible y biografía no vacíos.

## 7. Historial de cambios
| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 12 nov 2026 | Versión inicial | — |
