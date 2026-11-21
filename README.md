# Automatización en QA: Elevando la Eficiencia
## Plataformas de Desarrollo de Software — Foro Semana 5

Este proyecto implementa una **estrategia de testing automatizado y control de excepciones** para un sistema de servicios bancarios transaccionales. Incluye suites de pruebas unitarias que cubren flujos positivos, negativos, casos de borde y verificación estricta de excepciones, ejecutables nativamente tanto con **`pytest`** como con **`unittest`**.

---

## 📁 Estructura del Proyecto

```text
FORO SEMANA 5/
│
├── context/                             # Documentos y anexos de la actividad
│   ├── ISOFV193_F5.pdf
│   └── ISOFV193_F5_Anexo.pdf
│
├── src/                                 # Lógica de negocio del sistema
│   ├── __init__.py
│   └── payment_service.py               # Servicio bancario, cuentas y excepciones
│
├── tests/                               # Suites de pruebas automatizadas
│   ├── __init__.py
│   ├── test_banking_automation.py       # Pruebas duales (unittest + pytest)
│   └── test_banking_pytest.py           # Pruebas idiomáticas con fixtures y parametrización
│
├── main.py                              # Script de demostración interactiva y ejecutor de pruebas
└── README.md                            # Esta guía de ejecución
```

---

## ⚙️ Requisitos Previos

- **Python 3.10 o superior** instalado.
- Entorno virtual configurado en la carpeta `.venv`.
- Dependencias: `pytest`.

---

## 🚀 Guía de Ejecución de Pruebas

Abre una terminal de PowerShell o CMD en la carpeta raíz del proyecto:

### 1. Ejecución con `pytest`

`pytest` ejecuta automáticamente ambas suites de prueba (`tests/test_banking_automation.py` y `tests/test_banking_pytest.py`), reportando un total de **35 pruebas exitosas**:

```powershell
.\.venv\Scripts\pytest.exe -v
```

> **Opciones útiles de pytest:**
> - Para ver salida detallada y tiempos:
>   ```powershell
>   .\.venv\Scripts\pytest.exe -v --durations=0
>   ```
> - Para ejecutar solo un archivo específico:
>   ```powershell
>   .\.venv\Scripts\pytest.exe tests/test_banking_automation.py -v
>   ```

---

### 2. Ejecución con `unittest`

Para ejecutar las pruebas usando el ejecutor nativo de `unittest`:

- **Descubrimiento automático de todas las pruebas:**
  ```powershell
  .\.venv\Scripts\python.exe -m unittest discover -s tests -v
  ```

- **Ejecución directa del archivo de automatización:**
  ```powershell
  .\.venv\Scripts\python.exe tests/test_banking_automation.py
  ```

---

### 3. Ejecución de la Demostración General (`main.py`)

El archivo `main.py` contiene una simulación guiada paso a paso que muestra en consola:
1. Depósitos válidos con actualización de saldo.
2. Transferencias interbancarias con cálculo del 1.5% de comisión.
3. Captura controlada de la excepción por fondos insuficientes (`InsufficientFundsError`).
4. Captura controlada de la excepción por exceso de límite diario (`DailyLimitExceededError`).
5. Ejecución automática de la suite completa de pruebas unitarias.

Para ejecutarlo:
```powershell
.\.venv\Scripts\python.exe main.py
```

---

## 🧪 Resumen de Escenarios de Prueba Cubiertos

| Categoría | Descripción de los Escenarios |
| :--- | :--- |
| **Positivos (Happy Path)** | • Depósitos válidos con incremento exacto del balance.<br>• Retiros válidos dentro del saldo disponible.<br>• Transferencias exitosas entre cuentas activas sin comisión.<br>• Transferencias interbancarias con cálculo y débito exacto de comisión (1.5%). |
| **Negativos** | • Montos negativos o cero en depósitos y retiros.<br>• Tipos de datos no numéricos (`str`, `None`, `bool`).<br>• Retiros y transferencias con saldo insuficiente.<br>• Operaciones sobre cuentas bloqueadas (`BLOCKED`) o suspendidas (`SUSPENDED`).<br>• Transferencias a la misma cuenta de origen.<br>• Transferencias que superan el límite diario acumulado. |
| **Casos de Borde (Boundary Analysis)** | • Retiro del 100% exacto del saldo (deja la cuenta en `$0.00`).<br>• Transferencia por el monto mínimo permitido (`$1.00`).<br>• Rechazo en el límite inferior inmediato (`$0.99`).<br>• Transferencia por el monto máximo permitido por transacción (`$5000.00`).<br>• Rechazo en el límite superior inmediato (`$5000.01`).<br>• Transferencia que alcanza con exactitud el límite diario acumulado. |
| **Verificación de Excepciones** | Comprobación estricta con `with pytest.raises(...)` y `self.assertRaises(...)` de las excepciones personalizadas:<br>• `InvalidAmountError`<br>• `InsufficientFundsError`<br>• `AccountInactiveError`<br>• `DailyLimitExceededError`<br>• `BankingException` |

