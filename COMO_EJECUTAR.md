# 🚀 Cómo Ejecutar la Aplicación

## 📋 Requisitos Previos

Asegúrate de tener instalado:
- Python 3.9 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

## ▶️ Formas de Ejecutar la Aplicación

Hay **3 formas** de usar esta aplicación:

---

### 🎮 Opción 1: Aplicación Interactiva (RECOMENDADO)

**Comando:**
```bash
python main.py
```

**¿Qué hace?**
- Abre un menú interactivo en la consola
- Puedes agregar, ver, actualizar y eliminar tareas
- Interfaz amigable con opciones numeradas

**Ejemplo de uso:**

```
======================================================================
            BIENVENIDO AL GESTOR DE TAREAS
======================================================================

Desea cargar tareas de ejemplo? (s/n) [n]: s

======================================================================
GESTOR DE TAREAS - MENU PRINCIPAL
======================================================================

1. Agregar nueva tarea
2. Ver todas las tareas
3. Ver tareas por estado
4. Ver tareas por prioridad
5. Marcar tarea como en progreso
6. Marcar tarea como completada
7. Actualizar tarea
8. Eliminar tarea
9. Ver estadisticas
10. Ver tareas vencidas
0. Salir

Seleccione una opcion (0-10):
```

**Funcionalidades:**

1. **Agregar tarea**: Te pide título, descripción, prioridad y fecha de vencimiento
2. **Ver todas las tareas**: Lista completa con todos los detalles
3. **Filtrar por estado**: Pendientes, En Progreso, Completadas, Canceladas
4. **Filtrar por prioridad**: Baja, Media, Alta, Crítica
5. **Marcar en progreso**: Cambia el estado de una tarea
6. **Marcar completada**: Marca una tarea como terminada
7. **Actualizar**: Modifica título, descripción o prioridad
8. **Eliminar**: Borra una tarea
9. **Estadísticas**: Ver totales y tasa de completitud
10. **Ver vencidas**: Lista de tareas atrasadas

---

### 📚 Opción 2: Ejemplo Demostrativo

**Comando:**
```bash
python ejemplo_simple.py
```

**¿Qué hace?**
- Ejecuta un script que muestra todas las funcionalidades
- Crea tareas de ejemplo automáticamente
- Muestra paso a paso lo que hace el código
- No es interactivo, solo muestra el funcionamiento

**Salida esperada:**

```
======================================================================
               EJEMPLO DE USO DEL GESTOR DE TAREAS
======================================================================

1. Creando gestor de tareas...
   [OK] Gestor creado

2. Agregando tareas...
   [OK] Tarea 1 creada: Estudiar Python (ID: 1)
   [OK] Tarea 2 creada: Hacer ejercicio (ID: 2)
   [OK] Tarea 3 creada: Comprar viveres (ID: 3)
   [OK] Tarea 4 creada: Preparar presentacion (ID: 4)

3. Listando todas las tareas...
   Total de tareas: 4
   - [1] Estudiar Python (Prioridad: HIGH)
   - [2] Hacer ejercicio (Prioridad: MEDIUM)
   - [3] Comprar viveres (Prioridad: LOW)
   - [4] Preparar presentacion (Prioridad: CRITICAL)

...

[FIN DEL EJEMPLO]
```

**Uso recomendado:**
- Para entender cómo funciona la aplicación
- Para ver ejemplos de código
- Para demostrar las funcionalidades a otros

---

### 💻 Opción 3: Usar como Biblioteca

**¿Qué significa?**
Puedes importar la funcionalidad en tus propios scripts de Python.

**Ejemplo - Crea tu propio script:**

