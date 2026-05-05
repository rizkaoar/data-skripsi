import streamlit as st
import pandas as pd
import os

file_excel = "data_skripsi.xlsx"

if not os.path.exists(file_excel):
    data_awal = pd.DataFrame(columns=[
        "Nama", "NIM", "No HP", "Pembimbing Akademik",
        "Pembimbing Skripsi", "Penguji", "Progres"
    ])
    data_awal.to_excel(file_excel, index=False)

data = pd.read_excel(file_excel, dtype=str).fillna("")

st.title("SISTEM MONITORING MAHASISWA SKRIPSI")

# ========================
# 🔍 CARI DATA
# ========================
st.subheader("Cari Nama / NIM")

cari = st.text_input("Cari nama atau NIM")

if cari != "":
    hasil = data[
        data["Nama"].str.lower().str.contains(cari.lower(), na=False) |
        data["NIM"].str.lower().str.contains(cari.lower(), na=False)
    ]

    if len(hasil) == 0:
        st.write("Data tidak ditemukan")
    else:
        for i, row in hasil.iterrows():
            st.write("Nama:", row["Nama"])
            st.write("NIM:", row["NIM"])
            st.write("No HP:", row["No HP"])
            st.write("Pembimbing Akademik:", row["Pembimbing Akademik"])
            st.write("Pembimbing Skripsi:", row["Pembimbing Skripsi"])
            st.write("Penguji:", row["Penguji"])
            st.write("Progres:", row["Progres"])

            # ========================
            # 🔄 UPDATE PROGRES
            # ========================
            progres_baru = st.selectbox(
                "Update Progres",
                ["Belum", "Judul", "Proposal", "Seminar", "Sidang", "Lulus"],
                key="progres_" + str(row["NIM"])
            )

            if st.button("Update Progres", key="update_" + str(row["NIM"])):
                data.loc[data["NIM"] == row["NIM"], "Progres"] = progres_baru
                data.to_excel(file_excel, index=False)
                st.success("Progres berhasil diupdate")
                st.rerun()

            # ========================
            # 🗑️ HAPUS DATA
            # ========================
            if st.button("Hapus Data Ini", key="hapus_" + str(row["NIM"])):
                data = data[data["NIM"] != row["NIM"]]
                data.to_excel(file_excel, index=False)
                st.success("Data berhasil dihapus")
                st.rerun()

            st.write("---")

# ========================
# ➕ TAMBAH DATA
# ========================
st.subheader("TAMBAH DATA MAHASISWA")

nama = st.text_input("Nama")
nim = st.text_input("NIM")
no_hp = st.text_input("No HP")
pa = st.text_input("Pembimbing Akademik")
ps = st.text_input("Pembimbing Skripsi")
penguji = st.text_input("Penguji")
progres = st.selectbox(
    "Progres",
    ["Belum", "Judul", "Proposal", "Seminar", "Sidang", "Lulus"]
)

if st.button("Simpan Data"):
    if nama == "" or nim == "":
        st.warning("Nama dan NIM wajib diisi")
    elif nim in data["NIM"].values:
        st.error("NIM sudah ada")
    else:
        data_baru = pd.DataFrame({
            "Nama": [nama],
            "NIM": [nim],
            "No HP": [no_hp],
            "Pembimbing Akademik": [pa],
            "Pembimbing Skripsi": [ps],
            "Penguji": [penguji],
            "Progres": [progres]
        })

        data = pd.concat([data, data_baru], ignore_index=True)
        data.to_excel(file_excel, index=False)

        st.success("Data berhasil disimpan")
        