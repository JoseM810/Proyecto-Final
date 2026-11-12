# Plan técnico — Entidad Usuario
**Especificación de referencia:** spec.md v1.0

## 1. Estructura de datos elegida
La entidad Usuario no implementa una estructura de datos propia; delega el
almacenamiento en dos clases existentes de dominio:
- `Feed` (dominio/feed.py): lista doblemente enlazada con cursor, para las
  publicaciones del usuario.
- `BandejaNotificaciones` (dominio/notificaciones.py): cola enlazada, para las
  notificaciones pendientes del usuario.

Los atributos id, username, nombre_visible y biografía se guardan como
atributos simples de la instancia.

## 2. Alternativas consideradas
| Alternativa | Ventaja | Por qué se descartó |
|---|---|---|
| Almacenar publicaciones y notificaciones directamente en Usuario | Menos clases involucradas | Se reutilizan Feed y BandejaNotificaciones ya implementadas y testeadas, evitando duplicar lógica |
| Usar estructuras nativas de Python (list, dict) | Simplicidad inicial | Violaría el principio 1 de la constitución: estructuras desde cero |

## 3. Complejidad esperada
| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| __init__ | O(1) | O(1) | Asignar atributos y crear Feed y BandejaNotificaciones vacíos |
| publicar | O(1) | O(1) | Delegado en Feed.publicar (insertar al inicio de lista doble) |
| agregar_notificacion | O(1) | O(1) | Delegado en BandejaNotificaciones.agregar (encolar al final) |
| cantidad_notificaciones | O(1) | O(1) | Delegado en BandejaNotificaciones.pendientes (contador) |

## 4. Diseño interno
- Clase Usuario (dominio/usuario.py): agrupa id, username, nombre_visible,
  biografía, feed y bandeja.
- Feed (dominio/feed.py): ya implementado y testeado (soporta HU-03).
- BandejaNotificaciones (dominio/notificaciones.py): ya implementado y
  testeado (soporta HU-07).
- Excepciones PublicacionInvalidaError y NotificacionInvalidaError en
  estructuras/errores.py.
- No se usa list, dict, set ni deque en ningún punto.

## 5. Riesgos técnicos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Que el id de Usuario no coincida con el vértice de RedSeguimiento | Medio | SistemaRed asigna el id desde RedSeguimiento.agregar_usuario() antes de crear el Usuario |
| Que publicar o agregar_notificacion fallen silenciosamente | Bajo | Las excepciones de Feed y BandejaNotificaciones se propagan tal cual |
