"""
Script de Automatización de Entorno de Desarrollo - Empresa XYZ
Asignatura: Plataformas de Desarrollo de Software
Objetivo: Automatizar la creación del entorno virtual dev_env,
          generación de estructura de directorios (App/, Tests/),
          archivos de configuración (requirements.txt, README.md)
          e instalación de dependencias requeridas.
"""

import os
import sys
import subprocess
import venv

def crear_estructura_directorios():
    """Crea las carpetas base del proyecto: App/ y Tests/"""
    print("[1/5] Creando estructura de directorios del proyecto...")
    directorios = ["App", "Tests"]
    for dir_name in directorios:
        os.makedirs(dir_name, exist_ok=True)
        # Archivo __init__.py para tratar las carpetas como módulos de Python
        init_file = os.path.join(dir_name, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w", encoding="utf-8") as f:
                f.write(f'# Módulo {dir_name}\n')
        print(f"  -> Carpeta creada/verificada: {dir_name}/")

    # Muestra de archivo inicial en App
    sample_app = os.path.join("App", "app.py")
    if not os.path.exists(sample_app):
        with open(sample_app, "w", encoding="utf-8") as f:
            f.write(
                'from flask import Flask\n\n'
                'app = Flask(__name__)\n\n'
                '@app.route("/")\n'
                'def home():\n'
                '    return "Entorno de desarrollo XYZ configurado exitosamente!"\n\n'
                'if __name__ == "__main__":\n'
                '    app.run(debug=True)\n'
            )
        print("  -> Archivo de ejemplo creado: App/app.py")

    # Muestra de test inicial en Tests
    sample_test = os.path.join("Tests", "test_app.py")
    if not os.path.exists(sample_test):
        with open(sample_test, "w", encoding="utf-8") as f:
            f.write(
                'def test_ejemplo():\n'
                '    assert 1 + 1 == 2\n'
            )
        print("  -> Archivo de prueba creado: Tests/test_app.py")


def crear_archivo_requirimientos():
    """Genera los archivos de requerimientos con las dependencias requeridas"""
    print("[2/5] Creando archivo de dependencias requeridas...")
    dependencias = [
        "flask",
        "SQLAlchemy",
        "pytest"
    ]
    contenido = "\n".join(dependencias) + "\n"

    # Se genera requirements.txt y requiriments.txt (por requerimiento literal del anexo)
    for nombre_archivo in ["requirements.txt", "requiriments.txt"]:
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"  -> Archivo creado: {nombre_archivo}")


def crear_archivo_readme():
    """Genera el archivo README.md con instrucciones claras de instalación y ejecución"""
    print("[3/5] Creando archivo README.md...")
    contenido_readme = """# Proyecto Empresa XYZ

Este repositorio cuenta con un entorno de desarrollo automatizado para estandarizar la arquitectura y configuración de proyectos de software en la organización.

## Estructura del Proyecto

```text
.
├── App/                     # Código fuente de la aplicación (Flask, Modelos SQLAlchemy)
│   ├── __init__.py
│   └── app.py
├── Tests/                   # Pruebas automatizadas y unitarias (Pytest)
│   ├── __init__.py
│   └── test_app.py
├── dev_env/                 # Entorno virtual de Python
├── requirements.txt         # Lista de dependencias del proyecto
├── setup.py                 # Script de automatización de entorno
└── README.md                # Documentación del proyecto
```

## Dependencias Principales

- **Flask**: Microframework web ágil y ligero.
- **SQLAlchemy**: ORM para gestión relacional de bases de datos.
- **pytest**: Framework de ejecución de pruebas unitarias robusto y extensible.

## Instrucciones de Uso

### 1. Inicialización y Automatización del Entorno

Si es la primera vez que clona el repositorio o si eliminó el entorno virtual `dev_env`, ejecute:
```bash
python setup.py
```
Este comando crea automáticamente el entorno virtual `dev_env`, las carpetas requeridas (`App/` y `Tests/`), los archivos de dependencias y realiza la instalación de todos los paquetes (`Flask`, `SQLAlchemy`, `pytest`).

### 2. Activar el Entorno Virtual (`dev_env`)

- **En Windows (PowerShell):**
  ```powershell
  .\\dev_env\\Scripts\\Activate.ps1
  ```
- **En Windows (CMD):**
  ```cmd
  dev_env\\Scripts\\activate.bat
  ```
- **En Linux / macOS:**
  ```bash
  source dev_env/bin/activate
  ```

### 3. Ejecutar la Aplicación

Con el entorno activado, ejecute:
```bash
python App/app.py
```

### 4. Ejecutar las Pruebas Unitarias

Para validar las pruebas unitarias con `pytest`:
```bash
pytest
```
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(contenido_readme)
    print("  -> Archivo README.md generado exitosamente.")


def crear_entorno_virtual(env_name="dev_env"):
    """Crea el entorno virtual con pip habilitado"""
    print(f"[4/5] Creando entorno virtual '{env_name}'...")
    if os.path.exists(env_name):
        print(f"  -> El entorno virtual '{env_name}' ya existe. Se reutilizará.")
    else:
        builder = venv.EnvBuilder(with_pip=True)
        builder.create(env_name)
        print(f"  -> Entorno virtual '{env_name}' creado con éxito.")


def instalar_dependencias(env_name="dev_env"):
    """Instala las dependencias en el entorno virtual utilizando su ejecutable de pip"""
    print("[5/5] Instalando dependencias en el entorno virtual...")
    
    # Determinar ruta del ejecutable pip según el sistema operativo
    if sys.platform == "win32":
        pip_path = os.path.join(os.getcwd(), env_name, "Scripts", "pip.exe")
    else:
        pip_path = os.path.join(os.getcwd(), env_name, "bin", "pip")

    if not os.path.exists(pip_path):
        raise FileNotFoundError(f"No se encontró el ejecutable pip en: {pip_path}")

    # Ejecutar instalación mediante subprocess
    cmd = [pip_path, "install", "-r", "requirements.txt"]
    print(f"  -> Ejecutando: {' '.join(cmd)}")
    subprocess.check_call(cmd)
    print("  -> Dependencias (flask, SQLAlchemy, pytest) instaladas exitosamente.")


def main():
    print("=" * 65)
    print(" INICIO DE LA AUTOMATIZACIÓN DE ENTORNO - EMPRESA XYZ")
    print("=" * 65)
    
    try:
        crear_estructura_directorios()
        crear_archivo_requirimientos()
        crear_archivo_readme()
        crear_entorno_virtual("dev_env")
        instalar_dependencias("dev_env")
        
        print("=" * 65)
        print(" ¡CONFIGURACIÓN COMPLETADA SATISFACTORIAMENTE!")
        print(" Entorno listo para desarrollo y pruebas.")
        print("=" * 65)
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un fallo durante la automatización: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
