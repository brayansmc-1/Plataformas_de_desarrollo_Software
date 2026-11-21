"""
Módulo de procesamiento de transacciones financieras y cuentas bancarias.
Diseñado para la demostración de estrategias de testing automatizado en QA.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    SUSPENDED = "SUSPENDED"


class BankingException(Exception):
    """Excepción base para operaciones bancarias."""
    pass


class InvalidAmountError(BankingException):
    """Se lanza cuando el monto ingresado no es válido (<= 0 o no numérico)."""
    pass


class InsufficientFundsError(BankingException):
    """Se lanza cuando el saldo es menor que el monto a retirar o transferir."""
    pass


class AccountInactiveError(BankingException):
    """Se lanza cuando la cuenta de origen o destino no está activa."""
    pass


class DailyLimitExceededError(BankingException):
    """Se lanza cuando la transacción excede el límite operativo diario."""
    pass


@dataclass
class BankAccount:
    account_id: str
    owner: str
    balance: float
    status: AccountStatus = AccountStatus.ACTIVE
    daily_limit: float = 10000.0
    accumulated_daily_transfers: float = 0.0

    def is_active(self) -> bool:
        return self.status == AccountStatus.ACTIVE


class BankService:
    """
    Servicio que implementa la lógica de negocio para depósitos,
    retiros y transferencias bancarias con reglas de validación estrictas.
    """

    MIN_TRANSFER_AMOUNT: float = 1.0
    MAX_SINGLE_TRANSACTION: float = 5000.0
    COMMISSION_RATE: float = 0.015  # 1.5% de comisión por transferencia interbancaria

    @staticmethod
    def _validate_numeric_amount(amount: float) -> None:
        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise InvalidAmountError(f"El monto debe ser un valor numérico válido, recibido: {type(amount).__name__}")
        if amount <= 0:
            raise InvalidAmountError(f"El monto debe ser estrictamente mayor a 0, recibido: {amount}")

    def deposit(self, account: BankAccount, amount: float) -> float:
        """
        Realiza un depósito a una cuenta bancaria.
        Retorna el nuevo saldo de la cuenta.
        """
        self._validate_numeric_amount(amount)
        if not account.is_active():
            raise AccountInactiveError(f"La cuenta {account.account_id} está en estado {account.status.value}")

        account.balance = round(account.balance + amount, 2)
        return account.balance

    def withdraw(self, account: BankAccount, amount: float) -> float:
        """
        Realiza un retiro de una cuenta bancaria.
        Retorna el nuevo saldo de la cuenta.
        """
        self._validate_numeric_amount(amount)
        if not account.is_active():
            raise AccountInactiveError(f"La cuenta {account.account_id} está en estado {account.status.value}")

        if amount > account.balance:
            raise InsufficientFundsError(
                f"Saldo insuficiente. Saldo disponible: {account.balance}, requerido: {amount}"
            )

        account.balance = round(account.balance - amount, 2)
        return account.balance

    def transfer(
        self,
        source: BankAccount,
        target: BankAccount,
        amount: float,
        apply_commission: bool = False
    ) -> dict:
        """
        Realiza una transferencia entre dos cuentas.
        Verifica límites de monto mínimo, monto máximo por transacción y límite diario acumulado.
        """
        self._validate_numeric_amount(amount)

        if not source.is_active():
            raise AccountInactiveError(f"La cuenta de origen {source.account_id} está inactiva.")

        if not target.is_active():
            raise AccountInactiveError(f"La cuenta de destino {target.account_id} está inactiva.")

        if source.account_id == target.account_id:
            raise BankingException("No se pueden realizar transferencias a la misma cuenta de origen.")

        # Casos de borde / límites de transacción
        if amount < self.MIN_TRANSFER_AMOUNT:
            raise InvalidAmountError(
                f"El monto mínimo de transferencia es {self.MIN_TRANSFER_AMOUNT}. Recibido: {amount}"
            )

        if amount > self.MAX_SINGLE_TRANSACTION:
            raise InvalidAmountError(
                f"El monto máximo por transacción única es {self.MAX_SINGLE_TRANSACTION}. Recibido: {amount}"
            )

        commission = round(amount * self.COMMISSION_RATE, 2) if apply_commission else 0.0
        total_debit = round(amount + commission, 2)

        # Validación de saldo suficiente
        if total_debit > source.balance:
            raise InsufficientFundsError(
                f"Fondos insuficientes para cubrir transferencia + comisión ({total_debit}). Saldo: {source.balance}"
            )

        # Validación de límite diario
        if (source.accumulated_daily_transfers + amount) > source.daily_limit:
            remaining_limit = round(source.daily_limit - source.accumulated_daily_transfers, 2)
            raise DailyLimitExceededError(
                f"Excede el límite diario. Límite restante: {remaining_limit}, solicitado: {amount}"
            )

        # Ejecución atómica de la transacción
        source.balance = round(source.balance - total_debit, 2)
        target.balance = round(target.balance + amount, 2)
        source.accumulated_daily_transfers = round(source.accumulated_daily_transfers + amount, 2)

        return {
            "source_id": source.account_id,
            "target_id": target.account_id,
            "transferred_amount": amount,
            "commission": commission,
            "total_debited": total_debit,
            "source_new_balance": source.balance,
            "target_new_balance": target.balance
        }