```python
# mi_script.py
from datetime import datetime, timedelta
from src.task_manager import TaskManager, TaskPriority, TaskStatus

# Crear gestor
manager = TaskManager()

# Agregar tareas
tarea1 = manager.add_task(
    title="Hacer la compra",
    description="Comprar frutas y verduras",
    priority=TaskPriority.HIGH,
    due_date=datetime.now() + timedelta(days=2)
)

print(f"Tarea creada con ID: {tarea1.task_id}")
print(f"Título: {tarea1.title}")
print(f"Estado: {tarea1.status.value}")

# Marcar como completada
manager.mark_task_completed(tarea1.task_id)
print(f"Nuevo estado: {tarea1.status.value}")

# Ver estadísticas
stats = manager.get_statistics()
print(f"Total de tareas: {stats['total']}")
print(f"Completadas: {stats['completed']}")
```

**Ejecutar tu script:**
```bash
python mi_script.py
```

---

## 📊 Verificar que Todo Funciona

### Ejecutar los tests:

```bash
# Tests básicos
pytest

# Tests con reporte detallado
pytest -v

# Tests con cobertura
pytest --cov=src --cov-report=html
```

Si ves esto, todo funciona correctamente:
```
============================= 61 passed in 0.33s ==============================
```

---

## 🎯 Comandos Rápidos

| Comando | Descripción |
|---------|-------------|
| `python main.py` | Aplicación interactiva |
| `python ejemplo_simple.py` | Ver demostración |
| `pytest` | Ejecutar tests |
| `make test` | Ejecutar tests (con Makefile) |
| `make all` | Formatear + verificar + tests |

---

## 🐛 Solución de Problemas

### Error: "No module named 'src'"

**Solución:**
Asegúrate de estar en la carpeta del proyecto:
```bash
cd "C:\Users\ASUS GAMING\Desktop\Prcoesos Soft\PipeLine CD"
python main.py
```

### Error: "ModuleNotFoundError: No module named 'pytest'"

**Solución:**
Instala las dependencias:
```bash
pip install -r requirements.txt
```

### La aplicación no muestra los emojis correctamente

**Solución:**
Esto es normal en Windows. Los emojis son opcionales, la aplicación funciona igual.

---

## 📖 Ejemplos de Uso Real

### Ejemplo 1: Agregar una tarea rápida

```bash
python main.py
# Selecciona opción 1
# Ingresa título: "Llamar al doctor"
# Descripción: "Agendar cita para revisión"
# Prioridad: 3 (Alta)
# Vencimiento: s
# Días: 3
```

### Ejemplo 2: Ver tareas pendientes

```bash
python main.py
# Selecciona opción 3 (Ver tareas por estado)
# Selecciona 1 (Pendiente)
```

### Ejemplo 3: Ver estadísticas

```bash
python main.py
# Selecciona opción 9 (Ver estadísticas)
```

---

## 🎓 Próximos Pasos

Después de probar la aplicación, puedes:

1. **Modificar el código** - Agrega nuevas funcionalidades
2. **Crear tests** - Escribe tests para tus cambios
3. **Integrar con base de datos** - Guarda las tareas en SQLite
4. **Crear API REST** - Usa FastAPI para crear una API
5. **Interfaz web** - Crea un frontend con HTML/CSS/JavaScript

---

## 📝 Notas Importantes

- ⚠️ **Persistencia**: Actualmente las tareas solo existen mientras el programa está corriendo. Al cerrar, se pierden.
- ✅ **Tests**: Todos los tests pasan con 98.96% de cobertura
- 🔧 **Desarrollo**: Usa `make all` para verificar la calidad del código

---

## 🆘 Ayuda

Si tienes problemas, verifica:

1. ✅ Python está instalado: `python --version`
2. ✅ Dependencias instaladas: `pip list`
3. ✅ Estás en la carpeta correcta: `pwd` (Linux/Mac) o `cd` (Windows)
4. ✅ Los tests pasan: `pytest`

---

## 🎉 ¡Listo!

Ya sabes cómo ejecutar la aplicación de 3 formas diferentes.

**Recomendación:** Empieza con `python main.py` para tener una experiencia interactiva.

¡Disfruta gestionando tus tareas! 🚀
