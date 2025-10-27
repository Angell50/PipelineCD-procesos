#!/usr/bin/env python
"""
Ejemplo simple de uso de la aplicación de gestión de tareas.
Ejecutar: python ejemplo_simple.py
"""

from datetime import datetime, timedelta

from src.task_manager import TaskManager, TaskPriority, TaskStatus


def main():
    """Ejemplo simple de uso del gestor de tareas."""
    print("=" * 70)
    print(" " * 15 + "EJEMPLO DE USO DEL GESTOR DE TAREAS")
    print("=" * 70)

    # 1. Crear el gestor de tareas
    print("\n1. Creando gestor de tareas...")
    manager = TaskManager()
    print("   [OK] Gestor creado")

    # 2. Agregar algunas tareas
    print("\n2. Agregando tareas...")

    tarea1 = manager.add_task(
        title="Estudiar Python",
        description="Repasar conceptos de POO y testing",
        priority=TaskPriority.HIGH,
        due_date=datetime.now() + timedelta(days=7),
    )
    print(f"   [OK] Tarea 1 creada: {tarea1.title} (ID: {tarea1.task_id})")

    tarea2 = manager.add_task(
        title="Hacer ejercicio",
        description="30 minutos de cardio",
        priority=TaskPriority.MEDIUM,
    )
    print(f"   [OK] Tarea 2 creada: {tarea2.title} (ID: {tarea2.task_id})")

    tarea3 = manager.add_task(
        title="Comprar viveres",
        description="Leche, pan, huevos, frutas",
        priority=TaskPriority.LOW,
        due_date=datetime.now() + timedelta(days=2),
    )
    print(f"   [OK] Tarea 3 creada: {tarea3.title} (ID: {tarea3.task_id})")

    tarea4 = manager.add_task(
        title="Preparar presentacion",
        description="Slides para reunion del viernes",
        priority=TaskPriority.CRITICAL,
        due_date=datetime.now() + timedelta(days=1),
    )
    print(f"   [OK] Tarea 4 creada: {tarea4.title} (ID: {tarea4.task_id})")

    # 3. Ver todas las tareas
    print("\n3. Listando todas las tareas...")
    todas = manager.get_all_tasks()
    print(f"   Total de tareas: {len(todas)}")
    for tarea in todas:
        print(f"   - [{tarea.task_id}] {tarea.title} (Prioridad: {tarea.priority.name})")

    # 4. Marcar algunas tareas como en progreso
    print("\n4. Marcando tareas como 'En Progreso'...")
    manager.mark_task_in_progress(tarea1.task_id)
    print(f"   [OK] '{tarea1.title}' ahora esta en progreso")

    manager.mark_task_in_progress(tarea4.task_id)
    print(f"   [OK] '{tarea4.title}' ahora esta en progreso")

    # 5. Completar una tarea
    print("\n5. Completando tareas...")
    manager.mark_task_completed(tarea2.task_id)
    print(f"   [OK] '{tarea2.title}' marcada como completada")

    # 6. Filtrar tareas por estado
    print("\n6. Filtrando tareas por estado...")

    pendientes = manager.get_tasks_by_status(TaskStatus.PENDING)
    print(f"\n   Tareas PENDIENTES ({len(pendientes)}):")
    for tarea in pendientes:
        print(f"   - {tarea.title}")

    en_progreso = manager.get_tasks_by_status(TaskStatus.IN_PROGRESS)
    print(f"\n   Tareas EN PROGRESO ({len(en_progreso)}):")
    for tarea in en_progreso:
        print(f"   - {tarea.title}")

    completadas = manager.get_tasks_by_status(TaskStatus.COMPLETED)
    print(f"\n   Tareas COMPLETADAS ({len(completadas)}):")
    for tarea in completadas:
        print(f"   - {tarea.title}")

    # 7. Filtrar por prioridad
    print("\n7. Filtrando tareas por prioridad...")

    alta_prioridad = manager.get_tasks_by_priority(TaskPriority.HIGH)
    print(f"\n   Tareas de ALTA prioridad ({len(alta_prioridad)}):")
    for tarea in alta_prioridad:
        print(f"   - {tarea.title}")

    criticas = manager.get_tasks_by_priority(TaskPriority.CRITICAL)
    print(f"\n   Tareas CRITICAS ({len(criticas)}):")
    for tarea in criticas:
        print(f"   - {tarea.title} (Estado: {tarea.status.value})")

    # 8. Ver tareas vencidas
    print("\n8. Verificando tareas vencidas...")
    vencidas = manager.get_overdue_tasks()
    if vencidas:
        print(f"   [!] Hay {len(vencidas)} tarea(s) vencida(s):")
        for tarea in vencidas:
            print(f"   - {tarea.title}")
    else:
        print("   [OK] No hay tareas vencidas")

    # 9. Ver estadísticas
    print("\n9. Estadisticas del gestor...")
    stats = manager.get_statistics()
    print(f"\n   Total de tareas: {stats['total']}")
    print(f"   Pendientes: {stats['pending']}")
    print(f"   En progreso: {stats['in_progress']}")
    print(f"   Completadas: {stats['completed']}")
    print(f"   Canceladas: {stats['cancelled']}")
    print(f"   Vencidas: {stats['overdue']}")
    print(f"   Tasa de completitud: {stats['completion_rate']:.2f}%")

    # 10. Actualizar una tarea
    print("\n10. Actualizando una tarea...")
    manager.update_task(
        tarea3.task_id,
        title="Comprar viveres y productos de limpieza",
        priority=TaskPriority.MEDIUM,
    )
    tarea_actualizada = manager.get_task(tarea3.task_id)
    print(f"   [OK] Tarea actualizada: {tarea_actualizada.title}")
    print(f"        Nueva prioridad: {tarea_actualizada.priority.name}")

    # 11. Eliminar una tarea
    print("\n11. Eliminando una tarea...")
    print(f"   Eliminando: '{tarea3.title}'")
    manager.delete_task(tarea3.task_id)
    print(f"   [OK] Tarea eliminada")
    print(f"   Total de tareas ahora: {manager.get_task_count()}")

    # 12. Resumen final
    print("\n" + "=" * 70)
    print(" " * 20 + "RESUMEN FINAL")
    print("=" * 70)

    todas = manager.get_all_tasks()
    print(f"\nTareas restantes: {len(todas)}\n")

    for tarea in todas:
        estado_str = {
            TaskStatus.PENDING: "[PEND]",
            TaskStatus.IN_PROGRESS: "[PROG]",
            TaskStatus.COMPLETED: "[DONE]",
            TaskStatus.CANCELLED: "[CANC]",
        }.get(tarea.status, "")

        prioridad_str = {
            TaskPriority.LOW: "[BAJO]",
            TaskPriority.MEDIUM: "[MEDI]",
            TaskPriority.HIGH: "[ALTO]",
            TaskPriority.CRITICAL: "[CRIT]",
        }.get(tarea.priority, "")

        print(f"{estado_str} {prioridad_str} [{tarea.task_id}] {tarea.title}")
        print(f"   Estado: {tarea.status.value} | Prioridad: {tarea.priority.name}")
        if tarea.due_date:
            vencimiento = tarea.due_date.strftime("%Y-%m-%d")
            vencida = " [VENCIDA]" if tarea.is_overdue() else ""
            print(f"   Vence: {vencimiento}{vencida}")
        print()

    print("=" * 70)
    print("\n[FIN DEL EJEMPLO]")
    print("\nPara usar la aplicacion interactiva, ejecuta: python main.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
