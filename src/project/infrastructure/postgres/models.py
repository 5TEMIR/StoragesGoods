from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, false
from project.infrastructure.postgres.database import Base


class Storage(Base):
    __tablename__ = "storages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False, unique=True)


class GoodsGroup(Base):
    __tablename__ = "goodsgroups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)


class Producer(Base):
    __tablename__ = "producers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    address: Mapped[str] = mapped_column(nullable=True)


class StorageMethod(Base):
    __tablename__ = "storagemethods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    address: Mapped[str] = mapped_column(nullable=True)


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    address: Mapped[str] = mapped_column(nullable=True)


class Good(Base):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    goods_group_id: Mapped[int] = mapped_column(ForeignKey("goodsgroups.id", ondelete="CASCADE", onupdate="CASCADE"))
    producer_id: Mapped[int] = mapped_column(ForeignKey("producers.id", ondelete="CASCADE", onupdate="CASCADE"))
    totalquantity: Mapped[int] = mapped_column(nullable=False)
    storage_method_id: Mapped[int] = mapped_column(
        ForeignKey("storagemethods.id", ondelete="CASCADE", onupdate="CASCADE"))


class StoragePlace(Base):
    __tablename__ = "storageplaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    good_id: Mapped[int] = mapped_column(ForeignKey("goods.id", ondelete="CASCADE", onupdate="CASCADE"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    storage_id: Mapped[int] = mapped_column(ForeignKey("storages.id", ondelete="CASCADE", onupdate="CASCADE"))


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True)
    receip_date: Mapped[datetime] = mapped_column(nullable=False)
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="CASCADE", onupdate="CASCADE"))


class GoodsReceipt(Base):
    __tablename__ = "goodsreceipts"

    receipt_id: Mapped[int] = mapped_column(
        ForeignKey("receipts.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    storage_place_id: Mapped[int] = mapped_column(
        ForeignKey("storageplaces.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)


class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    expens_date: Mapped[datetime] = mapped_column(nullable=False)
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id", ondelete="CASCADE", onupdate="CASCADE"))


class GoodsExpense(Base):
    __tablename__ = "goodsexpenses"

    expense_id: Mapped[int] = mapped_column(
        ForeignKey("expenses.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    storage_place_id: Mapped[int] = mapped_column(
        ForeignKey("storageplaces.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=False)


class GoodsTransfer(Base):
    __tablename__ = "goodstransfers"

    id: Mapped[int] = mapped_column(primary_key=True)
    transfer_date: Mapped[datetime] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    from_storage_id: Mapped[int] = mapped_column(
        ForeignKey("storages.id", ondelete="CASCADE", onupdate="CASCADE"))
    to_storage_id: Mapped[int] = mapped_column(
        ForeignKey("storages.id", ondelete="CASCADE", onupdate="CASCADE"))
    good_id: Mapped[int] = mapped_column(
        ForeignKey("goods.id", ondelete="CASCADE", onupdate="CASCADE"))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=false())
