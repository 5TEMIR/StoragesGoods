from typing import Final
from datetime import datetime


class StorageNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Storage с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class StorageAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Storage с адресом '{address}' уже существует"

    def __init__(self, address: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(address=address)
        super().__init__(self.message)


class GoodsGroupNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "GoodsGroup с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class GoodsGroupAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "GoodsGroup с именем '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(name=name)
        super().__init__(self.message)


class ProducerNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Producer с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class ProducerAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Producer с именем '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(name=name)
        super().__init__(self.message)


class StorageMethodNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "StorageMethod с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class StorageMethodAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "StorageMethod с именем '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(name=name)
        super().__init__(self.message)


class SupplierNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Supplier с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class SupplierAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Supplier с именем '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(name=name)
        super().__init__(self.message)


class ClientNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Client с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class ClientAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Client с именем '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(name=name)
        super().__init__(self.message)


class GoodNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Good с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class GoodAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Good с именем '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(name=name)
        super().__init__(self.message)


class StoragePlaceNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "StoragePlace с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class StoragePlaceAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[
        str] = "StoragePlace для Good с id '{good_id}' уже существует в Storage с id '{storage_id}'"

    def __init__(self, good_id: int, storage_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(good_id=good_id, storage_id=storage_id)
        super().__init__(self.message)


class ReceiptNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Receipt с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class ReceiptAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[
        str] = "Receipt с датой '{receipt_date}' и поставщиком с id '{supplier_id}' уже существует"

    def __init__(self, receipt_date: datetime, supplier_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(receipt_date=receipt_date, supplier_id=supplier_id)
        super().__init__(self.message)


class GoodsReceiptNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[
        str] = "GoodsReceipt с receipt_id {receipt_id} не найдены"
    message: str

    def __init__(self, receipt_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(receipt_id=receipt_id)
        super().__init__(self.message)


class GoodsReceiptAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[
        str] = "GoodsReceipt для Receipt с id '{receipt_id}' и StoragePlace с id '{storage_place_id}' уже существует"

    def __init__(self, receipt_id: int, storage_place_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(receipt_id=receipt_id, storage_place_id=storage_place_id)
        super().__init__(self.message)


class ExpenseNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Expense с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class ExpenseAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Expense с датой '{expens_date}' и клиентом с id '{client_id}' уже существует"

    def __init__(self, expens_date: datetime, client_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(expens_date=expens_date, client_id=client_id)
        super().__init__(self.message)


class GoodsExpenseNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[
        str] = "GoodsExpense с expense_id {expense_id} не найдены"
    message: str

    def __init__(self, expense_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(expense_id=expense_id)
        super().__init__(self.message)


class GoodsExpenseAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[
        str] = "GoodsExpense для Expense с id '{expense_id}' и StoragePlace с id '{storage_place_id}' уже существует"

    def __init__(self, expense_id: int, storage_place_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(expense_id=expense_id, storage_place_id=storage_place_id)
        super().__init__(self.message)


class GoodsTransferNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "GoodsTransfer с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class GoodsTransferAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[
        str] = "GoodsTransfer с датой '{transfer_date}', количеством '{quantity}' и товаром с id '{good_id}' уже существует"

    def __init__(self, transfer_date: datetime, quantity: int, good_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(transfer_date=transfer_date, quantity=quantity,
                                                           good_id=good_id)
        super().__init__(self.message)
