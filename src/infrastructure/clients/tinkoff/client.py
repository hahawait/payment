from config import TinkoffConfig
from infrastructure.clients.base.client import APIClient
from infrastructure.clients.base.exceptions import ClientException
from infrastructure.clients.tinkoff.schemas import SendInvoiceResponse, SendInvoiceSchema


class TinkoffCli(APIClient):
    """Клиент для запросов в АПИ Т-банка"""

    def __init__(self, config: TinkoffConfig) -> None:
        self.config = config
        super().__init__(config.URL)

    async def send_invoice(self, data: SendInvoiceSchema):
        """
        Метод для выставления счетов — номер, срок оплаты, дата выставления, информация о плательщике и другое.
        Логотип и подпись с печатью не проставляются.
        Пользователь должен дать согласие на доступ к созданию и отправке счетов на оплату контрагенту.

        Чтобы использовать метод, нужен доступ — opensme/inn/[{inn}]/kpp/[{kpp}]/invoice/submit
        — Создание, отправка счета на оплату и получение его информации в компании с ИНН {inn} и КПП {kpp}.

        Ограничение на использование метода — 4 запроса в секунду.
        """

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.config.TOKEN}"
        }

        response = await self._make_request(
            method="POST",
            url=self.config.ACCOUNT_FROM_TELEGRAM_ENDPOINT,
            headers=headers,
            json=data.model_dump()
        )

        if response.status != 200:
            message = f"{response.result.get('errorMessage')}\n{response.result.get('errorDetails')}"
            raise ClientException(status_code=response.status, message=message)

        return SendInvoiceResponse(**response.result)
