# 🔧 Cómo Arreglar los Tests Fallando

## 🎯 Objetivo

Volver a tener **61 de 61 tests pasando** (100% de éxito)

---

## 📋 Tests a Corregir

Hay **3 tests** con fallas intencionales que necesitamos corregir:

1. ❌ `test_create_valid_task` - línea 22
2. ❌ `test_update_title` - línea 126
3. ❌ `test_get_statistics_with_tasks` - línea 321

---

## 🛠️ Solución 1: Corrección Manual (Paso a Paso)

### **Paso 1: Corregir `test_create_valid_task`**

**Archivo:** `tests/test_task.py`
**Línea:** 22

**Busca esto:**
```python
# FALLA INTENCIONAL #1: Esperamos prioridad HIGH pero es MEDIUM
assert task.priority == TaskPriority.HIGH  # Este test fallará
```

**Cámbialo por esto:**
```python
assert task.priority == TaskPriority.MEDIUM
```

**O simplemente elimina la línea con el comentario y déjala como estaba:**
```python
assert task.priority == TaskPriority.MEDIUM
```

---

### **Paso 2: Corregir `test_update_title`**

**Archivo:** `tests/test_task.py`
**Línea:** 126

**Busca esto:**
```python
# FALLA INTENCIONAL #2: Esperamos un título diferente
assert sample_task.title == "Wrong Title"  # Este test fallará
```

**Cámbialo por esto:**
```python
assert sample_task.title == new_title
```

**O más explícitamente:**
```python
assert sample_task.title == "Updated Title"
```

---

### **Paso 3: Corregir `test_get_statistics_with_tasks`**

**Archivo:** `tests/test_task_manager.py`
**Línea:** 321

**Busca esto:**
```python
# FALLA INTENCIONAL #3: Esperamos 75% pero debería ser 50%
assert stats["completion_rate"] == 75.0  # Este test fallará
```

**Cámbialo por esto:**
```python
assert stats["completion_rate"] == 50.0
```

---

### **Paso 4: Verificar las Correcciones**

Después de hacer los cambios, ejecuta:

```bash
pytest
```

**Resultado esperado:**
```
======================== 61 passed in 0.33s ==============================
```

---

## 🚀 Solución 2: Usando los Comandos de Git

Si tienes Git configurado y los archivos originales en el repositorio:

```bash
# Revertir los cambios en los archivos de tests
git checkout tests/test_task.py
git checkout tests/test_task_manager.py

# Ejecutar tests
pytest
```

---

## 📝 Solución 3: Reemplazar el Contenido Completo

Si prefieres copiar y pegar, aquí están las versiones corregidas:

### **tests/test_task.py - línea 13-22 (corregida)**

```python
def test_create_valid_task(self):
    """Test creating a valid task."""
    task = Task(task_id=1, title="Test Task", description="Test Description")

    assert task.task_id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == TaskStatus.PENDING
    assert task.priority == TaskPriority.MEDIUM
```

### **tests/test_task.py - línea 120-126 (corregida)**

```python
def test_update_title(self, sample_task):
    """Test updating task title."""
    new_title = "Updated Title"
    sample_task.update_title(new_title)

    assert sample_task.title == new_title
```

### **tests/test_task_manager.py - línea 303-321 (corregida)**

```python
def test_get_statistics_with_tasks(self, task_manager):
    """Test statistics with various tasks."""
    task1 = task_manager.add_task(title="Task 1")
    task2 = task_manager.add_task(title="Task 2")
    task3 = task_manager.add_task(title="Task 3")
    task_manager.add_task(title="Task 4")

    task_manager.mark_task_completed(task1.task_id)
    task_manager.mark_task_completed(task2.task_id)
    task_manager.mark_task_in_progress(task3.task_id)

    stats = task_manager.get_statistics()

    assert stats["total"] == 4
    assert stats["completed"] == 2
    assert stats["in_progress"] == 1
    assert stats["pending"] == 1
    assert stats["completion_rate"] == 50.0
```

