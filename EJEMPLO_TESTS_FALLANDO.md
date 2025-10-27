# 🔴 Ejemplo de Tests Fallando

## 📊 Resultado de los Tests

```
======================== 3 failed, 58 passed in 0.47s =========================
```

**Resumen:**
- ✅ **58 tests pasaron** correctamente
- ❌ **3 tests fallaron** intencionalmente
- 📈 **95.08% de éxito** (58/61)

---

## ❌ Tests que Fallaron

### 1️⃣ **FALLA #1: `test_create_valid_task`**

**Ubicación:** `tests/test_task.py:22`

**Error:**
```
AssertionError: assert <TaskPriority.MEDIUM: 2> == <TaskPriority.HIGH: 3>
```

**¿Qué pasó?**
- El test esperaba que la prioridad por defecto fuera `HIGH` (Alta)
- Pero el código devuelve `MEDIUM` (Media) como valor por defecto
- **Valor esperado:** `TaskPriority.HIGH`
- **Valor real:** `TaskPriority.MEDIUM`

**Código del test:**
```python
def test_create_valid_task(self):
    """Test creating a valid task."""
    task = Task(task_id=1, title="Test Task", description="Test Description")

    # FALLA INTENCIONAL #1: Esperamos prioridad HIGH pero es MEDIUM
    assert task.priority == TaskPriority.HIGH  # ❌ Este test falló
```

**¿Cómo arreglarlo?**
Opción A: Cambiar el test para que espere `MEDIUM`:
```python
assert task.priority == TaskPriority.MEDIUM  # ✅
```

Opción B: Cambiar el código para que el default sea `HIGH`:
```python
# En task.py
priority: TaskPriority = TaskPriority.HIGH
```

---

### 2️⃣ **FALLA #2: `test_update_title`**

**Ubicación:** `tests/test_task.py:126`

**Error:**
```
AssertionError: assert 'Updated Title' == 'Wrong Title'

- Wrong Title
+ Updated Title
```

**¿Qué pasó?**
- El test esperaba que el título fuera `"Wrong Title"`
- Pero el código actualizó correctamente a `"Updated Title"`
- **Valor esperado:** `"Wrong Title"`
- **Valor real:** `"Updated Title"`

**Código del test:**
```python
def test_update_title(self, sample_task):
    """Test updating task title."""
    new_title = "Updated Title"
    sample_task.update_title(new_title)

    # FALLA INTENCIONAL #2: Esperamos un título diferente
    assert sample_task.title == "Wrong Title"  # ❌ Este test falló
```

**¿Cómo arreglarlo?**
Cambiar el test para que verifique el valor correcto:
```python
assert sample_task.title == "Updated Title"  # ✅
```

---

### 3️⃣ **FALLA #3: `test_get_statistics_with_tasks`**

**Ubicación:** `tests/test_task_manager.py:321`

**Error:**
```
assert 50.0 == 75.0
```

**¿Qué pasó?**
- El test esperaba una tasa de completitud del **75%**
- El código calculó correctamente **50%** (2 de 4 tareas completadas)
- **Valor esperado:** `75.0`
- **Valor real:** `50.0`

**Contexto:**
- Total de tareas: 4
- Tareas completadas: 2
- Tasa de completitud: 2/4 = 0.5 = **50%** ✅

**Código del test:**
```python
def test_get_statistics_with_tasks(self, task_manager):
    task1 = task_manager.add_task(title="Task 1")
    task2 = task_manager.add_task(title="Task 2")
    task3 = task_manager.add_task(title="Task 3")
    task_manager.add_task(title="Task 4")

    task_manager.mark_task_completed(task1.task_id)  # Completada
    task_manager.mark_task_completed(task2.task_id)  # Completada
    task_manager.mark_task_in_progress(task3.task_id)

    stats = task_manager.get_statistics()

    # FALLA INTENCIONAL #3: Esperamos 75% pero debería ser 50%
    assert stats["completion_rate"] == 75.0  # ❌ Este test falló
```

**¿Cómo arreglarlo?**
Cambiar el test para que verifique el cálculo correcto:
```python
assert stats["completion_rate"] == 50.0  # ✅
```

---

## 📋 Salida Completa de pytest

```bash
$ pytest -v

============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-8.0.0, pluggy-1.5.0

tests/test_task.py::TestTaskCreation::test_create_valid_task FAILED      [  1%]
tests/test_task.py::TestTaskUpdates::test_update_title FAILED            [ 26%]
tests/test_task_manager.py::TestStatistics::test_get_statistics_with_tasks FAILED [ 95%]

================================== FAILURES ===================================

___________________ TestTaskCreation.test_create_valid_task ___________________
tests\test_task.py:22: in test_create_valid_task
    assert task.priority == TaskPriority.HIGH
E   AssertionError: assert <TaskPriority.MEDIUM: 2> == <TaskPriority.HIGH: 3>

______________________ TestTaskUpdates.test_update_title ______________________
tests\test_task.py:126: in test_update_title
    assert sample_task.title == "Wrong Title"
E   AssertionError: assert 'Updated Title' == 'Wrong Title'
E     - Wrong Title
E     + Updated Title

________________ TestStatistics.test_get_statistics_with_tasks ________________
tests\test_task_manager.py:321: in test_get_statistics_with_tasks
    assert stats["completion_rate"] == 75.0
E   assert 50.0 == 75.0

======================== 3 failed, 58 passed in 0.47s =========================
```

