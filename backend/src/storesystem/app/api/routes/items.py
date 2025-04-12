import datetime

import postgrest
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from storesystem.app.api.supabase_client import fetch_data, get_table
from storesystem.models import Item, ParchaseLog, RestockLog

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
    current_items = [
        Item(**item)
        for item in (
            get_table("item_stocks")
            .select("*")
            .eq("item_id", restock_log.item_id)
            .execute()
        ).data
    ]

    if current_items:  # 既に商品データがある場合は現在の個数取得 + Update
        # item_idで取得したため要素が1つであることは保証されている
        current_item = current_items.pop()
        get_table("item_stocks").update(
            dict(item_quantity=current_item.item_quantity + restock_log.item_quantity)
        ).eq("item_id", restock_log.item_id).execute()
    else:  # 商品データがない場合はInsert
        item = Item(
            item_id=restock_log.item_id,
            item_name=restock_log.item_name,
            item_quantity=restock_log.item_quantity,
        )
        get_table("item_stocks").insert(item.model_dump(mode="json")).execute()
    try:
        get_table("restock_log").insert(restock_log.model_dump_for_log()).execute()
        return {"message": "Success!"}
    except postgrest.exceptions.APIError as e:
        raise HTTPException(status_code=404, detail=e.details)


@items_router.post("/parchase")
def parchase_item(parchase_log: ParchaseLog):
    try:
        current_items = [
            Item(**item)
            for item in (
                get_table("item_stocks")
                .select("*")
                .eq("item_id", parchase_log.item_id)
                .execute()
            ).data
        ]
    except ValidationError:
        raise HTTPException(
            status_code=404, detail=f"ItemID={parchase_log.item_id}の在庫は0です。"
        )

    if len(current_items) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"ItemID={parchase_log.item_id}が存在しません。",
        )
    # item_idで取得したため要素が1つであることは保証されている
    current_item = current_items.pop()
    if current_item.item_quantity - parchase_log.item_quantity < 0:
        raise HTTPException(
            status_code=404, detail="購入する商品の在庫がマイナスになってしまいます！"
        )
    get_table("item_stocks").update(
        dict(item_quantity=current_item.item_quantity - parchase_log.item_quantity)
    ).eq("item_id", parchase_log.item_id).execute()
    try:
        get_table("parchase_log").insert(parchase_log.model_dump_for_log()).execute()
        return {"message": "Success!"}
    except postgrest.exceptions.APIError as e:
        raise HTTPException(status_code=404, detail=e.details)


@items_router.get("/diff")
def diff_log_item(): ...
