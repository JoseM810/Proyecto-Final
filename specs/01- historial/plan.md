# Plan técnico — Historial de navegación
**Especificación de referencia:** spec.md v1.0

## 1. Estructura de datos elegida
Pila enlazada. Cada nodo guarda una pantalla y una referencia al nodo que
quedó debajo. La pantalla actual es siempre el tope. Visitar apila una
pantalla nueva; volver desapila el tope y la anterior pasa a ser la actual.
Esto cubre CA-03 sin código extra: lo que se abandona al volver ya no está en
la pila, así que no puede alcanzarse.

## 2. Alternativas consideradas
| Alternativa | Ventaja | Por qué se descartó |
|---|---|---|
| Lista doble + cursor | Permitiría "avanzar" de nuevo | La spec deja fuera avanzar. Además, al visitar tras volver hay que cortar la lista, y eso agrega casos sin ganar costo |
| Arreglo dinámico | Acceso por posición | Apilar es O(1) amortizado, pero al llenarse copia todo (O(n) en ese caso), y no necesito acceso por posición |

## 3. Complejidad esperada
| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| visitar | O(1) | O(1) | Crear un nodo y apuntarlo al tope actual |
| volver | O(1) | O(1) | Mover el tope al nodo de abajo |
| actual | O(1) | O(1) | Leer el tope |
| cantidad | O(1) | O(1) | Se lleva un contador, no se recorre |

## 4. Diseño interno
- Clase Nodo (módulo estructuras/nodo.py, la reutilizo en la cola de
  notificaciones): atributos valor y siguiente
- Clase PilaEnlazada (estructuras/pila.py): tope y tamaño; operaciones
  apilar, desapilar, ver_tope, tamaño
- Clase Historial (dominio/historial.py): usa una PilaEnlazada y aplica
  las reglas de la spec (pantalla válida, volver con al menos dos)
- Excepciones PantallaInvalidaError y NadaAtrasError en estructuras/errores.py
- Invariante de representación: tamaño = número de nodos alcanzables desde el
  tope; tope es None si y solo si tamaño es 0
- No se usa list, dict, set ni deque en ningún punto

## 5. Riesgos técnicos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Que volver() deje el historial vacío al ser llamada con una sola pantalla | Medio | Verificar tamaño >= 2 antes de desapilar; probado en CA-02 |
| Que el contador de tamaño se desincronice de los nodos | Medio | Solo apilar y desapilar lo modifican; hay prueba de INV-01 e INV-02 |