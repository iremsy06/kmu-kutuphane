import streamlit as st
import pandas as pd
import os
import math
import time
import requests
import re 
import base64
from datetime import datetime, timedelta

st.set_page_config(
    page_title="KMÜ Kütüphane Portalı",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

base_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(base_dir, "assets")
if not os.path.exists(assets_dir): os.makedirs(assets_dir)


FILES = {
    "books": os.path.join(base_dir, "books.csv"),
    "odunc": os.path.join(base_dir, "odunc_hareketleri.csv"),
    "users": os.path.join(base_dir, "kullanicilar.csv"),
    "istek": os.path.join(base_dir, "istek_listesi.csv"),
    "bildirim": os.path.join(base_dir, "bildirimler.csv"),
    "detay": os.path.join(base_dir, "kitap_detaylari.csv")
}


st.markdown("""
<style>
    /* 1. ANA ARKA PLAN (LACİVERT/GECE MAVİSİ) */
    .stApp {
background: linear-gradient(135deg, #1a120b 0%, #3c2a21 50%, #2b1d16 100%);
        
        /* Yazı Rengi (Hafif Krem) */
        color: #f0e6d2;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* LOGO */
    .kmu-logo-img {
        width: 110px; height: 110px; border-radius: 50%;
        border: 3px solid #d4af37; box-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
        object-fit: contain; background-color: white; padding: 5px;
        display: block; margin: 0 auto 15px auto;
    }

    /* GİRİŞ KUTUSU */
    .login-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px; border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    /* INPUTLAR */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px;
    }
    
    /* SEKME VE BUTONLAR */
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(255,255,255,0.05); border-radius: 20px; padding: 5px; }
    .stTabs [aria-selected="true"] { background-color: #F2C94C !important; color: black !important; font-weight: bold; }

    /* KİTAP KARTI */
    .book-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px; padding: 15px; text-align: center;
        transition: transform 0.3s; border: 1px solid rgba(255,255,255,0.1);
        height: 100%; display: flex; flex-direction: column; justify-content: space-between;
    }
    .book-container:hover {
        transform: translateY(-5px); border-color: #d4af37;
        background: rgba(255, 255, 255, 0.08); box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    /* KAPAK */
    .grid-cover-img {
        width: 100%; height: 220px; object-fit: contain;
        border-radius: 5px; margin-bottom: 10px; filter: drop-shadow(0 5px 5px rgba(0,0,0,0.5));
    }

    /* YAZILAR */
    .book-title {
        font-size: 13px; font-weight: bold; color: #fff;
        display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
        margin-bottom: 5px; height: 35px;
    }
    .book-author { font-size: 11px; color: #aaa; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 5px; }
    
    /* STOK */
    .stock-badge {
        font-size: 11px; color: #4ade80; background: rgba(74, 222, 128, 0.1);
        padding: 2px 8px; border-radius: 10px; display: inline-block; margin-bottom: 10px;
        border: 1px solid rgba(74, 222, 128, 0.3);
    }

    /* BUTONLAR (ORİJİNAL ALTIN SARISI) */
    .stButton>button, [data-testid="stLinkButton"] > a {
        background: linear-gradient(90deg, #d4af37 0%, #f2c94c 100%) !important;
        color: #000 !important;
        border: none !important; border-radius: 8px !important; font-weight: bold !important; font-size: 12px !important;
        padding: 8px 16px !important; width: 100% !important; text-transform: uppercase !important; letter-spacing: 1px !important;
        text-decoration: none !important; display: flex !important; justify-content: center !important; align-items: center !important;
    }
    .stButton>button:hover, [data-testid="stLinkButton"] > a:hover { opacity: 0.9; }
    
    /* METRİK KARTLARI */
    .metric-card {
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 15px; text-align: center;
    }
    .metric-title { font-size: 14px; color: #aaa; text-transform: uppercase; }
    .metric-value { font-size: 36px; font-weight: bold; color: #d4af37; margin: 10px 0; }
/* SOL MENÜ (SIDEBAR) TASARIMI */
    section[data-testid="stSidebar"] {
        background-color: #2b1d16 !important; /* Koyu Kahve Zemin */
        background-image: linear-gradient(180deg, #3e2b22 0%, #1a0f0a 100%) !important; /* Hafif Gradyan */
        border-right: 2px solid #d4af37 !important; /* Sağ tarafa altın çizgi */
    }
    
    /* Sol Menüdeki Yazı Renkleri */
    section[data-testid="stSidebar"] * {
        color: #e6f1ff !important; /* Yazılar açık renk kalsın */
    }
    /* FOOTER */
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: rgba(0,0,0,0.8); color: #888; text-align: center; padding: 10px; font-size: 11px; z-index: 999;}
</style>
""", unsafe_allow_html=True)


def init_data():

    schemas = {
        "books": ["Kitap Adi", "Yazar", "isbn", "image", "Link", "Durum"],
        "odunc": ["Ogrenci No", "Kitap Adi", "Alis Tarihi", "Son Teslim Tarihi", "Islem Durumu"],
        "users": ["Ogrenci No", "Ad Soyad", "Email", "Sifre", "AvatarYolu"],
        "istek": ["Ogrenci No", "Kitap Adi", "Tarih"],
        "bildirim": ["Ogrenci No", "Mesaj", "Tarih", "Durum"],
        "detay": ["Kitap Adi", "ResimURL"]
    }
    for key, path in FILES.items():
        if not os.path.exists(path): pd.DataFrame(columns=schemas[key]).to_csv(path, index=False)
    

    if 'df_books' not in st.session_state:
        st.session_state.df_books = pd.read_csv(FILES["books"]).fillna("")
        st.session_state.df_books['AramaMetni'] = (st.session_state.df_books['Kitap Adi'].astype(str) + " " + st.session_state.df_books['Yazar'].astype(str) + " " + st.session_state.df_books['isbn'].astype(str)).str.lower()

    if 'df_users' not in st.session_state: st.session_state.df_users = pd.read_csv(FILES["users"], dtype=str).fillna("")
    if 'df_odunc' not in st.session_state: st.session_state.df_odunc = pd.read_csv(FILES["odunc"], dtype=str).fillna("")
    if 'df_istek' not in st.session_state: st.session_state.df_istek = pd.read_csv(FILES["istek"], dtype=str).fillna("")
    if 'df_bildirim' not in st.session_state: st.session_state.df_bildirim = pd.read_csv(FILES["bildirim"], dtype=str).fillna("")
    if 'df_detay' not in st.session_state: st.session_state.df_detay = pd.read_csv(FILES["detay"]).fillna("")

def save_data(key):

    if key == 'df_books': st.session_state.df_books.drop(columns=['AramaMetni'], errors='ignore').to_csv(FILES["books"], index=False)
    elif key == 'df_users': st.session_state.df_users.to_csv(FILES["users"], index=False)
    elif key == 'df_odunc': st.session_state.df_odunc.to_csv(FILES["odunc"], index=False)
    elif key == 'df_istek': st.session_state.df_istek.to_csv(FILES["istek"], index=False)
    elif key == 'df_bildirim': st.session_state.df_bildirim.to_csv(FILES["bildirim"], index=False)

init_data() 


@st.cache_data(show_spinner=False)
def get_logo():
    LOGO_URL = "https://upload.wikimedia.org/wikipedia/tr/6/69/Karamano%C4%9Flu_Mehmetbey_%C3%9Cniversitesi_logosu.png"
    LOGO_PATH_1 = os.path.join(assets_dir, "logo.png.png")
    LOGO_PATH_2 = os.path.join(assets_dir, "logo.png")
    
    local_path = LOGO_PATH_1 if os.path.exists(LOGO_PATH_1) else (LOGO_PATH_2 if os.path.exists(LOGO_PATH_2) else None)
    if local_path:
        try:
            with open(local_path, "rb") as img_file:
                b64 = base64.b64encode(img_file.read()).decode()
                return f"data:image/png;base64,{b64}"
        except: pass
    return LOGO_URL

final_logo_src = get_logo()

def google_link_getir_DEBUG(isbn, title, author, log_container):
    search_queries = []
    if isbn: search_queries.append(f"isbn:{re.sub(r'[^0-9]','',str(isbn))}")
    if title: search_queries.append(f"intitle:{title}")
    
    for q in search_queries:
        try:
            if log_container: log_container.text(f"Aranıyor: {q}...")
            r = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={q}&maxResults=1", timeout=2)
            if r.status_code == 200:
                data = r.json()
                if "items" in data:
                    v = data["items"][0]["volumeInfo"]
                    link = v.get("previewLink") or v.get("infoLink") or v.get("canonicalVolumeLink")
                    if link: return link
        except: pass
    return ""

def kapak_bul(row):
    if pd.notna(row['image']) and str(row['image']).startswith('http'): return row['image']
    if 'df_detay' in st.session_state:
        d = st.session_state.df_detay
        o = d[d["Kitap Adi"] == row["Kitap Adi"]]
        if not o.empty and pd.notna(o.iloc[0]["ResimURL"]): return o.iloc[0]["ResimURL"]
    return "https://via.placeholder.com/200x300.png?text=Resim+Yok"

def akilli_arama_yap(df, sorgu):
    if not sorgu: return df
    sorgu = sorgu.lower().strip().split()
    mask = pd.Series([True]*len(df))
    for k in sorgu: mask = mask & df['AramaMetni'].str.contains(k, na=False)
    return df[mask]


def giris_ekrani():
    st.write("")
    c1, c2 = st.columns([1.2, 1])
    with c1: st.image("https://images.unsplash.com/photo-1568667256549-094345857637?q=80&w=800&auto=format&fit=crop", use_container_width=True)
    with c2:
        st.markdown(f"""<div class="login-box"><img src="{final_logo_src}" class="kmu-logo-img"><h1 style="color:#fff;text-align:center;font-size:24px;">KMÜ Kütüphane Portalı</h1><p style="color:#d4af37;text-align:center;">Merkez Kütüphane Sistemi</p></div>""", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["GİRİŞ", "KAYIT", "YÖNETİCİ"])
        with t1:
            with st.form("l"):
                no = st.text_input("Öğrenci No"); sif = st.text_input("Şifre", type="password")
                if st.form_submit_button("GİRİŞ YAP 🚀"):
                    u = st.session_state.df_users[(st.session_state.df_users["Ogrenci No"]==no)&(st.session_state.df_users["Sifre"]==sif)]
                    if not u.empty: st.session_state.update({"user":u.iloc[0]["Ad Soyad"], "no":no, "rol":"ogrenci"}); st.rerun()
                    else: st.error("Hatalı!")
        with t2:
            with st.form("r"):
                no = st.text_input("No"); ad = st.text_input("Ad Soyad"); m = st.text_input("Email"); s = st.text_input("Şifre", type="password")
                if st.form_submit_button("KAYDOL ✅"):
                    if no and ad and s:
                        if no not in st.session_state.df_users["Ogrenci No"].values:
                            new = pd.DataFrame([{"Ogrenci No":no,"Ad Soyad":ad,"Email":m,"Sifre":s,"AvatarYolu":""}])
                            st.session_state.df_users = pd.concat([st.session_state.df_users, new], ignore_index=True)
                            save_data("df_users"); st.success("Kaydedildi!")
                        else: st.warning("Kayıtlı!")
        with t3:
            with st.form("a"):
                p = st.text_input("Şifre", type="password")
                if st.form_submit_button("PANEL"):
                    if p=="admin": st.session_state.update({"user":"Admin","rol":"personel"}); st.rerun()
                    else: st.error("Hatalı!")


def show_vitrin(rol, u_no):
    st.markdown("### 📚 Arşiv ve Kitap Yönetimi")
    df = st.session_state.df_books
    c1, c2 = st.columns([3, 1])
    ara = c1.text_input("🔍 Ara...", placeholder="Kitap, Yazar, ISBN...")
    kat = c2.selectbox("Kategori", ["Tümü", "Tarih", "Bilim", "Roman", "Fantastik", "Polisiye"])

    mask = pd.Series([True]*len(df))
    if kat != "Tümü":
        kw = {"Tarih":"tarih","Bilim":"bilim","Roman":"roman","Fantastik":"büyü","Polisiye":"polis"}.get(kat,"")
        mask = mask & df['AramaMetni'].str.contains(kw, na=False)
    if ara:
        for w in ara.lower().split(): mask = mask & df['AramaMetni'].str.contains(w, na=False)
    
    filtered = df[mask]
    if filtered.empty: st.info("Bulunamadı."); return

    PAGE_SIZE = 20
    if "page" not in st.session_state: st.session_state.page = 0
    total_pages = math.ceil(len(filtered)/PAGE_SIZE)
    start = st.session_state.page * PAGE_SIZE
    view_data = filtered.iloc[start:start+PAGE_SIZE]

    c_p, c_i, c_n = st.columns([1, 2, 1])
    if c_p.button("⬅️", disabled=st.session_state.page==0): st.session_state.page-=1; st.rerun()
    c_i.markdown(f"<div style='text-align:center;color:#d4af37'>Sayfa {st.session_state.page+1} / {total_pages}</div>", unsafe_allow_html=True)
    if c_n.button("➡️", disabled=st.session_state.page>=total_pages-1): st.session_state.page+=1; st.rerun()

    st.markdown("---")
    rows = [view_data.iloc[i:i+5] for i in range(0, len(view_data), 5)]
    stok_map = df[df["Durum"]=="Mevcut"]["Kitap Adi"].value_counts()

    for r in rows:
        cols = st.columns(5)
        for i, (idx, row) in enumerate(r.iterrows()):
            with cols[i]:
                stok = stok_map.get(row["Kitap Adi"], 0)
                img = kapak_bul(row)
                st.markdown(f"""<div class="book-container"><img src="{img}" class="grid-cover-img"><div class="book-title">{row['Kitap Adi']}</div><div class="book-author">{row['Yazar']}</div><div class="stock-badge">Stok: {stok}</div>""", unsafe_allow_html=True)
                
                lnk = row.get("Link","")
                if pd.notna(lnk) and len(str(lnk))>5: st.link_button("🌐 İNCELE", lnk, use_container_width=True)
                else: st.write("")

                if rol == "ogrenci":
                    if stok > 0:
                        if st.button("KİRALA", key=f"k_{idx}"):
                            t_idx = st.session_state.df_books[(st.session_state.df_books["Kitap Adi"]==row["Kitap Adi"]) & (st.session_state.df_books["Durum"]=="Mevcut")].index[0]
                            st.session_state.df_books.at[t_idx, "Durum"] = "Oduncte"
                            save_data("df_books")
                            new_o = pd.DataFrame([{"Ogrenci No":u_no, "Kitap Adi":row["Kitap Adi"], "Alis Tarihi":datetime.now().strftime("%Y-%m-%d"), "Son Teslim Tarihi":(datetime.now()+timedelta(days=15)).strftime("%Y-%m-%d"), "Islem Durumu":"Aktif"}])
                            st.session_state.df_odunc = pd.concat([st.session_state.df_odunc, new_o], ignore_index=True)
                            save_data("df_odunc")
                            st.toast("Kiralandı!", icon="✅"); time.sleep(0.5); st.rerun()
                    else:
                        if st.button("🔔 İSTEK", key=f"rq_{idx}"):
                            new_r = pd.DataFrame([{"Ogrenci No":u_no, "Kitap Adi":row["Kitap Adi"], "Tarih":datetime.now().strftime("%Y-%m-%d")}])
                            st.session_state.df_istek = pd.concat([st.session_state.df_istek, new_r], ignore_index=True)
                            save_data("df_istek")
                            st.success("Eklendi!")
                elif rol == "personel":
                    if st.button("🗑️ SİL", key=f"d_{idx}"):
                        st.session_state.df_books = st.session_state.df_books.drop(idx)
                        save_data("df_books")
                        st.success("Silindi!"); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)


