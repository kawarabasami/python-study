# **🚀 4時間でキャッチアップ！TSエンジニアのためのモダンPythonハンズオン**

このハンズオンでは、TypeScript（Next.js / Apollo / Jest）の経験者が、モダンPythonエコシステム（FastAPI / Typer / PostgreSQL / uv / ruff / pytest）を最速で理解するためのステップを提供します。

## **🧠 0\. TypeScriptとの概念マッピング (読むだけ: 10分)**

まずは脳内の用語をPythonエコシステムに変換しましょう。

| 概念 | TypeScript (Node.js) | モダンPython (本プロジェクト) | 補足 |
| :---- | :---- | :---- | :---- |
| **パッケージ管理** | npm, pnpm | **uv** | Rust製の爆速パッケージ・仮想環境マネージャ。 |
| **Lint / Format** | ESLint \+ Prettier | **ruff** | これもRust製。Flake8(Lint)とBlack(Format)を統合した爆速ツール。 |
| **型システム** | TypeScript | **Type Hints (typing)** | Pythonは動的型付けですが、Type HintsとMypy/Pyrightで静的解析が可能。 |
| **実行時バリデーション** | Zod | **Pydantic** | クラスの型ヒントを元に実行時にデータを検証・変換する強力なライブラリ。 |
| **Web API / サーバー** | Express / Apollo Server | **FastAPI** | Pydanticを内包し、型安全なAPIを爆速で作れるフレームワーク。Swagger UI自動生成。 |
| **CLIツール** | Commander.js | **Typer** | FastAPIの兄弟。型ヒントを使ってCLIを簡単に作れる。 |
| **テスト** | Jest | **pytest** | assert文だけでシンプルに書けるテストフレームワーク。 |
| **DB ORM** | Prisma / TypeORM | **SQLAlchemy** | Python界隈におけるデファクトスタンダードの強力なORM。 |

## **🛠️ 1\. 環境構築とPostgreSQLの起動 (30分)**

### **1-1. uv のインストールとプロジェクト作成**

Node.jsの npm init に相当する作業です。

