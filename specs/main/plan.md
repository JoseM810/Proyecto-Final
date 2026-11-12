# Plan técnico — Interfaz de consola (main.py)
**Especificación de referencia:** spec.md v1.0

## 1. Estructura de datos elegida
main.py no implementa estructuras de datos propias; delega en los componentes
de dominio ya implementados:

| Componente | Clase | Rol en la interfaz |
|---|---|---|
| SistemaRed | dominio.sistema_red.SistemaRed | Orquestación principal: registrar, buscar, seguir, dejar de seguir, listar, recomendar, cargar desde generador |
| GeneradorUsuarios | dominio.generador_usuarios.GeneradorUsuarios | Generar 100 usuarios con semilla fija al iniciar |
| Usuario | dominio.usuario.Usuario | Entidad del usuario activo (feed, bandeja, id, nombre) |
| Feed | dominio.feed.Feed | Publicaciones del usuario activo (avanzar, retroceder, buscar) |
| Historial | dominio.historial.Historial | Navegación de pantallas (visitar, volver) |
| RedSeguimiento | dominio.red.RedSeguimiento | Relaciones de seguimiento (usado internamente por SistemaRed) |
| IndiceUsuarios | dominio.indice_usuarios.IndiceUsuarios | Búsqueda de usuarios por nombre (usado internamente por SistemaRed) |
| BandejaNotificaciones | dominio.notificaciones.BandejaNotificaciones | Notificaciones del usuario activo (usado internamente por Usuario) |
| HiloComentarios | dominio.hilo_comentarios.HiloComentarios | Comentarios y respuestas en árbol general por publicación |

El uso de `list` en Python se limita a acumular opciones de menú y datos de
salida; no sustituye a ninguna estructura de datos propia de la red.

## 2. Alternativas consideradas
| Alternativa | Ventaja | Por qué se descartó |
|---|---|---|
| Interfaz web (HTML/CSS/JS) | Más atractiva visualmente | Violaría la restricción de la Constitución: "Interfaz: consola" |
| Framework de CLI (click, typer) | Menos código de menú | Agregaría dependencia externa no permitida (solo pytest y matplotlib) |
| Menú con input() simple | Sin dependencias, cumple la Constitución | Seleccionada |

## 3. Complejidad esperada
| Operación | Tiempo | Espacio | Justificación |
|---|---|---|---|
| cargar_usuarios_iniciales | O(n·h) | O(n) | n registros a O(h) cada uno en IndiceUsuarios (documentado en specs/sistema-red/plan.md) |
| seleccionar_usuario | O(h) | O(1) | SistemaRed.buscar_usuario_por_nombre (BST) |
| publicar | O(1) | O(1) | Usuario.publicar delegado en Feed.publicar |
| recorrer_feed (avanzar/retroceder) | O(1) | O(1) | ListaDoble con cursor |
| seguir_usuario | O(h + g) | O(1) | SistemaRed.seguir |
| dejar_de_seguir_usuario | O(h + g) | O(1) | SistemaRed.dejar_de_seguir |
| buscar_usuario | O(h) | O(1) | SistemaRed.buscar_usuario_por_nombre (BST) |
| listar_usuarios | O(n) | O(h) | SistemaRed.listar_usuarios (recorrido en orden del BST) |
| mostrar_recomendaciones | O(V + E) | O(V) | RedSeguimiento.recomendar (BFS 2 saltos) |
| consultar_notificaciones | O(1) por notificación | O(1) | BandejaNotificaciones.leer_siguiente |
| visitar_pantalla | O(1) | O(1) | Historial.visitar (apilar) |
| volver_pantalla_anterior | O(1) | O(1) | Historial.volver (desapilar) |
| comentar_publicacion | O(1) | O(1) | HiloComentarios.comentar() |
| responder_comentario | O(1) | O(1) | HiloComentarios.responder() |
| ver_comentarios_publicacion | O(n) | O(n) | HiloComentarios.recorrer() (n comentarios) |

## 4. Diseño interno
- `main()`: función principal con bucle `while` que muestra el menú y procesa
  la opción elegida. Todo el estado vive como variables locales de `main()`
  y se pasa como parámetro a las funciones auxiliares.
- `usuario_activo`: variable local de `main()` que almacena el objeto Usuario
  actualmente seleccionado (None al inicio).
- `historial`: objeto Historial creado dentro de `main()`, empieza vacío
  (0 pantallas). Se pasa como parámetro a las funciones de navegación.
- `sistema`: objeto SistemaRed creado dentro de `main()`.
- Cada opción del menú llama al método correspondiente de SistemaRed o de
  los componentes de dominio, y muestra el resultado por consola.
- El flujo de arranque: crear SistemaRed → cargar 100 usuarios con
  GeneradorUsuarios(42).generar(100) → SistemaRed.cargar_desde_generador()
  → mostrar menú principal.
- No se usa `list`, `dict`, `set` ni `deque` como sustituto de estructuras
  propias de la red.

## 5. Riesgos técnicos
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Que cargar_usuarios_iniciales falle por nombre duplicado | Medio | GeneradorUsuarios genera nombres únicos por construcción (usuario{i:04d}) |
| Que el usuario seleccione una opción inválida | Bajo | Validar entrada y mostrar mensaje de error sin salir del bucle |
| Que no haya usuario activo al intentar publicar | Medio | Verificar que usuario_activo no sea None antes de publicar (INV-01) |
| Que el Historial quede vacío tras volver demasiado | Bajo | Historial empieza vacío y solo crece con visitar(); volver necesita >= 2 pantallas |
| Que HiloComentarios no esté vinculado a publicaciones | Medio | HiloComentarios existe isolado; se requiere asociar comentarios a publicaciones específicas antes de mostrar |
