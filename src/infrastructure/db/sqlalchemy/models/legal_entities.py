from sqlalchemy import BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.sqlalchemy.models.base import BaseModel


class LegalEntityModel(BaseModel):
    __tablename__ = "legal_entities"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    account_number: Mapped[int] = mapped_column(BIGINT, nullable=False)
    sender_account_number: Mapped[int] = mapped_column(BIGINT, nullable=False)
    payment_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    payment_inn: Mapped[int] = mapped_column(BIGINT, nullable=False)
    payment_kpp: Mapped[int] = mapped_column(BIGINT, nullable=False)
    payment_email: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)

    invoices: Mapped[set["InvoiceModel"]] = relationship("InvoiceModel", back_populates="legal_entity", lazy="selectin")