\# macOS/Linuxの場合 (Windowsの場合は公式ドキュメント参照)  
curl \-LsSf \[https://astral.sh/uv/install.sh\](https://astral.sh/uv/install.sh) | sh

\# プロジェクトの作成  
uv init my-python-app  
cd my-python-app

\# 必要なパッケージの追加 (npm install に相当)  
\# FastAPI本体, サーバー(uvicorn), DB関連, CLI(typer), テスト関連を追加  
uv add fastapi uvicorn sqlalchemy asyncpg pydantic pydantic-settings typer pytest httpx

### **1-2. ruff の設定 (VS Code)**

VS Codeに拡張機能 Ruff (charliermarsh.ruff) をインストールします。

プロジェクトルートに pyproject.toml （package.json相当）が作成されているので、以下を追記します。

\# pyproject.toml の末尾に追記  
\[tool.ruff\]  
line-length \= 88 \# PrettierのprintWidth相当

\[tool.ruff.lint\]  
select \= \["E", "F", "I"\] \# 基本的なエラーと、I(isort: import順序の自動整理)を有効化

### **1-3. Docker ComposeでPostgreSQL起動**

プロジェクトルートに docker-compose.yml を作成し、DBを立ち上げます。

\# docker-compose.yml  
services:  
  db:  
    image: postgres:15-alpine  
    environment:  
      POSTGRES\_USER: user  
      POSTGRES\_PASSWORD: password  
      POSTGRES\_DB: app\_db  
    ports:  
      \- "5432:5432"

docker compose up \-d

## **🌐 2\. FastAPIでAPIとDB接続を実装 (90分)**

Apollo ServerでいうSchemaとResolver、そしてPrismaクライアントの設定を一気にやります。

### **2-1. DBとモデルの定義 (database.py)**

TypeScriptのPrisma schemaやTypeORMのEntityに相当します。

\# database.py  
from sqlalchemy.ext.asyncio import create\_async\_engine, async\_sessionmaker  
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped\_column

DATABASE\_URL \= "postgresql+asyncpg://user:password@localhost:5432/app\_db"

\# DBエンジンの作成 (非同期)  
engine \= create\_async\_engine(DATABASE\_URL, echo=True)  
SessionLocal \= async\_sessionmaker(engine, expire\_on\_commit=False)

\# ベースモデル (TypeORMのBaseEntityのようなもの)  
class Base(DeclarativeBase):  
    pass

\# テーブル定義  
class User(Base):  
    \_\_tablename\_\_ \= "users"

    \# Mapped\[int\] のように型ヒントをつけることで、エディタの補完が効きます  
    id: Mapped\[int\] \= mapped\_column(primary\_key=True, index=True)  
    name: Mapped\[str\] \= mapped\_column(index=True)  
    email: Mapped\[str\] \= mapped\_column(unique=True, index=True)

### **2-2. スキーマ（Pydantic）の定義 (schemas.py)**

APIのリクエスト・レスポンスの型を定義します。Zodのような役割を果たします。

\# schemas.py  
from pydantic import BaseModel, EmailStr

\# リクエスト作成時のバリデーション (Zodスキーマ相当)  
class UserCreate(BaseModel):  
    name: str  
    email: str \# より厳密にするなら pydantic の EmailStr を使います

\# APIレスポンス時の型 (ApolloのGraphQLスキーマの戻り値相当)  
class UserResponse(BaseModel):  
    id: int  
    name: str  
    email: str

    class Config:  
        from\_attributes \= True \# SQLAlchemyのモデルからPydanticモデルへの変換を許可

### **2-3. APIルーティング (main.py)**

ExpressやNext.js(App Router)のAPI Routesに相当します。

\# main.py  
from contextlib import asynccontextmanager  
from fastapi import FastAPI, Depends, HTTPException  
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy.future import select

from database import engine, Base, SessionLocal, User  
from schemas import UserCreate, UserResponse

\# アプリ起動時にテーブルを作成する処理  
@asynccontextmanager  
async def lifespan(app: FastAPI):  
    async with engine.begin() as conn:  
        await conn.run\_sync(Base.metadata.create\_all)  
    yield

app \= FastAPI(lifespan=lifespan)

\# DBセッションを取得する依存性注入 (Dependency Injection)  
async def get\_db():  
    async with SessionLocal() as session:  
        yield session

\# POSTメソッド: ユーザー作成  
@app.post("/users/", response\_model=UserResponse)  
async def create\_user(user: UserCreate, db: AsyncSession \= Depends(get\_db)):  
    \# db\_userはSQLAlchemyのモデル  
    db\_user \= User(name=user.name, email=user.email)  
    db.add(db\_user)  
    await db.commit()  
    await db.refresh(db\_user)  
    return db\_user

\# GETメソッド: ユーザー一覧取得  
@app.get("/users/", response\_model=list\[UserResponse\])  
async def read\_users(db: AsyncSession \= Depends(get\_db)):  
    result \= await db.execute(select(User))  
    users \= result.scalars().all()  
    return users

### **2-4. サーバーの起動と確認**

uv 経由で uvicorn (ASGIサーバー) を起動します。

uv run uvicorn main:app \--reload

💡 **ここがスゴイ！**

ブラウザで http://localhost:8000/docs にアクセスしてください。

FastAPIがType Hints（Pydantic）から**Swagger UI（APIドキュメント）を自動生成**しています。ここから直接APIのテスト実行が可能です。

## **🖥️ 3\. TyperでCLIコマンドを作成 (45分)**

バッチ処理や運用スクリプトを作ります。Commander.jsと同じノリですが、型ヒントのおかげで記述が圧倒的に少ないです。

\# cli.py  
import typer  
import asyncio  
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy.future import select  
from database import SessionLocal, User

app \= typer.Typer()

async def async\_get\_user(email: str):  
    async with SessionLocal() as db:  
        result \= await db.execute(select(User).where(User.email \== email))  
        user \= result.scalars().first()  
        return user

@app.command()  
def get\_user(email: str):  
    """  
    指定したメールアドレスのユーザーを検索して表示します。  
    """  
    \# 非同期関数を同期的なCLIから呼び出すためのイディオム  
    user \= asyncio.run(async\_get\_user(email))  
    if user:  
        typer.echo(f"Found User: {user.name} (ID: {user.id})")  
    else:  
        typer.echo("User not found.")

if \_\_name\_\_ \== "\_\_main\_\_":  
    app()

実行してみましょう：

uv run python cli.py \--help  
uv run python cli.py get\_user test@example.com

## **🧪 4\. Pytestでテストを書く (45分)**

JestでのAPIテストとほぼ同じ感覚です。FastAPIが用意している TestClient を使います。

\# test\_main.py  
from fastapi.testclient import TestClient  
from main import app

\# Jestの \`describe\` はクラスで代用することもありますが、Pythonではフラットに書くことが多いです。  
client \= TestClient(app)

def test\_create\_user():  
    \# Jestの \`it\` や \`test\` に相当  
    response \= client.post(  
        "/users/",  
        json={"name": "Test User", "email": "test@example.com"}  
    )  
    \# Jestの \`expect(response.status).toBe(200)\` に相当  
    assert response.status\_code \== 200  
    data \= response.json()  
    assert data\["name"\] \== "Test User"  
    assert data\["email"\] \== "test@example.com"  
    assert "id" in data

def test\_read\_users():  
    response \= client.get("/users/")  
    assert response.status\_code \== 200  
    data \= response.json()  
    assert isinstance(data, list)

テストの実行：

\# uv経由でpytestを実行  
uv run pytest \-v

## **🤖 5\. Copilot / Agent向けインストラクション (agents.md)**

プロジェクトルートに agents.md または .github/copilot-instructions.md を作成し、以下を記述しておくと、Copilotが的外れな古いPythonコードを生成するのを防げます。

\# Python Project Instructions

\#\# Context  
This is a modern Python project developed by a team using a cutting-edge stack. The developer asking you questions has a strong background in TypeScript (Next.js, Apollo, Jest) but is re-learning Python after a 10-year gap. Explain concepts by drawing analogies to the TypeScript/Node.js ecosystem when helpful.

\#\# Tech Stack  
\- \*\*Package & Environment Manager\*\*: \`uv\` (Use \`uv add\`, \`uv run\` instead of \`pip\` or \`poetry\`)  
\- \*\*Linter & Formatter\*\*: \`ruff\` (Do not suggest \`flake8\`, \`black\`, or \`isort\`)  
\- \*\*Web API Framework\*\*: \`FastAPI\`  
\- \*\*CLI Framework\*\*: \`Typer\`  
\- \*\*Database / ORM\*\*: \`PostgreSQL\` \+ \`SQLAlchemy 2.0\` (Async mode)  
\- \*\*Validation\*\*: \`Pydantic v2\`  
\- \*\*Testing\*\*: \`pytest\`

\#\# Coding Rules & Guidelines  
1\. \*\*Always use Type Hints\*\*: Every function parameter and return value must have type annotations.  
2\. \*\*Asynchronous by Default\*\*: For database operations and FastAPI endpoints, use \`async\`/\`await\` and \`sqlalchemy.ext.asyncio\`.  
3\. \*\*Pydantic v2 Syntax\*\*: Use \`model\_dump()\` instead of \`dict()\`, and \`model\_validate()\` instead of \`parse\_obj()\`.  
4\. \*\*No Legacy Python\*\*: Do not use \`os.path\` (use \`pathlib\`), avoid old string formatting (use f-strings).  
5\. \*\*Clear Separation\*\*: Maintain separation between Pydantic models (Schemas) and SQLAlchemy models (Entities).  
