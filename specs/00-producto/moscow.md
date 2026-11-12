# Priorización MoSCoW — Red social UCC

## Capacidad
Datos pendientes: se requieren horas por semana y número de semanas para aplicar la fórmula del profesor (`h/semana × semanas − 20 % de imprevistos = capacidad real`). No se han definido estos valores todavía.

Motivo del porcentaje del 20 %: cubre configuración del entorno, depuración de errores inesperados, reescritura por cambio de especificación y preparación de entregas.

## Must (suman 8 h de <capacidad> h reales)
| Historia | Horas | Por qué es Must | Componente |
|----------|-------|-----------------|------------|
| HU-01 Generar usuarios sintéticos reproducibles | 0,75 | Mínimo del dominio: sin usuarios no hay red | generador en dominio/ |
| HU-02 Seguir y dejar de seguir | 1 | Mínimo del dominio: núcleo de las relaciones de la red | grafo (lista de adyacencia) |
| HU-03 Publicar y ver el feed de un usuario | 1,25 | Mínimo del dominio: funcionalidad principal de publicación | lista doble |
| HU-04 Comentar y responder en hilos anidados | 1,25 | Mínimo del dominio: interacción entre usuarios | árbol general |
| HU-05 Buscar usuarios por nombre | 1,25 | Mínimo del dominio: descubrimiento de usuarios | BST |
| HU-06 Volver a la pantalla anterior | 0,75 | Mínimo del dominio: navegación básica | pila |
| HU-07 Recibir y leer notificaciones | 0,75 | Mínimo del dominio: retroalimentación de acciones | cola |
| HU-08 Personas que quizá conozcas | 1 | Mínimo del dominio: recomendación de contactos | BFS sobre el grafo |

## Should
| Historia | Horas | Condición para entrar |
|----------|-------|----------------------|
| Cambiar el índice de BST a AVL | 1,5 | Solo si sobra capacidad después de completar todos los Must |

## Could
| Historia | Horas |
|----------|-------|
| Medición empírica de tiempos con n creciente | por definir |

## Won't (esta versión no)
| Historia | Razón |
|----------|-------|
| Cadena de conexión más corta con A* | Opcional en el enunciado, no es mínimo del dominio |
| Notificaciones con prioridad | Todas se leen en orden de llegada |
| Búsqueda por prefijo | La búsqueda es por nombre exacto |
| Guardar datos en disco | Los datos se regeneran con la semilla |

## Orden de construcción
1. HU-01 Generar usuarios sintéticos reproducibles (necesario antes de cualquier otra operación)
2. HU-02 Seguir y dejar de seguir (base de las relaciones de la red)
3. HU-05 Buscar usuarios por nombre (necesario para seleccionar usuarios en la red)
4. HU-03 Publicar y ver el feed (requiere usuarios existentes)
5. HU-04 Comentar y responder en hilos (requiere publicaciones)
6. HU-07 Recibir y leer notificaciones (requiere acciones de seguimiento)
7. HU-06 Volver a la pantalla anterior (navegación independiente)
8. HU-08 Personas que quizá conozcas (requiere grafo de seguimiento poblado)

## Historial de cambios
| Versión | Fecha | Qué cambió de prioridad | Por qué |
|---------|-------|------------------------|---------|
| 1.0 | 12 nov 2026 | Versión inicial | Adaptación a la plantilla del profesor |
