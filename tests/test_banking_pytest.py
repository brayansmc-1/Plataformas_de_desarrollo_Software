"""
Suite de Pruebas Automatizadas con Pytest (Enfoque Idiomático QA).
Utiliza fixtures, parametrización (@pytest.mark.parametrize) y pytest.raises.
"""

import pytest
from src.payment_service import (
    BankAccount,
    BankService,
    AccountStatus,
    InvalidAmountError,
    InsufficientFundsError,
    AccountInactiveError,
    DailyLimitExceededError,
)


@pytest.fixture
def bank_service():
    """Fixture que provee una instancia limpia del servicio bancario."""
    return BankService()


@pytest.fixture
def origin_account():
    """Fixture de cuenta origen activa con saldo."""
    return BankAccount(
        account_id="ORIGIN-01",
        owner="Alice QA",
        balance=2500.0,
        status=AccountStatus.ACTIVE,
        daily_limit=6000.0,
        accumulated_daily_transfers=0.0
    )


@pytest.fixture
def destination_account():
    """Fixture de cuenta destino activa."""
    return BankAccount(
        account_id="DEST-02",
        owner="Bob QA",
        balance=300.0,
        status=AccountStatus.ACTIVE,
        daily_limit=6000.0,
        accumulated_daily_transfers=0.0
    )


# =============================================================================
# PRUEBAS POSITIVAS Y PARAMETRIZADAS CON ASSERT
# =============================================================================

@pytest.mark.parametrize("deposit_val, expected_balance", [
    (10.0, 2510.0),
    (500.25, 3000.25),
    (0.01, 2500.01),  # Borde positivo mínimo
])
def test_pytest_parametrized_deposits(bank_service, origin_account, deposit_val, expected_balance):
    """Verificación parametrizada de múltiples depósitos válidos."""
    res = bank_service.deposit(origin_account, deposit_val)
    assert res == expected_balance
    assert origin_account.balance == expected_balance


def test_pytest_transfer_success_with_commission(bank_service, origin_account, destination_account):
    """Caso positivo: Transferencia con cálculo exacto de comisión."""
    receipt = bank_service.transfer(
        source=origin_account,
        target=destination_account,
        amount=500.0,
        apply_commission=True
    )
    # Comisión 1.5% de 500 = 7.5
    assert receipt["transferred_amount"] == 500.0
    assert receipt["commission"] == 7.5
    assert receipt["total_debited"] == 507.5
    assert origin_account.balance == 2500.0 - 507.5
    assert destination_account.balance == 300.0 + 500.0


# =============================================================================
# PRUEBAS DE EXCEPCIONES Y NEGATIVAS CON PYTEST.RAISES
# =============================================================================

@pytest.mark.parametrize("invalid_amount", [-100.0, -0.01, 0.0, "cinco mil", None, False])
def test_pytest_invalid_amounts_raise_exception(bank_service, origin_account, invalid_amount):
    """Verificación de que valores negativos, cero y tipos no numéricos disparen InvalidAmountError."""
    with pytest.raises(InvalidAmountError):
        bank_service.deposit(origin_account, invalid_amount)


def test_pytest_insufficient_funds_exception(bank_service, origin_account):
    """Verificación de excepción por sobregiro/fondos insuficientes."""
    with pytest.raises(InsufficientFundsError) as exc_info:
        bank_service.withdraw(origin_account, 3000.0)
    assert "Saldo insuficiente" in str(exc_info.value)


@pytest.mark.parametrize("status", [AccountStatus.BLOCKED, AccountStatus.SUSPENDED])
def test_pytest_inactive_account_exception(bank_service, origin_account, status):
    """Verificación de que cuentas bloqueadas o suspendidas no puedan transaccionar."""
    origin_account.status = status
    with pytest.raises(AccountInactiveError):
        bank_service.withdraw(origin_account, 100.0)


# =============================================================================
# CASOS DE BORDE (BOUNDARY ANALYSIS)
# =============================================================================

def test_pytest_boundary_withdraw_all_funds(bank_service, origin_account):
    """Borde: Retirar el 100% de los fondos deja el balance en exactamente 0.0."""
    balance = origin_account.balance
    bank_service.withdraw(origin_account, balance)
    assert origin_account.balance == 0.0


@pytest.mark.parametrize("amount, should_pass", [
    (0.99, False),    # Justo debajo del mínimo permitido (1.0)
    (1.0, True),      # Límite inferior exacto
    (5000.0, True),   # Límite superior por transacción exacto
    (5000.01, False)  # Justo por encima del límite superior
])
def test_pytest_transfer_boundaries(bank_service, origin_account, destination_account, amount, should_pass):
    """Análisis de valores límite para montos de transferencia."""
    origin_account.balance = 10000.0
    if should_pass:
        receipt = bank_service.transfer(origin_account, destination_account, amount)
        assert receipt["transferred_amount"] == amount
    else:
        with pytest.raises(InvalidAmountError):
            bank_service.transfer(origin_account, destination_account, amount)
