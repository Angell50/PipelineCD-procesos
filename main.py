#!/usr/bin/env python
"""
Aplicación de línea de comandos para gestión de tareas.
Ejecutar: python main.py
"""

import sys
from datetime import datetime, timedelta

from src.task_manager import (
    TaskManager,
    TaskNotFoundError,
    TaskPriority,
    TaskStatus,
    ValidationError,
)


def print_separator():
    """Imprime una línea separadora."""
    print("\n" + "=" * 70 + "\n")


def print_menu():
    """Muestra el menú principal."""
    print_separator()
    print("GESTOR DE TAREAS - MENU PRINCIPAL")
    print_separator()
    print("1. Agregar nueva tarea")
    print("2. Ver todas las tareas")
    print("3. Ver tareas por estado")
    print("4. Ver tareas por prioridad")
    print("5. Marcar tarea como en progreso")
    print("6. Marcar tarea como completada")
    print("7. Actualizar tarea")
    print("8. Eliminar tarea")
    print("9. Ver estadisticas")
    print("10. Ver tareas vencidas")
    print("0. Salir")
    print_separator()


def print_task(task):
    """Imprime una tarea formateada."""
    print(f"\n  ID: {task.task_id}")
    print(f"  Titulo: {task.title}")
    print(f"  Descripcion: {task.description or 'Sin descripcion'}")
    print(f"  Estado: {task.status.value}")
    print(f"  Prioridad: {task.priority.name}")
    print(f"  Creada: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
    if task.due_date:
        print(f"  Vencimiento: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
        if task.is_overdue():
            print("  [!] TAREA VENCIDA")
    print("  " + "-" * 60)


def add_task(manager):
    """Agrega una nueva tarea."""
    print_separator()
    print("AGREGAR NUEVA TAREA")
    print_separator()

    title = input("Titulo (obligatorio): ").strip()
    if not title:
        print("\n[ERROR] El titulo no puede estar vacio.")
        return

    description = input("Descripcion (opcional): ").strip()

    print("\nPrioridades disponibles:")
    print("1. Baja")
    print("2. Media (default)")
    print("3. Alta")
    print("4. Critica")

    priority_choice = input("Seleccione prioridad (1-4) [2]: ").strip() or "2"
    priority_map = {
        "1": TaskPriority.LOW,
        "2": TaskPriority.MEDIUM,
        "3": TaskPriority.HIGH,
        "4": TaskPriority.CRITICAL,
    }
    priority = priority_map.get(priority_choice, TaskPriority.MEDIUM)

    # Fecha de vencimiento
    add_due_date = input("\nAgregar fecha de vencimiento? (s/n) [n]: ").strip().lower()
    due_date = None

    if add_due_date == "s":
        try:
            days = int(input("Dias hasta el vencimiento: "))
            due_date = datetime.now() + timedelta(days=days)
        except ValueError:
            print("[ADVERTENCIA] Fecha invalida, se omitira.")

    try:
        task = manager.add_task(
            title=title, description=description, priority=priority, due_date=due_date
        )
        print(f"\n[EXITO] Tarea creada con ID: {task.task_id}")
        print_task(task)
    except ValidationError as e:
        print(f"\n[ERROR] {e}")


def view_all_tasks(manager):
    """Muestra todas las tareas."""
    print_separator()
    print("TODAS LAS TAREAS")
    print_separator()

    tasks = manager.get_all_tasks()

    if not tasks:
        print("No hay tareas registradas.")
        return

    print(f"\nTotal de tareas: {len(tasks)}")
    for task in tasks:
        print_task(task)


def view_tasks_by_status(manager):
    """Muestra tareas filtradas por estado."""
    print_separator()
    print("TAREAS POR ESTADO")
    print_separator()

    print("Estados disponibles:")
    print("1. Pendiente")
    print("2. En Progreso")
    print("3. Completada")
    print("4. Cancelada")

    choice = input("\nSeleccione estado (1-4): ").strip()

    status_map = {
        "1": TaskStatus.PENDING,
        "2": TaskStatus.IN_PROGRESS,
        "3": TaskStatus.COMPLETED,
        "4": TaskStatus.CANCELLED,
    }

    status = status_map.get(choice)
    if not status:
        print("[ERROR] Opcion invalida.")
        return

    tasks = manager.get_tasks_by_status(status)

    if not tasks:
        print(f"\nNo hay tareas con estado: {status.value}")
        return

    print(f"\nTareas con estado '{status.value}': {len(tasks)}")
    for task in tasks:
        print_task(task)


def view_tasks_by_priority(manager):
    """Muestra tareas filtradas por prioridad."""
    print_separator()
    print("TAREAS POR PRIORIDAD")
    print_separator()

    print("Prioridades disponibles:")
    print("1. Baja")
    print("2. Media")
    print("3. Alta")
    print("4. Critica")

    choice = input("\nSeleccione prioridad (1-4): ").strip()

    priority_map = {
        "1": TaskPriority.LOW,
        "2": TaskPriority.MEDIUM,
        "3": TaskPriority.HIGH,
        "4": TaskPriority.CRITICAL,
    }

    priority = priority_map.get(choice)
    if not priority:
        print("[ERROR] Opcion invalida.")
        return

    tasks = manager.get_tasks_by_priority(priority)

    if not tasks:
        print(f"\nNo hay tareas con prioridad: {priority.name}")
        return

    print(f"\nTareas con prioridad '{priority.name}': {len(tasks)}")
    for task in tasks:
        print_task(task)


def mark_task_in_progress(manager):
    """Marca una tarea como en progreso."""
    print_separator()
    print("MARCAR TAREA COMO EN PROGRESO")
    print_separator()

    try:
        task_id = int(input("ID de la tarea: "))
        task = manager.mark_task_in_progress(task_id)
        print("\n[EXITO] Tarea marcada como en progreso:")
        print_task(task)
    except ValueError:
        print("[ERROR] ID invalido.")
    except TaskNotFoundError as e:
        print(f"[ERROR] {e}")
    except ValidationError as e:
        print(f"[ERROR] {e}")


def mark_task_completed(manager):
    """Marca una tarea como completada."""
    print_separator()
    print("MARCAR TAREA COMO COMPLETADA")
    print_separator()

    try:
        task_id = int(input("ID de la tarea: "))
        task = manager.mark_task_completed(task_id)
        print("\n[EXITO] Tarea marcada como completada:")
        print_task(task)
    except ValueError:
        print("[ERROR] ID invalido.")
    except TaskNotFoundError as e:
        print(f"[ERROR] {e}")
    except ValidationError as e:
        print(f"[ERROR] {e}")


def update_task(manager):
    """Actualiza una tarea existente."""
    print_separator()
    print("ACTUALIZAR TAREA")
    print_separator()

    try:
        task_id = int(input("ID de la tarea a actualizar: "))

        # Mostrar tarea actual
        current_task = manager.get_task(task_id)
        print("\nTarea actual:")
        print_task(current_task)

        print("\nDeje en blanco para mantener el valor actual.")

        new_title = input(f"Nuevo titulo [{current_task.title}]: ").strip()
        new_description = input(f"Nueva descripcion [{current_task.description}]: ").strip()

        # Prioridad
        print("\nPrioridades: 1=Baja, 2=Media, 3=Alta, 4=Critica")
        priority_input = input(f"Nueva prioridad [{current_task.priority.value}]: ").strip()

        priority_map = {
            "1": TaskPriority.LOW,
            "2": TaskPriority.MEDIUM,
            "3": TaskPriority.HIGH,
            "4": TaskPriority.CRITICAL,
        }
        new_priority = priority_map.get(priority_input) if priority_input else None

        # Actualizar
        task = manager.update_task(
            task_id,
            title=new_title if new_title else None,
            description=new_description if new_description else None,
            priority=new_priority,
        )

        print("\n[EXITO] Tarea actualizada:")
        print_task(task)

    except ValueError:
        print("[ERROR] ID invalido.")
    except TaskNotFoundError as e:
        print(f"[ERROR] {e}")
    except ValidationError as e:
        print(f"[ERROR] {e}")


def delete_task(manager):
    """Elimina una tarea."""
    print_separator()
    print("ELIMINAR TAREA")
    print_separator()

    try:
        task_id = int(input("ID de la tarea a eliminar: "))

        # Mostrar tarea antes de eliminar
        task = manager.get_task(task_id)
        print("\nTarea a eliminar:")
        print_task(task)

        confirm = input("\nEsta seguro? (s/n): ").strip().lower()
        if confirm == "s":
            manager.delete_task(task_id)
            print("\n[EXITO] Tarea eliminada correctamente.")
        else:
            print("\n[CANCELADO] Operacion cancelada.")

    except ValueError:
        print("[ERROR] ID invalido.")
    except TaskNotFoundError as e:
        print(f"[ERROR] {e}")


def show_statistics(manager):
    """Muestra estadísticas del gestor."""
    print_separator()
    print("ESTADISTICAS")
    print_separator()

    stats = manager.get_statistics()

    print(f"\nTotal de tareas: {stats['total']}")
    print(f"Pendientes: {stats['pending']}")
    print(f"En progreso: {stats['in_progress']}")
    print(f"Completadas: {stats['completed']}")
    print(f"Canceladas: {stats['cancelled']}")
    print(f"Vencidas: {stats['overdue']}")
    print(f"\nTasa de completitud: {stats['completion_rate']:.2f}%")


def show_overdue_tasks(manager):
    """Muestra tareas vencidas."""
    print_separator()
    print("TAREAS VENCIDAS")
    print_separator()

    tasks = manager.get_overdue_tasks()

    if not tasks:
        print("\nNo hay tareas vencidas. Buen trabajo!")
        return

    print(f"\n[!] Hay {len(tasks)} tarea(s) vencida(s):")
    for task in tasks:
        print_task(task)


def demo_mode(manager):
    """Modo demo con tareas de ejemplo."""
    print_separator()
    print("MODO DEMO - Creando tareas de ejemplo...")
    print_separator()

    # Agregar tareas de ejemplo
    manager.add_task(
        title="Completar proyecto Python",
        description="Terminar la aplicacion de gestion de tareas",
        priority=TaskPriority.HIGH,
        due_date=datetime.now() + timedelta(days=3),
    )

    manager.add_task(
        title="Estudiar para examen",
        description="Repasar capitulos 1-5",
        priority=TaskPriority.CRITICAL,
        due_date=datetime.now() + timedelta(days=1),
    )

    manager.add_task(
        title="Hacer ejercicio", description="30 minutos de cardio", priority=TaskPriority.MEDIUM
    )

    task4 = manager.add_task(
        title="Comprar viveres",
        description="Leche, pan, huevos, frutas",
        priority=TaskPriority.LOW,
    )

    # Completar una tarea
    manager.mark_task_completed(task4.task_id)

    print("\n[EXITO] Se crearon 4 tareas de ejemplo.")
    print("Una de ellas ya esta completada.")
    print("\nUsa la opcion 2 para ver todas las tareas.")


def main():
    """Función principal de la aplicación."""
    manager = TaskManager()

    print("\n" + "=" * 70)
    print(" " * 15 + "BIENVENIDO AL GESTOR DE TAREAS")
    print("=" * 70)

    # Preguntar si quiere modo demo
    demo = input("\nDesea cargar tareas de ejemplo? (s/n) [n]: ").strip().lower()
    if demo == "s":
        demo_mode(manager)

    while True:
        print_menu()

        try:
            choice = input("Seleccione una opcion (0-10): ").strip()

            if choice == "0":
                print("\nGracias por usar el Gestor de Tareas. Hasta luego!")
                sys.exit(0)

            elif choice == "1":
                add_task(manager)

            elif choice == "2":
                view_all_tasks(manager)

            elif choice == "3":
                view_tasks_by_status(manager)

            elif choice == "4":
                view_tasks_by_priority(manager)

            elif choice == "5":
                mark_task_in_progress(manager)

            elif choice == "6":
                mark_task_completed(manager)

            elif choice == "7":
                update_task(manager)

            elif choice == "8":
                delete_task(manager)

            elif choice == "9":
                show_statistics(manager)

            elif choice == "10":
                show_overdue_tasks(manager)

            else:
                print("\n[ERROR] Opcion invalida. Por favor seleccione 0-10.")

            input("\nPresione Enter para continuar...")

        except KeyboardInterrupt:
            print("\n\nInterrumpido por el usuario. Hasta luego!")
            sys.exit(0)
        except Exception as e:
            print(f"\n[ERROR INESPERADO] {e}")
            input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()
