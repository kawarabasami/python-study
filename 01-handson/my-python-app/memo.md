# Python FastAPIハンズオン学習メモ

## import文の文法
- 標準ライブラリ、外部ライブラリ、自作モジュールのimportは同じ構文。
  - 例: `from fastapi import FastAPI`（外部）
  - 例: `from database import User`（自作ファイル）
- ドット（.）はパッケージやモジュールの階層を区切る。
- import文はruffやblackでグループごとに空行が入る（標準/外部/自作）。

## async/await, yield, asynccontextmanager
- `async def`で非同期関数、`await`で非同期処理を待つ。
- `yield`は「値を返して一時停止」する。ジェネレーターやリソース管理で使う。
- `@asynccontextmanager`は非同期コンテキストマネージャーを簡単に作るデコレーター。
- `async with`は非同期リソースの準備・後片付けを自動化。
- FastAPIのlifespanはアプリ起動・終了時の処理をまとめて書ける仕組み。

## FastAPIの依存性注入とリソース管理
- `Depends(get_db)`でDBセッションを自動で取得・クローズ。
- get_db関数はyieldでセッションを渡し、スコープ終了時に自動でクローズ。
- 生成とクローズを同じ関数で担うのがFastAPI流のお作法。

## 型ヒント
- Pythonの型ヒントは `name: str` や `def foo(x: int) -> str:` のように書く。
- 戻り値の型ヒントも推奨（例: `-> UserResponse`）。
- 型ヒントだけでは型ミスは防げない。mypyやPyrightで静的チェックが可能。
- FastAPIの`response_model`と型ヒントは両方書く必要がある。

## テーブル作成・マイグレーション
- `Base.metadata.create_all`は「存在しないテーブルだけ作成」する。
- マイグレーションにはAlembicが定番。

## CLIツール（typer）
- typerでCLIコマンドを簡単に作成できる。
- 非同期関数は`asyncio.run()`で同期関数から呼び出せる。
- コマンド名は関数名のアンダースコアがハイフンに変換される。

## テストと非同期DB
- TestClient（同期）＋async DBは相性が悪い。pytest-asyncioやAsyncClient推奨。
- lifespanのfinallyで `await engine.dispose()` など、DB接続の明示的なクローズ処理が重要。
- テスト時のエラー例：RuntimeError: Event loop is closed など

## その他
- ruffやblackで保存時自動整形したい場合は、VS Codeのformatter設定とpyproject.tomlのline-length設定を活用。
- .gitignoreには__pycache__、.venv、.vscode、*.db、.mypy_cache/などを含める。

---

このメモは、Python/TypeScript経験者向けにFastAPIハンズオンで学んだポイントをまとめたものです。