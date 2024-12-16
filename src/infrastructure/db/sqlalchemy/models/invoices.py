from sqlalchemy import BIGINT, VARCHAR, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.sqlalchemy.models.base import BaseModel


class InvoiceModel(BaseModel):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    legal_entity_id: Mapped[int] = mapped_column(ForeignKey("legal_entities.id"))
    amount: Mapped[int] = mapped_column(BIGINT, nullable=False)
    status: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    json_meta_info: Mapped[dict] = mapped_column(JSON, nullable=False)

    legal_entity: Mapped["LegalEntityModel"] = relationship("LegalEntityModel", back_populates="invoices")