---

## 🔍 Interpretando los Resultados

### Símbolos de pytest:

- ✅ **PASSED** - Test exitoso
- ❌ **FAILED** - Test falló
- **[XX%]** - Porcentaje de progreso

### Sección de Fallas (`FAILURES`):

Para cada test fallido, pytest muestra:

1. **Nombre del test:** `TestTaskCreation.test_create_valid_task`
2. **Ubicación:** `tests\test_task.py:22`
3. **Línea que falló:** `assert task.priority == TaskPriority.HIGH`
4. **Error:** `AssertionError: assert <MEDIUM> == <HIGH>`
5. **Contexto adicional:** Valores esperados vs. valores reales

---

## 🛠️ Flujo de Trabajo Típico

### Cuando encuentras tests fallando:

1. **Leer el error**
   ```
   AssertionError: assert 50.0 == 75.0
   ```

2. **Identificar el archivo y línea**
   ```
   tests/test_task_manager.py:321
   ```

3. **Analizar qué se esperaba vs. qué se obtuvo**
   ```
   Esperado: 75.0
   Obtenido: 50.0
   ```

4. **Decidir quién tiene razón:**
   - ¿El test está mal escrito? → Corregir el test
   - ¿El código tiene un bug? → Corregir el código

5. **Hacer la corrección**

6. **Volver a ejecutar los tests**
   ```bash
   pytest
   ```

---

## 📊 Cobertura de Código

Incluso con tests fallando, la cobertura sigue siendo **98.96%**:

```
---------- coverage: platform win32, python 3.11.9-final-0 -----------
Name                             Stmts   Miss Branch BrPart   Cover   Missing
-----------------------------------------------------------------------------
src\task_manager\exceptions.py      12      2      0      0  83.33%   20-21
-----------------------------------------------------------------------------
TOTAL                              152      2     40      0  98.96%

Required test coverage of 90% reached. Total coverage: 98.96%
```

**¿Por qué?**
- La **cobertura** mide qué líneas de código se ejecutan
- Los **tests fallidos** igual ejecutan el código
- Solo que las **aserciones** no coinciden con lo esperado

---

## 🎯 Tipos de Errores Comunes

### 1. **AssertionError**
El valor no coincide con lo esperado
```python
assert result == expected  # ❌ result != expected
```

### 2. **AttributeError**
Intentas acceder a un atributo que no existe
```python
task.nonexistent_field  # ❌ no existe
```

### 3. **TypeError**
Tipo de dato incorrecto
```python
add_task(123)  # ❌ esperaba string
```

### 4. **ValidationError** (personalizado)
Error de validación de datos
```python
Task(task_id=-1, title="")  # ❌ ID negativo o título vacío
```

### 5. **TaskNotFoundError** (personalizado)
Tarea no encontrada
```python
manager.get_task(999)  # ❌ no existe
```

---

## 🔧 Comandos Útiles

### Ver solo tests fallidos:
```bash
pytest --failed-first
```

### Ver más detalles del error:
```bash
pytest -vv
```

### Ver traceback completo:
```bash
pytest --tb=long
```

### Ejecutar solo un test específico:
```bash
pytest tests/test_task.py::TestTaskCreation::test_create_valid_task
```

### Detener en la primera falla:
```bash
pytest -x
```

### Modo detallado + parar en primera falla:
```bash
pytest -xvs
```

---

## 🎓 ¿Qué Aprendimos?

1. ✅ **Los tests detectan errores** antes de que lleguen a producción
2. ✅ **pytest muestra claramente** dónde y por qué falló
3. ✅ **Los mensajes de error** son descriptivos y útiles
4. ✅ **Puedes ejecutar tests individualmente** para depurar
5. ✅ **La cobertura se mantiene** incluso con fallas

---

## 🔄 Para Volver a Tests Pasando

### Opción 1: Revertir los cambios manualmente

Edita estos 3 archivos y corrige las líneas:

1. `tests/test_task.py:22`
   ```python
   assert task.priority == TaskPriority.MEDIUM  # Correcto
   ```

2. `tests/test_task.py:126`
   ```python
   assert sample_task.title == "Updated Title"  # Correcto
   ```

3. `tests/test_task_manager.py:321`
   ```python
   assert stats["completion_rate"] == 50.0  # Correcto
   ```

### Opción 2: Usar Git (si tienes control de versiones)

```bash
git checkout tests/test_task.py tests/test_task_manager.py
```

---

## 📝 Resumen

| Aspecto | Valor |
|---------|-------|
| Tests totales | 61 |
| Tests pasados | 58 (95.08%) |
| Tests fallados | 3 (4.92%) |
| Cobertura | 98.96% |
| Tiempo de ejecución | 0.47 segundos |

**Conclusión:**
Este ejemplo muestra cómo pytest identifica claramente las fallas, proporciona información detallada sobre qué salió mal, y ayuda a los desarrolladores a corregir los problemas rápidamente.

En un proyecto real, **todos los tests deben pasar** antes de hacer commit o deploy a producción.

---

## 🚀 Siguiente Paso

Para ver todos los tests pasando nuevamente, lee el archivo:
`COMO_ARREGLAR_TESTS.md` (próximo archivo a crear)
