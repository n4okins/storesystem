import os

from supabase import Client, create_client

supabase_client: Client = create_client(
    os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY")
)


def get_table(table_name: str):
    return supabase_client.table(table_name)


def fetch_data(table_name: str, query: str = "*"):
    return get_table(table_name).select(query).execute().data
