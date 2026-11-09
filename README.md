# Proyecto Empresa XYZ

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
  .\dev_env\Scripts\Activate.ps1
  ```
- **En Windows (CMD):**
  ```cmd
  dev_env\Scripts\activate.bat
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
