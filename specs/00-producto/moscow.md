# Priorización MoSCoW — Red social UCC

## Capacidad
- Días disponibles: 7 (4 al 11 de nov) × 2 h = 14 h
- Reservado: documentos finales (ANALISIS, BITACORA, README, informe) 3 h,
  integración en main.py y pruebas finales 1 h, margen 1 h = 5 h
- **Capacidad para historias: 9 h**

## Must (8 h)
| Historia | Estimado | Componente |
|----------|----------|------------|
| HU-01 Usuarios reproducibles | 0,75 h | generador en dominio/ |
| HU-02 Seguir y dejar de seguir | 1 h | grafo (lista de adyacencia) |
| HU-03 Feed con ← → | 1,25 h | lista doble |
| HU-04 Hilos de comentarios | 1,25 h | árbol general |
| HU-05 Buscar | 1,25 h | BST |
| HU-06 Volver a la pantalla anterior | 0,75 h | pila |
| HU-07 Notificaciones | 0,75 h | cola |
| HU-08 Quizá conozcas | 1 h | BFS sobre el grafo |

## Should (1,5 h, solo si sobra tiempo)
- Cambiar el índice de BST a AVL (cambia plan.md y código; spec.md no)

## Could
- Medición empírica de tiempos con n creciente (para ANALISIS.md)

## Won't (por ahora)
- Cadena de conexión con A*: opcional en el enunciado y no cabe en la capacidad
- Notificaciones con prioridad: todas se leen en orden de llegada
- Búsqueda por prefijo: la búsqueda es por nombre exacto
- Guardar datos en disco: los datos se regeneran con la semilla

## Riesgo
Los estimados son míos y pueden fallar. Si un componente se pasa del doble,
se baja el Should y se avisa en este archivo.