---

## ✅ Verificación Final

Después de corregir los 3 tests, ejecuta el conjunto completo:

```bash
# Tests básicos
pytest

# Tests con más detalle
pytest -v

# Tests con cobertura
pytest --cov=src --cov-report=term-missing
```

**Resultado esperado:**

```
============================= test session starts =============================
collected 61 items

tests/test_task.py ............................                          [ 45%]
tests/test_task_manager.py .................................             [100%]

---------- coverage: platform win32, python 3.11.9-final-0 -----------
Name                             Stmts   Miss Branch BrPart   Cover   Missing
-----------------------------------------------------------------------------
src\task_manager\exceptions.py      12      2      0      0  83.33%   20-21
-----------------------------------------------------------------------------
TOTAL                              152      2     40      0  98.96%

======================== 61 passed in 0.33s ==============================
```

---

## 🎯 Checklist de Verificación

Marca cada item cuando lo completes:

- [ ] Corregir `test_create_valid_task` (línea 22 de test_task.py)
- [ ] Corregir `test_update_title` (línea 126 de test_task.py)
- [ ] Corregir `test_get_statistics_with_tasks` (línea 321 de test_task_manager.py)
- [ ] Ejecutar `pytest` y verificar que los 61 tests pasen
- [ ] Verificar cobertura de 98.96%
- [ ] (Opcional) Ejecutar `make all` para verificar todo

---

## 🔍 Comandos para Localizar las Líneas

Si no encuentras las líneas exactas, puedes buscar los comentarios:

### En Windows (PowerShell):
```powershell
Select-String "FALLA INTENCIONAL" tests\*.py
```

### En Windows (Command Prompt):
```cmd
findstr /S /N "FALLA INTENCIONAL" tests\*.py
```

### En Linux/Mac:
```bash
grep -n "FALLA INTENCIONAL" tests/*.py
```

---

## 📊 Antes y Después

### **ANTES (con fallas):**
```
======================== 3 failed, 58 passed in 0.47s =========================
```

### **DESPUÉS (corregido):**
```
======================== 61 passed in 0.33s ==============================
```

---

## 💡 Consejos

1. **Usa un editor de código** como VS Code, PyCharm, o Notepad++ para encontrar las líneas rápidamente
2. **Busca por los comentarios** "FALLA INTENCIONAL" para encontrar las líneas exactas
3. **Ejecuta pytest después de cada corrección** para verificar el progreso
4. **Si tienes dudas**, compara con las versiones corregidas en este documento

---

## 🎓 Lección Aprendida

Este ejercicio demuestra:

✅ Cómo pytest **detecta errores** en el código
✅ Cómo **leer e interpretar** mensajes de error
✅ Cómo **corregir tests fallidos** paso a paso
✅ La importancia de **mantener todos los tests pasando**

En un proyecto real, **NUNCA** debes hacer commit con tests fallando.

---

## 🆘 ¿Siguen fallando los tests?

Si después de las correcciones aún hay fallas:

1. **Verifica que guardaste los archivos** después de editarlos
2. **Asegúrate de estar en la carpeta correcta:**
   ```bash
   cd "C:\Users\ASUS GAMING\Desktop\Prcoesos Soft\PipeLine CD"
   ```
3. **Ejecuta pytest con más detalle:**
   ```bash
   pytest -vv
   ```
4. **Verifica que no haya errores de sintaxis:**
   ```bash
   python -m py_compile tests/test_task.py
   python -m py_compile tests/test_task_manager.py
   ```

---

## ✨ ¡Listo!

Una vez corregidos los 3 tests, tu proyecto volverá a tener:

- ✅ 61/61 tests pasando
- ✅ 100% de tasa de éxito
- ✅ 98.96% de cobertura de código
- ✅ Pylint 10/10
- ✅ Flake8 0 errores

**¡Proyecto perfecto nuevamente!** 🎉