if "user" not in st.session_state:
    giris_ekrani()
else:
    user, rol, u_no = st.session_state["user"], st.session_state["rol"], st.session_state.get("no","0")
    

    if rol == "ogrenci":
        ns = st.session_state.df_bildirim
        my_n = ns[(ns["Ogrenci No"]==u_no) & (ns["Durum"]=="Okunmadi")]
        if not my_n.empty:
            for _, n in my_n.iterrows(): st.toast(f"📢 {n['Mesaj']}")
            st.session_state.df_bildirim.loc[(st.session_state.df_bildirim["Ogrenci No"]==u_no), "Durum"]="Okundu"
            save_data("df_bildirim")

    with st.sidebar:
        st.markdown(f"<div style='text-align:center;color:#d4af37'><h3>{user}</h3><p>{rol.upper()}</p></div>", unsafe_allow_html=True)
        u_d = st.session_state.df_users[st.session_state.df_users["Ogrenci No"]==u_no]
        pp = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
        if not u_d.empty and os.path.exists(u_d.iloc[0]["AvatarYolu"]): pp = u_d.iloc[0]["AvatarYolu"]
        st.image(pp, width=120)
        st.markdown("---")
        if st.button("ÇIKIŞ", use_container_width=True): st.session_state.clear(); st.rerun()

    if rol == "ogrenci":
        m = st.sidebar.radio("MENÜ", ["💎 Koleksiyon", "📚 Kitaplarım", "⚙️ Profil"])
        if m == "💎 Koleksiyon": show_vitrin(rol, u_no)
        elif m == "📚 Kitaplarım":
            st.markdown("### 📚 Kiraladıklarım")
            df_o = st.session_state.df_odunc
            my = df_o[(df_o["Ogrenci No"]==u_no)&(df_o["Islem Durumu"]=="Aktif")]
            if not my.empty:
                st.dataframe(my[["Kitap Adi","Son Teslim Tarihi"]], use_container_width=True)
                iade = st.selectbox("İade:", my["Kitap Adi"].unique())
                if st.button("İADE ET"):
                    st.session_state.df_books.loc[st.session_state.df_books["Kitap Adi"]==iade, "Durum"] = "Mevcut"
                    save_data("df_books")
                    idx = df_o[(df_o["Ogrenci No"]==u_no)&(df_o["Kitap Adi"]==iade)&(df_o["Islem Durumu"]=="Aktif")].index[0]
                    st.session_state.df_odunc.at[idx, "Islem Durumu"] = "Teslim Edildi"
                    save_data("df_odunc")
                    # Bildirim Tetikle
                    reqs = st.session_state.df_istek
                    waits = reqs[reqs["Kitap Adi"]==iade]
                    if not waits.empty:
                        new_n = [{"Ogrenci No":w["Ogrenci No"], "Mesaj":f"'{iade}' geldi!", "Tarih":datetime.now().strftime("%Y-%m-%d"), "Durum":"Okunmadi"} for _, w in waits.iterrows()]
                        st.session_state.df_bildirim = pd.concat([st.session_state.df_bildirim, pd.DataFrame(new_n)], ignore_index=True)
                        save_data("df_bildirim")
                        st.session_state.df_istek = reqs[reqs["Kitap Adi"]!=iade]
                        save_data("df_istek")
                    st.success("İade edildi!"); st.rerun()
            else: st.info("Kitap yok.")
        elif m == "⚙️ Profil":
            idx = st.session_state.df_users[st.session_state.df_users["Ogrenci No"]==u_no].index[0]
            with st.form("pf"):
                mail = st.text_input("Email", value=st.session_state.df_users.at[idx,"Email"])
                sif = st.text_input("Şifre", value=st.session_state.df_users.at[idx,"Sifre"])
                up = st.file_uploader("Resim", type=["jpg","png"])
                if st.form_submit_button("GÜNCELLE"):
                    st.session_state.df_users.at[idx,"Email"]=mail
                    st.session_state.df_users.at[idx,"Sifre"]=sif
                    if up:
                        p = os.path.join(assets_dir, f"{u_no}.png")
                        with open(p, "wb") as f: f.write(up.getbuffer())
                        st.session_state.df_users.at[idx,"AvatarYolu"]=p
                    save_data("df_users"); st.success("Güncellendi!"); st.rerun()

    elif rol == "personel":
        page = st.sidebar.radio("Panel", ["🏠 Genel", "📚 Vitrin", "👥 Üyeler", "📋 Hareketler", "✏️ Link", "➕ Ekle"])
        if page == "🏠 Genel":
            st.markdown("### 📊 Genel Bakış")
            tb = len(st.session_state.df_books)
            al = len(st.session_state.df_odunc[st.session_state.df_odunc["Islem Durumu"]=="Aktif"])
            uc = len(st.session_state.df_users)
            c1,c2,c3=st.columns(3)
            c1.markdown(f"<div class='metric-card'><div class='metric-title'>Kitap</div><div class='metric-value'>{tb}</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='metric-card'><div class='metric-title'>Ödünç</div><div class='metric-value'>{al}</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='metric-card'><div class='metric-title'>Üye</div><div class='metric-value'>{uc}</div></div>", unsafe_allow_html=True)
            st.markdown("---")
            st.bar_chart(st.session_state.df_books[st.session_state.df_books["Durum"]=="Mevcut"]["Kitap Adi"].value_counts().head(10))
        elif page == "📚 Vitrin": show_vitrin(rol, "0")
        elif page == "👥 Üyeler":
            users = st.session_state.df_users
            sel = st.selectbox("Üye Seç:", ["Seçiniz..."]+list(users["Ad Soyad"]+" ("+users["Ogrenci No"]+")"))
            if sel != "Seçiniz...":
                no = sel.split("(")[1].replace(")","")
                u_i = users[users["Ogrenci No"]==no].iloc[0]
                c1,c2=st.columns([1,3])
                with c1:
                    im = u_i["AvatarYolu"] if os.path.exists(u_i["AvatarYolu"]) else "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
                    st.image(im, width=150)
                with c2: st.write(f"**Ad:** {u_i['Ad Soyad']}"); st.write(f"**Email:** {u_i['Email']}")
                t1,t2=st.tabs(["Kitaplar","İstekler"])
                with t1:
                    ods = st.session_state.df_odunc
                    st.dataframe(ods[(ods["Ogrenci No"]==no)&(ods["Islem Durumu"]=="Aktif")][["Kitap Adi","Son Teslim Tarihi"]], use_container_width=True)
                with t2:
                    rqs = st.session_state.df_istek
                    st.dataframe(rqs[rqs["Ogrenci No"]==no][["Kitap Adi","Tarih"]], use_container_width=True)
            st.markdown("---")
          
            disp = users.copy()[["Ogrenci No", "Ad Soyad"]]
            o = st.session_state.df_odunc
            disp["Aktif"] = disp["Ogrenci No"].apply(lambda x: len(o[(o["Ogrenci No"]==x)&(o["Islem Durumu"]=="Aktif")]))
            disp["Toplam"] = disp["Ogrenci No"].apply(lambda x: len(o[o["Ogrenci No"]==x]))
            st.dataframe(disp, use_container_width=True)
        elif page == "📋 Hareketler":
            if not st.session_state.df_odunc.empty:
                sh = st.session_state.df_odunc.copy()
                def cz(r):
                    if r["Islem Durumu"]=="Aktif":
                        try:
                            d = datetime.strptime(r["Son Teslim Tarihi"], "%Y-%m-%d").date()
                            if datetime.now().date()>d: return (datetime.now().date()-d).days * 1.0
                        except: pass
                    return 0.0
                sh["Ceza"] = sh.apply(cz, axis=1)
                st.dataframe(sh.style.apply(lambda x: ['background-color:#ff4b4b;color:white' if x["Ceza"]>0 else '' for i in x], axis=1), use_container_width=True)
                if st.button("📧 GECİKENLERE UYARI AT"): st.success("Gönderildi!")
            else: st.info("Veri yok.")
        elif page == "✏️ Link":
            if st.button("🔄 TARA", type="primary"):
                bs = st.session_state.df_books
                ms = bs[(bs["Link"]=="")|(bs["Link"].isnull())]
                p=st.progress(0); log=st.empty(); tot=len(ms); c=0
                for i, (idx, r) in enumerate(ms.iterrows()):
                    log.text(f"Aranıyor: {r['Kitap Adi']}")
                    l = google_link_getir_DEBUG(r["isbn"], r["Kitap Adi"], r["Yazar"], None)
                    st.session_state.df_books.at[idx, "Link"] = l if l else " "
                    c+=1; p.progress((i+1)/tot)
                save_data("df_books"); log.empty(); st.success(f"{c} güncellendi!"); time.sleep(1); st.rerun()
            bk = st.selectbox("Düzenle:", st.session_state.df_books["Kitap Adi"].unique())
            if bk:
                idx = st.session_state.df_books[st.session_state.df_books["Kitap Adi"]==bk].index[0]
                r = st.session_state.df_books.loc[idx]
                im = st.text_input("Resim", value=str(r["image"])); ln = st.text_input("Link", value=str(r["Link"]))
                st.link_button("Ara", f"https://www.google.com/search?q={bk}")
                if st.button("GÜNCELLE"):
                    st.session_state.df_books.at[idx,"image"]=im; st.session_state.df_books.at[idx,"Link"]=ln
                    save_data("df_books"); st.success("Tamam!")
        elif page == "➕ Ekle":
            with st.form("ad"):
                a=st.text_input("Ad"); y=st.text_input("Yazar"); i=st.text_input("ISBN"); r=st.text_input("Resim"); l=st.text_input("Link"); n=st.number_input("Adet",1,50,1)
                if st.form_submit_button("EKLE"):
                    nw = pd.DataFrame([{"Kitap Adi":a,"Yazar":y,"isbn":i,"image":r,"Link":l,"Durum":"Mevcut"}]*n)
                    st.session_state.df_books = pd.concat([st.session_state.df_books, nw], ignore_index=True)
                    save_data("df_books"); st.success("Eklendi!")

st.markdown('<div class="footer">KMÜ Kütüphane Otomasyon Sistemi © 2025</div>', unsafe_allow_html=True)