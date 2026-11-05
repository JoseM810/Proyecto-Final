# Plan técnico — Notificaciones pendientes
**Especificación de referencia:** spec.md v1.0

## 1. Estructura de datos elegida
Cola enlazada con referencias al frente y al final. Las notificaciones se
leen en el orden en que llegaron: agregar enlaza al final y leer saca del
frente. Con las dos referencias, ambas operaciones son O(1).

## 2. Alternativas consideradas
| Alternativa | Ventaja | Por qué se descartó |
|---|---|---|
| Arreglo dinámico | Simple | Sacar del inicio obliga a correr todos los elementos: O(n) por cada notificación leída |
| Lista enlazada con solo referencia al inicio | Menos atributos | Agregar al final exige recorrerla completa: O(n) |
| Cola de prioridad | Permitiría urgentes | La spec deja fuera la prioridad; costaría O(log n) sin dar nada |

## 3. Complejidad esperada
| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| agregar | O(1) | O(1) | Enlazar un nodo tras el final y mover el final |
| leer_siguiente | O(1) | O(1) | Quitar el nodo del frente y mover el frente |
| pendientes | O(1) | O(1) | Se lleva un contador |

## 4. Diseño interno
- Reutiliza Nodo (estructuras/nodo.py)
- ColaEnlazada (estructuras/cola.py): frente, final y tamanio; operaciones
  encolar, desencolar, ver_frente, tamanio
- Notificacion: pequeño registro con tipo y origen (dominio/notificaciones.py)
- BandejaNotificaciones (dominio/notificaciones.py): valida tipo y origen y
  usa una ColaEnlazada
- Invariante de representación: frente es None si y solo si final es None
  si y solo si tamanio es 0; tamanio = nodos alcanzables desde el frente
- No se usa list, dict, set ni deque

## 5. Riesgos técnicos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Al desencolar el último nodo, final queda apuntando a un nodo viejo | Alto | Poner final en None cuando frente quede en None; hay prueba de agregar tras vaciar |
| Que el contador se desincronice de los nodos | Medio | Solo encolar y desencolar lo modifican |