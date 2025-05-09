from supabase import create_client
import streamlit as st

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

def load_listings():
    res = supabase.table("listings").select("*").order("created_at").execute()
    return res.data if res.data else []

def add_listing(name, marker_id, article_no):
    supabase.table("listings").insert({
        "name": name,
        "marker_id": marker_id,
        "article_no": article_no
    }).execute()

def update_listing(id, name, marker_id, article_no):
    supabase.table("listings").update({
        "name": name,
        "marker_id": marker_id,
        "article_no": article_no
    }).eq("id", id).execute()

def delete_listing(id):
    supabase.table("listings").delete().eq("id", id).execute()
