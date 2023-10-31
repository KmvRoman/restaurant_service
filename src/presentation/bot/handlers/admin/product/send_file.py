from aiohttp import ClientSession

from src.infrastructure.web.s3.client import S3Client


async def send_file(file_path: str, s3: S3Client, token: str) -> str:
    telegram_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    async with ClientSession() as session:
        async with session.get(url=telegram_url) as resp:
            url = s3.s3_put_object(body=await resp.content.read())
            return url
