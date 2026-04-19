from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import Base, SessionLocal, User, engine
from schemas import UserCreate, UserResponse


# アプリ起動時にテーブル作成
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

# DBセッションを取得する依存性注入 (Dependency Injection)
async def get_db():
    async with SessionLocal() as session:
        yield session

# POSTメソッド: ユーザー作成
@app.post("/users/", response_model=UserResponse)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# GETメソッド: ユーザー一覧取得
@app.get("/users/", response_model=list[UserResponse])
async def read_users(db: AsyncSession = Depends(get_db)) -> list[UserResponse]:
    result = await db.execute(select(User))
    return result.scalars().all()
