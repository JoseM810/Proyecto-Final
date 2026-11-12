# Plan técnico — Sistema de Red Social
**Especificación de referencia:** spec.md v1.0

## 1. Estructura de datos elegida
- `IndiceUsuarios` (dominio/indice_usuarios.py): ArbolBST por nombre, para
  buscar usuarios por username en O(h).
- `RedSeguimiento` (dominio/red.py): GrafoDirigido con listas de adyacencia,
  para relaciones de seguimiento en O(g).
- `Usuario` (dominio/usuario.py): entidad con Feed y BandejaNotificaciones.
- `_usuarios_por_id`: lista de Python como soporte interno, indexada por el
  ID entero del usuario (vértice del grafo). Este uso de `list` se justifica
  porque RedSeguimiento ya usa `list` internamente (_listas) para acceder a
  vértices por número en O(1), como documenta su plan.md.

## 2. Alternativas consideradas
| Alternativa | Ventaja | Por qué se descartó |
|---|---|---|
| Un solo grafo que almacene objetos Usuario | Menos clases | RedSeguimiento ya está implementado y testeado; no se modifica para no romper sus pruebas |
| Usar dict para nombre → usuario | Búsqueda O(1) | Violaría el principio 1 de la constitución; se usa ArbolBST existente |
| No usar _usuarios_por_id, buscar por nombre siempre | Menos memoria | Acceder por ID es O(1) y se necesita para operaciones del grafo |

## 3. Complejidad esperada
| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| registrar_usuario | O(h) | O(1) | RedSeguimiento.agregar_usuario O(1) + IndiceUsuarios.agregar O(h) |
| buscar_usuario_por_nombre | O(h) | O(1) | IndiceUsuarios.buscar (BST) |
| obtener_usuario_por_id | O(1) | O(1) | Acceso por índice en lista |
| seguir | O(h + g) | O(1) | Dos búsquedas BST O(h) + RedSeguimiento.seguir O(g) |
| dejar_de_seguir | O(h + g) | O(1) | Dos búsquedas BST O(h) + RedSeguimiento.dejar_de_seguir O(g) |
| listar_usuarios | O(n) | O(h) | IndiceUsuarios.listar (recorrido en orden) |
| cantidad_usuarios | O(1) | O(1) | IndiceUsuarios.cantidad (contador) |
| cargar_desde_generador | O(n² + n·h) | O(n) | Primera pasada valida duplicados con `in` sobre lista (O(n²)); segunda pasada registra n usuarios a O(h) cada uno (O(n·h)) |

## 4. Diseño interno
- Clase SistemaRed (dominio/sistema_red.py): orquestador que une los tres
  componentes existentes.
- `_indice`: IndiceUsuarios para nombre → Usuario.
- `_red`: RedSeguimiento para ID → relaciones de seguimiento.
- `_usuarios_por_id`: lista indexada por ID entero para acceso O(1).
- `cargar_desde_generador` valida duplicados en una primera pasada antes de
  registrar, evitando carga parcial si hay nombres repetidos.
- No se usan list, dict, set ni deque como sustitutos de estructuras propias.

## 5. Riesgos técnicos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Que _usuarios_por_id tenga None en posiciones intermedias | Medio | IDs son consecutivos desde 0; no se esperan huecos |
| Que cargar_desde_generador falle parcialmente | Medio | Validación de duplicados antes de registrar cualquier usuario |
| Que h (altura BST) sea grande con nombres ordenados | Medio | Heredado de ArbolBST; se podría migrar a AVL (Should en moscow.md) |
