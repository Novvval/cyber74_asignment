import httpx

from config import Config

class ApiService:
    url = Config.API_URL

    def __init__(self) -> None:
        self.client = httpx.AsyncClient()

    async def get_products(self) -> list:
        response = await self.client.get(f'{self.url}/product/list')
        return response.json()

    async def get_details(self, id: int) -> dict:
        response = await self.client.get(f'{self.url}/price/{id}')
        return response.json()

    async def add_product(self, link: str) -> dict:
        response = await self.client.post(f'{self.url}/product/?link={link}')
        return response.json()

    async def delete_product(self, id: int) -> dict:
        response = await self.client.delete(f'{self.url}/product/{id}')
        return response.json()
