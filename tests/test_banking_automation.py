"""
Suite de Pruebas Unitarias Automatizadas para QA Bancario.
Compatible tanto con 'unittest' como con 'pytest'.

Criterios cubiertos según el anexo:
1. Escenarios Positivos (valores válidos).
2. Escenarios Negativos (valores inválidos y estados no permitidos).
3. Casos de Borde (valores frontera: saldo exacto a cero, montos mínimos/máximos, límites diarios).
4. Manejo y verificación estricta de excepciones con aserciones (assert).
5. Ejecución nativa con pytest y unittest.
"""

import unittest
from src.payment_service import (
    BankAccount,
    BankService,
    AccountStatus,
    BankingException,
    InvalidAmountError,
    InsufficientFundsError,
    AccountInactiveError,
    DailyLimitExceededError,
)


class TestBankServiceAutomation(unittest.TestCase):
    """Pruebas unitarias de la lógica de negocio bancaria."""

    def setUp(self):
        """Configuración de entorno de prueba antes de cada test."""
        self.service = BankService()
        self.account_a = BankAccount(
            account_id="ACC-001",
            owner="Carlos Pérez",
            balance=1000.0,
            status=AccountStatus.ACTIVE,
            daily_limit=5000.0,
            accumulated_daily_transfers=0.0
        )
        self.account_b = BankAccount(
            account_id="ACC-002",
            owner="María Gómez",
            balance=500.0,
            status=AccountStatus.ACTIVE,
            daily_limit=5000.0,
            accumulated_daily_transfers=0.0
        )

    # =========================================================================
    # 1. ESCENARIOS POSITIVOS (Valores Válidos y Caminos Felices)
    # =========================================================================

    def test_deposit_valid_amount_success(self):
        """Escenario Positivo: Depósito válido incrementa el saldo correctamente."""
        initial_balance = self.account_a.balance
        deposit_amount = 250.50

        new_balance = self.service.deposit(self.account_a, deposit_amount)

        # Aserciones de verificación
        assert new_balance == 1250.50, f"Se esperaba 1250.50 pero se obtuvo {new_balance}"
        assert self.account_a.balance == initial_balance + deposit_amount
        self.assertEqual(self.account_a.balance, 1250.50)

    def test_withdraw_valid_amount_success(self):
        """Escenario Positivo: Retiro de fondos menor al saldo disponible."""
        withdraw_amount = 400.0
        new_balance = self.service.withdraw(self.account_a, withdraw_amount)

        assert new_balance == 600.0, f"Se esperaba 600.0 pero se obtuvo {new_balance}"
        assert self.account_a.balance == 600.0
        self.assertEqual(new_balance, 600.0)

    def test_transfer_without_commission_success(self):
        """Escenario Positivo: Transferencia estándar entre cuentas activas sin comisión."""
        transfer_amount = 300.0

        receipt = self.service.transfer(
            source=self.account_a,
            target=self.account_b,
            amount=transfer_amount,
            apply_commission=False
        )

        assert receipt["transferred_amount"] == 300.0
        assert receipt["commission"] == 0.0
        assert receipt["total_debited"] == 300.0
        assert self.account_a.balance == 700.0
        assert self.account_b.balance == 800.0
        assert self.account_a.accumulated_daily_transfers == 300.0

    def test_transfer_with_commission_success(self):
        """Escenario Positivo: Transferencia interbancaria con comisión del 1.5%."""
        transfer_amount = 1000.0  # Comisión: 15.0, Total debitado: 1015.0
        self.account_a.balance = 2000.0

        receipt = self.service.transfer(
            source=self.account_a,
            target=self.account_b,
            amount=transfer_amount,
            apply_commission=True
        )

        assert receipt["commission"] == 15.0
        assert receipt["total_debited"] == 1015.0
        assert self.account_a.balance == 985.0
        assert self.account_b.balance == 1500.0

    # =========================================================================
    # 2. ESCENARIOS NEGATIVOS (Valores Inválidos y Reglas Violadas)
    # =========================================================================

    def test_deposit_negative_amount_raises_invalid_amount_error(self):
        """Escenario Negativo: Depósito de monto negativo lanza InvalidAmountError."""
        with self.assertRaises(InvalidAmountError) as context:
            self.service.deposit(self.account_a, -50.0)

        assert "estrictamente mayor a 0" in str(context.exception)
        assert self.account_a.balance == 1000.0, "El saldo no debe cambiar tras una operación inválida"

    def test_deposit_invalid_type_raises_invalid_amount_error(self):
        """Escenario Negativo: Pasar un string o booleano como monto lanza InvalidAmountError."""
        with self.assertRaises(InvalidAmountError):
            self.service.deposit(self.account_a, "cien_dolares")  # type: ignore

        with self.assertRaises(InvalidAmountError):
            self.service.deposit(self.account_a, True)  # booleano como monto

    def test_withdraw_insufficient_funds_raises_error(self):
        """Escenario Negativo: Retiro que supera el saldo disponible lanza InsufficientFundsError."""
        excessive_amount = 1500.0  # Saldo disponible es 1000.0

        with self.assertRaises(InsufficientFundsError) as context:
            self.service.withdraw(self.account_a, excessive_amount)

        assert "Saldo insuficiente" in str(context.exception)
        assert self.account_a.balance == 1000.0

    def test_operation_on_blocked_or_suspended_account_raises_error(self):
        """Escenario Negativo: Operar con una cuenta bloqueada o suspendida lanza AccountInactiveError."""
        self.account_a.status = AccountStatus.BLOCKED

        with self.assertRaises(AccountInactiveError):
            self.service.deposit(self.account_a, 100.0)

        with self.assertRaises(AccountInactiveError):
            self.service.withdraw(self.account_a, 50.0)

        with self.assertRaises(AccountInactiveError):
            self.service.transfer(self.account_a, self.account_b, 100.0)

    def test_transfer_to_same_account_raises_banking_exception(self):
        """Escenario Negativo: Transferir hacia la misma cuenta de origen debe ser rechazado."""
        with self.assertRaises(BankingException) as context:
            self.service.transfer(self.account_a, self.account_a, 100.0)

        assert "misma cuenta" in str(context.exception)

    def test_transfer_exceeding_daily_limit_raises_error(self):
        """Escenario Negativo: Transferencia que excede el límite diario acumulado."""
        self.account_a.balance = 10000.0
        self.account_a.accumulated_daily_transfers = 4500.0  # Límite: 5000.0

        # Intento de transferir 600.0 (superaría el límite diario de 5000.0)
        with self.assertRaises(DailyLimitExceededError) as context:
            self.service.transfer(self.account_a, self.account_b, 600.0)

        assert "Excede el límite diario" in str(context.exception)

    # =========================================================================
    # 3. CASOS DE BORDE (Boundary Value Analysis / Valores Límite)
    # =========================================================================

    def test_border_withdraw_exact_balance_leaves_zero(self):
        """Caso de Borde: Retiro del monto exacto del saldo total deja la cuenta en cero."""
        exact_balance = self.account_a.balance  # 1000.0

        new_balance = self.service.withdraw(self.account_a, exact_balance)

        assert new_balance == 0.0, "El saldo resultante debe ser exactamente 0.0"
        assert self.account_a.balance == 0.0

    def test_border_transfer_minimum_allowed_amount(self):
        """Caso de Borde: Transferencia exactamente por el límite mínimo permitido (1.0)."""
        min_allowed = BankService.MIN_TRANSFER_AMOUNT  # 1.0

        receipt = self.service.transfer(self.account_a, self.account_b, min_allowed)

        assert receipt["transferred_amount"] == 1.0
        assert self.account_a.balance == 999.0
        assert self.account_b.balance == 501.0

    def test_border_transfer_just_below_minimum_amount(self):
        """Caso de Borde: Transferencia justo por debajo del límite mínimo (0.99) debe fallar."""
        below_min = 0.99

        with self.assertRaises(InvalidAmountError) as context:
            self.service.transfer(self.account_a, self.account_b, below_min)

        assert "monto mínimo" in str(context.exception)

    def test_border_transfer_maximum_allowed_amount(self):
        """Caso de Borde: Transferencia exactamente por el límite máximo permitido por transacción (5000.0)."""
        self.account_a.balance = 6000.0
        self.account_a.daily_limit = 10000.0
        max_allowed = BankService.MAX_SINGLE_TRANSACTION  # 5000.0

        receipt = self.service.transfer(self.account_a, self.account_b, max_allowed)

        assert receipt["transferred_amount"] == 5000.0
        assert self.account_a.balance == 1000.0
        assert self.account_b.balance == 5500.0

    def test_border_transfer_just_above_maximum_allowed_amount(self):
        """Caso de Borde: Transferencia justo por encima del límite máximo (5000.01) debe fallar."""
        self.account_a.balance = 10000.0
        above_max = 5000.01

        with self.assertRaises(InvalidAmountError) as context:
            self.service.transfer(self.account_a, self.account_b, above_max)

        assert "monto máximo por transacción" in str(context.exception)

    def test_border_zero_amount_deposit_raises_exception(self):
        """Caso de Borde: El valor cero (0.0) debe ser rechazado como monto de depósito."""
        with self.assertRaises(InvalidAmountError):
            self.service.deposit(self.account_a, 0.0)

    def test_border_exact_daily_limit_boundary(self):
        """Caso de Borde: Transferencia que alcanza exactamente el límite diario acumulado."""
        self.account_a.balance = 5000.0
        self.account_a.daily_limit = 3000.0
        self.account_a.accumulated_daily_transfers = 2000.0

        # Transferencia de exactamente 1000.0 para alcanzar los 3000.0 de límite
        receipt = self.service.transfer(self.account_a, self.account_b, 1000.0)

        assert self.account_a.accumulated_daily_transfers == 3000.0
        assert receipt["transferred_amount"] == 1000.0


if __name__ == "__main__":
    # Permite ejecutar directamente el script como suite de pruebas con unittest
    unittest.main(verbosity=2)
