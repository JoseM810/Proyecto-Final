# Especificación — Sistema Completo (99-sistema)
**Versión:** 1.0 · **Fecha:** 12 nov 2026 · **Autor:** Jose Miguel Alvarez Ortega

## 1. Propósito
Documentar el sistema completo de red social: cómo interactúan los componentes de dominio, cuáles son sus contratos, invariantes globales y criterios de aceptación del sistema. Especifica el conjunto integrado, no cada componente de forma aislada.

## 2. Alcance y fuera de alcance

### Implementado y probado
- Red de seguimiento (seguir, dejar de seguir, recomendaciones BFS a 2 saltos)
- Índice de usuarios (BST por nombre)
- Usuario con feed propio y bandeja de notificaciones
- Generador de usuarios reproducible con semilla fija
- SistemaRed como orquestador de IndiceUsuarios, RedSeguimiento y Usuario
- Feed individual por usuario (publicar, avanzar, retroceder, buscar por palabra)
- Historial de navegación (visitar, volver, pantalla actual)
- Bandeja de notificaciones (agregar, leer siguiente, pendientes)
- Hilos de comentarios (comentar, responder, obtener, recorrer en preorden)

### Pendiente de integración
- Interfaz de consola `main.py` (especificada en specs/main/spec.md, tareas T-01 a T-11 pendientes)
- Asociación de comentarios a publicaciones (HU-04 CA-03 en specs/04-comentarios/tasks.md está Pendiente)
- Notificaciones disparadas por comentario o respuesta (solo se generan al seguir)

### Fuera de alcance (Won't)
- Cadena de conexión más corta con A* (opcional en el enunciado)
- Notificaciones con prioridad (todas se leen en orden de llegada)
- Búsqueda por prefijo (búsqueda por nombre exacto)
- Persistencia en disco (los datos se regeneran con la semilla)
- Interfaz web (HTML, CSS, JavaScript) ni frameworks
- Autenticación ni contraseñas

## 3. Actores del sistema

| Actor | Descripción |
|-------|-------------|
| Usuario de la red | Persona que sigue a otros, publica, comenta, recibe notificaciones y consulta recomendaciones |
| SistemaRed | Orquestador que une IndiceUsuarios, RedSeguimiento y Usuario |
| GeneradorUsuarios | Proveedor de datos de prueba con semilla fija |

## 4. Componentes y responsabilidades

| Componente | Archivo | Responsabilidad | Estado |
|------------|---------|-----------------|--------|
| RedSeguimiento | dominio/red.py | Relaciones de seguir/dejar de seguir, recomendaciones BFS a 2 saltos | Implementado y testeado |
| Feed | dominio/feed.py | Publicaciones de un usuario, navegar adelante/atrás, buscar por palabra | Implementado y testeado |
| IndiceUsuarios | dominio/indice_usuarios.py | Índice de usuarios por nombre (BST) | Implementado y testeado |
| Historial | dominio/historial.py | Navegación de pantallas con retroceso (pila) | Implementado y testeado |
| Notificaciones | dominio/notificaciones.py | Cola de notificaciones (NUEVO_SEGUIDOR, COMENTARIO, RESPUESTA) | Implementado y testeado |
| HiloComentarios | dominio/hilo_comentarios.py | Comentarios y respuestas en árbol general | Implementado y testeado |
| Usuario | dominio/usuario.py | Entidad con id, username, nombre_visible, biografía, feed, bandeja | Implementado y testeado |
| GeneradorUsuarios | dominio/generador_usuarios.py | Generación reproducible con semilla fija | Implementado y testeado |
| SistemaRed | dominio/sistema_red.py | Orquestador: une IndiceUsuarios, RedSeguimiento y Usuario | Implementado y testeado |
| main.py | No existe | Interfaz de consola | Pendiente de implementar |

## 5. Contratos e interacciones

### 5.1 Contrato SistemaRed → IndiceUsuarios
SistemaRed registra usuarios con `registrar_usuario()`, los indexa por nombre y los recupera con `buscar_usuario_por_nombre()`. El índice mantiene la correspondencia nombre → objeto Usuario.

### 5.2 Contrato SistemaRed → RedSeguimiento
SistemaRed asigna un ID entero consecutivo a cada usuario registrado mediante `RedSeguimiento.agregar_usuario()`. Ese ID es el vértice del grafo. Las operaciones `seguir()` y `dejar_de_seguir()` resuelven nombres a IDs a través de `IndiceUsuarios` antes de operar en el grafo.

### 5.3 Contrato SistemaRed → Usuario
SistemaRed crea una instancia de `Usuario` por cada usuario registrado, pasando el ID asignado por RedSeguimiento. El Usuario encapsula su propio `Feed` y `BandejaNotificaciones`.

### 5.4 Contrato SistemaRed → GeneradorUsuarios
SistemaRed.cargar_desde_generador() recibe tuplas (username, nombre_visible, biografia) del generador, valida que no haya duplicados y las registra. Valida antes de registrar para evitar cargas parciales.

### 5.5 Flujo de arranque del sistema
1. Crear instancia de `SistemaRed`.
2. Generar datos con `GeneradorUsuarios(semilla=42).generar(100)`.
3. Llamar `SistemaRed.cargar_desde_generador(datos)` para registrar todos los usuarios.
4. Seleccionar un usuario activo con `buscar_usuario_por_nombre()`.
5. Operar sobre el usuario activo (publicar, seguir, dejar de seguir, consultar notificaciones, etc.).

## 6. Invariantes globales del sistema

