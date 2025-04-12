import postgrest
from fastapi import APIRouter, HTTPException
from storesystem.app.api.supabase_client import fetch_data, get_table
from storesystem.models import Item, RestockLog

items_router = APIRouter(prefix="/items", tags=["items"])


@items_router.get("/list")
def get_item_list() -> list[Item]:
    """全在庫情報の取得(残数0も含む)
    Returns:
        list[ItemStockSchema]: 在庫情報
    """
    try:
        return [Item(**item) for item in fetch_data("item_stocks")]
    except Exception as e:
        raise e


@items_router.post("/restock")
def restock_item(restock_log: RestockLog):
    """商品の追加
    Args:
        user_id (str): 購入したUserのID
        item_id (str): 追加した商品のUUID
        item_quantity (int): 商品の個数
        item_name (Optiona[str]): 追加した商品の名前 (新規追加のときに使用)
    """
    item = Item(
        item_id=restock_log.item_id,
        item_name=restock_log.item_name,
        item_quantity=restock_log.item_quantity,
    ).model_dump(mode="json")
    get_table("item_stocks").upsert(item).execute()
    try:
        get_table("restock_log").insert(restock_log.model_dump_for_log()).execute()
        return {"message": "Success!"}
    except postgrest.exceptions.APIError as e:
        return HTTPException(status_code=503, detail=e.details)
