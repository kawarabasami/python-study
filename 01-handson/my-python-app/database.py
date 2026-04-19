from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/app_db"

# DBエンジンの作成 (非同期)
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# ベースモデル (TypeORMのBaseEntityのようなもの)
class Base(DeclarativeBase):
    pass

# テーブル定義
class User(Base):
    __tablename__ = "users"

    # Mapped[int] のように型ヒントをつけることで、エディタの補完が効きます
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)