| ID | Invariante |
|----|------------|
| INV-SIS-01 | El ID de cada Usuario coincide con su vértice en RedSeguimiento. |
| INV-SIS-02 | Los IDs son consecutivos desde 0 sin huecos. |
| INV-SIS-03 | No hay dos usuarios con el mismo username en IndiceUsuarios. |
| INV-SIS-04 | Una notificación NUEVO_SEGUIDOR solo se genera la primera vez que se sigue una relación. |
| INV-SIS-05 | Los datos no persisten entre ejecuciones; se regeneran con la semilla fija al iniciar. |
| INV-SIS-06 | Un usuario activo debe existir antes de operaciones que lo requieran (publicar, seguir, consultar notificaciones). |

## 7. Criterios de aceptación del sistema

Los criterios se dividen en dos grupos:

### 7.1 Verificado en dominio (pruebas unitarias existentes)
Estos criterios ya están implementados y testeados en los módulos de dominio, pero **aún no se ejercitan desde `main.py`**.

| ID | Criterio | Verificable mediante |
|----|----------|----------------------|
| SIS-CA-01 | El sistema carga usuarios desde un generador con semilla fija y les asigna IDs consecutivos desde 0 | `test_cargar_desde_generador`, `test_cargar_desde_generador_ids_consecutivos` en tests/test_sistema_red.py |
| SIS-CA-02 | El sistema busca un usuario por nombre exacto y devuelve el objeto Usuario; si no existe, devuelve None sin error | `test_buscar_usuario_por_nombre`, `test_buscar_usuario_inexistente_devuelve_none` en tests/test_sistema_red.py |
| SIS-CA-03 | El sistema permite seguir y dejar de seguir usuarios; seguir una relación nueva genera una notificación NUEVO_SEGUIDOR para el usuario seguido | `test_seguir_usuario_genera_notificacion`, `test_dejar_de_seguir` en tests/test_sistema_red.py |
| SIS-CA-04 | El sistema no genera notificación duplicada al seguir una relación que ya existe | `test_seguir_repetido_no_genera_notificacion_duplicada` en tests/test_sistema_red.py |
| SIS-CA-05 | El sistema lanza UsuarioNoExisteError al seguir o dejar de seguir a un usuario inexistente | `test_seguir_usuario_inexistente_lanza_error` en tests/test_sistema_red.py |
| SIS-CA-06 | El sistema lista usuarios en orden alfabético ascendente | `test_listar_usuarios_orden_alfabetico` en tests/test_sistema_red.py |
| SIS-CA-07 | El sistema obtiene un usuario por ID entero; devuelve None para ID negativo o fuera de rango | `test_obtener_usuario_por_id_negativo_devuelve_none`, `test_obtener_usuario_por_id_fuera_de_rango_devuelve_none` en tests/test_sistema_red.py |
| SIS-CA-08 | El sistema carga usuarios desde el generador sin carga parcial: si hay nombres duplicados, lanza NombreDuplicadoError y no registra ninguno | `test_cargar_desde_generador_con_duplicados_no_carga_parcial` en tests/test_sistema_red.py |
| SIS-CA-09 | El sistema genera recomendaciones de contactos a exactamente 2 saltos que el usuario activo no sigue ni es él mismo | `test_recomendar_a_traves_del_sistema` en tests/test_sistema_red.py; `test_recomendar_a_dos_saltos`, `test_recomendar_sin_repetidos_ni_conocidos`, `test_recomendar_sin_candidatos`, `test_recomendar_orden` en tests/test_red.py |

### 7.2 Pendiente de integración con main.py (sin pruebas de consola aún)
Estos criterios requieren pruebas de integración que ejecuten `main.py` y verifiquen el comportamiento desde la interfaz de consola. Actualmente **no existen pruebas de este tipo**.

| ID | Criterio | Estado | Qué se necesita |
|----|----------|--------|-----------------|
| SIS-CA-10 | Un usuario puede publicar en su propio feed y verlo en el feed | Pendiente de integración | Prueba de main.py que publique y muestre el feed |
| SIS-CA-11 | Al seguir a alguien, el usuario seguido recibe una notificación visible desde consola | Pendiente de integración | Prueba de main.py que verifique la bandeja de notificaciones |
| SIS-CA-12 | El usuario puede volver a la pantalla anterior desde el menú de consola | Pendiente de integración | Prueba de main.py con Historial |
| SIS-CA-13 | El usuario puede buscar otro usuario y seleccionarlo desde el menú | Pendiente de integración | Prueba de main.py con búsqueda y selección |
| SIS-CA-14 | El usuario recibe recomendaciones de contactos desde el menú de consola | Pendiente de integración | Prueba de main.py con recomendaciones |

## 8. Casos extremos considerados

| Caso | Comportamiento esperado |
|------|------------------------|
| Sin usuarios cargados | No hay usuario activo; operaciones que lo requieren muestran mensaje de error |
| Usuario activo sin publicaciones | Feed vacío muestra cantidad 0 y actual() devuelve None |
| Usuario activo sin seguidos | Recomendaciones devuelven lista vacía |
| Seguir a uno mismo | Lanza AutoSeguimientoError |
| Seguir relación existente | Devuelve False, no genera notificación duplicada |
| Seguir usuario inexistente | Lanza UsuarioNoExisteError |
| Obtener usuario por ID negativo o fuera de rango | Devuelve None |
| Cargar con nombres duplicados | Lanza NombreDuplicadoError sin carga parcial (cantidad de usuarios = 0) |
| Notificaciones vacías | leer_siguiente() devuelve None sin error |
| Historial vacío | actual() devuelve None; volver lanza NadaAtrasError |

## 9. Historial de cambios

| Versión | Fecha | Cambio | Motivo |
|---------|-------|--------|--------|
| 1.0 | 12 nov 2026 | Versión inicial | Especificación del sistema integrado |
