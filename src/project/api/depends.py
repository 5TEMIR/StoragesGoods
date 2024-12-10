from project.infrastructure.postgres.repository.storage_repo import StorageRepository
from project.infrastructure.postgres.repository.goodsgroup_repo import GoodsGroupRepository
from project.infrastructure.postgres.repository.producer_repo import ProducerRepository
from project.infrastructure.postgres.repository.storagemethod_repo import StorageMethodRepository
from project.infrastructure.postgres.repository.supplier_repo import SupplierRepository
from project.infrastructure.postgres.repository.client_repo import ClientRepository
from project.infrastructure.postgres.repository.good_repo import GoodRepository
from project.infrastructure.postgres.repository.storageplace_repo import StoragePlaceRepository
from project.infrastructure.postgres.repository.receipt_repo import ReceiptRepository
from project.infrastructure.postgres.repository.expense_repo import ExpenseRepository
from project.infrastructure.postgres.repository.goodstransfer_repo import GoodsTransferRepository
from project.infrastructure.postgres.repository.goodsreceipt_repo import GoodsReceiptRepository
from project.infrastructure.postgres.repository.goodsexpense_repo import GoodsExpenseRepository
from project.infrastructure.postgres.database import PostgresDatabase

storage_repo = StorageRepository()
goodsgroup_repo = GoodsGroupRepository()
producer_repo = ProducerRepository()
storage_method_repo = StorageMethodRepository()
supplier_repo = SupplierRepository()
client_repo = ClientRepository()
good_repo = GoodRepository()
storage_place_repo = StoragePlaceRepository()
receipt_repo = ReceiptRepository()
expense_repo = ExpenseRepository()
goods_transfer_repo = GoodsTransferRepository()
goods_receipt_repo = GoodsReceiptRepository()
goods_expense_repo = GoodsExpenseRepository()
database = PostgresDatabase()
