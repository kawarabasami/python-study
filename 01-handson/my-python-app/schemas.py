from pydantic import BaseModel, EmailStr


# リクエスト作成時のバリデーション
class UserCreate(BaseModel):
    name: str
    email: EmailStr

# APIレスポンス時の型
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True  # SQLAlchemyのモデルからPydanticモデルへの変換を許可