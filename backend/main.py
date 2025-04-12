import os

from fastapi import FastAPI
from storesystem.exceptions import (
    ParchaseItemTransactionException,
    RestockItemTransactionException,
)
from storesystem.models import ItemStockSchema, ParchaseLogSchema, RestockLogSchema

# from fastapi.middleware.cors import CORSMiddleware
from supabase import Client, create_client

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
)
app = FastAPI()


def _read_item_stock():
    return supabase.table("item_stock").select("*").execute()


def _write_parchase_log(parchase_log: ParchaseLogSchema):
    try:
        return (
            supabase.table("parchase_log")
            .insert(parchase_log.model_dump_json())
            .execute()
        )
    except Exception as e:
        raise ParchaseItemTransactionException(f"An Occurred Error!, {e}")


def _write_restock_log(restock_log: RestockLogSchema):
    try:
        return (
            supabase.table("restock_log")
            .insert(restock_log.model_dump_json())
            .execute()
        )
    except Exception as e:
        raise RestockItemTransactionException(f"An Occurred Error!, {e}")


@app.get("/")
def root():
    return {"message": "This is Root. Hello from FastAPI!"}


@app.get("/list_item")
def list_item() -> list[ItemStockSchema]:
    """全在庫情報の取得(残数0も含む)
    Returns:
        list[ItemStockSchema]: 在庫情報
    """
    response = _read_item_stock()
    return [ItemStockSchema(**item) for item in response.data]


@app.get("/diff_stock")
def diff_stock() -> list[ItemStockSchema]:
    """各itemについて、前回Add時からの差分を取る
    Returns:
        list[ItemStockSchema]: 差分？
    """
    return []


@app.get("/parchase_item")
def parchase_item(item_id: str, item_quantity: int) -> None:
    """Userが商品買った際のログ記録
    Args:
        item_id (str): 入荷したItemのItem ID (UUID)
        item_quantity (int): 入荷した個数 (int)

    """
    _write_parchase_log(ParchaseLogSchema(item_id=item_id, item_quantity=item_quantity))
    return None


@app.get("/restock_item")
def restock_item(user_id: str, item_id: str, item_quantity: int) -> None:
    """Snack Memberが在庫入荷した時のログ記録
    Args:
        user_id (str): Snack MemberのUser ID (UUID)
        item_id (str): 入荷したItemのItem ID (UUID)
        item_quantity (int): 入荷した個数 (int)
    """
    _write_restock_log(
        RestockLogSchema(user_id=user_id, item_id=item_id, item_quantity=item_quantity)
    )
    return None
