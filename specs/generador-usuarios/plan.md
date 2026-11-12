# Plan técnico — Generador de Usuarios
**Especificación de referencia:** spec.md v1.0

## 1. Estructura de datos elegida
Lista de tuplas (username, nombre_visible, biografía). Se usa `list` como
soporte interno para acumular los datos generados antes de retornarlos. Este
uso se justifica porque:
- El generador no implementa una estructura de datos de la red; solo produce
  datos de entrada para SistemaRed.cargar_desde_generador().
- La lista se descarta tras la carga; no persiste como estructura de la red.

## 2. Alternativas consideradas
| Alternativa | Ventaja | Por qué se descartó |
|---|---|---|
| Generador que devuelve un iterador | Menos memoria para muchas generaciones | Se necesita la lista completa para cargar en SistemaRed de una vez |
| Devolver objetos Usuario directamente | Menos código en SistemaRed | El generador no debería depender de la clase Usuario; separa generación de registro |

## 3. Complejidad esperada
| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| __init__ | O(1) | O(1) | Almacenar la semilla |
| generar | O(n) | O(n) | Iterar n veces creando tuplas y acumulando en lista |

## 4. Diseño interno
- Clase GeneradorUsuarios (dominio/generador_usuarios.py): almacena semilla y
  genera datos con random.Random(semilla).
- random.Random: generador independiente de la semilla global de Python, para
  garantizar reproducibilidad sin afectar otros usos de random.
- Cada tupla contiene (username, nombre_visible, biografía) con formato
  usuario{i:04d}.
- No se usa list, dict, set ni deque como sustituto de estructuras de la red.

## 5. Riesgos técnicos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Que random.Random no sea reproducible | Medio | Se usa siempre con la misma semilla explícita; probado en CA-01 |
| Que los nombres no sean únicos | Medio | El patrón usuario{i:04d} garantiza unicidad por construcción |
