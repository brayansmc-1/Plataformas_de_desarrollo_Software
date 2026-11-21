"""
Script Principal - Automatización en QA: Elevando la Eficiencia
Demostración de ejecución de servicios bancarios y ejecución de pruebas unitarias.
"""

import sys
import unittest
from src.payment_service import (
    BankAccount,
    BankService,
    AccountStatus,
    InsufficientFundsError,
    DailyLimitExceededError,
)


def run_demonstration():
    print("=" * 70)
    print("DEMOSTRACIÓN DE LÓGICA DE NEGOCIO Y MANEJO DE EXCEPCIONES EN QA")
    print("=" * 70)

    service = BankService()
    cuenta_origen = BankAccount("CTA-001", "Ana Pérez", 1500.0, AccountStatus.ACTIVE, daily_limit=2000.0)
    cuenta_destino = BankAccount("CTA-002", "Juan Gómez", 300.0, AccountStatus.ACTIVE)

    print("[Estado Inicial]")
    print(f"Cuenta Origen ({cuenta_origen.owner}): Saldo = ${cuenta_origen.balance}, Límite Diario = ${cuenta_origen.daily_limit}")
    print(f"Cuenta Destino ({cuenta_destino.owner}): Saldo = ${cuenta_destino.balance}\n")

    # Caso Positivo 1: Depósito
    print("1. Ejecutando depósito de $500.0 a Cuenta Origen...")
    service.deposit(cuenta_origen, 500.0)
    print(f"   -> Saldo actualizado: ${cuenta_origen.balance}")

    # Caso Positivo 2: Transferencia con comisión
    print("\n2. Ejecutando transferencia de $1000.0 con comisión (1.5%)...")
    recibo = service.transfer(cuenta_origen, cuenta_destino, 1000.0, apply_commission=True)
    print(f"   -> Transferido: ${recibo['transferred_amount']}")
    print(f"   -> Comisión: ${recibo['commission']}")
    print(f"   -> Total debitado: ${recibo['total_debited']}")
    print(f"   -> Nuevo saldo origen: ${recibo['source_new_balance']}")
    print(f"   -> Nuevo saldo destino: ${recibo['target_new_balance']}")
    print(f"   -> Transferencias acumuladas hoy: ${cuenta_origen.accumulated_daily_transfers}")

    # Caso Negativo / Excepción: Fondos insuficientes
    print("\n3. Intentando retiro mayor al saldo (Demostración de Excepción)...")
    try:
        service.withdraw(cuenta_origen, 2000.0)
    except InsufficientFundsError as exc:
        print(f"   [ÉXITO QA - EXCEPCIÓN DETECTADA Y CONTROLADA]: {exc}")

    # Inyectamos saldo para aislar la prueba del límite diario
    service.deposit(cuenta_origen, 4000.0)

    # Caso de Borde / Límite diario: límite es 2000, acumulado ya va 1000, transferir 1500 supera el límite
    print("\n4. Intentando exceder límite diario con saldo suficiente (Demostración de Excepción)...")
    try:
        service.transfer(cuenta_origen, cuenta_destino, 1500.0)
    except DailyLimitExceededError as exc:
        print(f"   [ÉXITO QA - EXCEPCIÓN DE LÍMITE DIARIO DETECTADA]: {exc}")

    print("\n" + "=" * 70)
    print("EJECUTANDO SUITE COMPLETA DE PRUEBAS UNITARIAS AUTOMATIZADAS (UNITTEST / PYTEST)")
    print("=" * 70)


if __name__ == "__main__":
    run_demonstration()
    # Ejecución automática de los tests
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
