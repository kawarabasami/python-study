
import asyncio

import typer
from sqlalchemy import select

from database import SessionLocal, User

app = typer.Typer()

async def async_get_user(email: str):
    async with SessionLocal() as db: 
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        return user

@app.command()
def test(value: str):
    """
    引数をそのまま表示するテストコマンドです。
    """
    typer.echo(f"入力された値: {value}")

@app.command()
def get_user(email: str):
    """
    指定されたメールアドレスのユーザーを取得します。
    """
    # 非同期関数を同期的に呼び出す
    user = asyncio.run(async_get_user(email))
    if user:
        typer.echo(f"ユーザーが見つかりました: {user.name} ({user.email})")
    else:
        typer.echo("ユーザーが見つかりませんでした。")

if __name__ == "__main__":
    app()