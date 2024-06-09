import requests
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Asuransi",
    description="API untuk mengelola data Asuransi",
    docs_url="/",  # Ubah docs_url menjadi "/"
)

@app.get("/")
async def read_root():
    return {"Data":"Successful"}

# Model untuk Data Asuransi
class Asuransi(BaseModel):
    id_asuransi: str
    tanggal_mulai_asuransi : str
    tanggal_selesai_asuransi : str
    jenis_asuransi: str
    premi: str
    objek : str
    keterangan: str

# Dummy data untuk asuransi
data_asuransi = [
    {"id_asuransi": "AA01", "tanggal_mulai_asuransi": "12-09-2023", "tanggal_selesai_asuransi": "12-09-2024", "jenis_asuransi": "Asuransi Kesehatan", "premi": "Rp5.000.000", "objek": "-", "keterangan": "Stroke"},
    {"id_asuransi": "AA02", "tanggal_mulai_asuransi": "11-06-2023", "tanggal_selesai_asuransi": "11-06-2024", "jenis_asuransi": "Asuransi kendaraan", "premi": "Rp15.000.000", "objek": "Mobil", "keterangan": "body rusak"},
    {"id_asuransi": "AA03", "tanggal_mulai_asuransi": "05-05-2023", "tanggal_selesai_asuransi": "05-07-2024", "jenis_asuransi": "Asuransi Kesehatan", "premi": "Rp5.000.000", "objek": "-", "keterangan": "Kaki patah"},
    {"id_asuransi": "AA04", "tanggal_mulai_asuransi": "20-10-2023", "tanggal_selesai_asuransi": "20-10-2024", "jenis_asuransi": "Asuransi Kerusakan", "premi": "Rp8.000.000", "objek": "Furniture", "keterangan": "Kasur rusak"},
    {"id_asuransi": "AA05", "tanggal_mulai_asuransi": "21-11-2023", "tanggal_selesai_asuransi": "21-11-2024", "jenis_asuransi": "Asuransi Kesehatan", "premi": "Rp3.000.000", "objek": "-", "keterangan": "Diabetes"},
]

# Endpoint untuk menambahkan data asuransi
@app.post("/asuransi")
def tambah_asuransi(asuransi: Asuransi):
    data_asuransi.append(asuransi.dict())
    return {"message": "Data asuransi berhasil ditambahkan."}

# Endpoint untuk mendapatkan data asuransi
@app.get("/asuransi", response_model=List[Asuransi])
def get_asuransi():
    return data_asuransi

def get_asuransi_index(id_asuransi):
    for index, asuransi in enumerate(data_asuransi):
        if asuransi['id_asuransi'] == id_asuransi:
            return index
    return None

# Endpoint untuk detail get id
@app.get("/asuransi/{id_asuransi}", response_model=Optional[Asuransi])
def get_asuransi_by_id(id_asuransi: str):
    for asuransi in data_asuransi:
        if asuransi['id_asuransi'] == id_asuransi:
            return Asuransi(**asuransi)
    return None

# Endpoint untuk memperbarui data wisata dengan hanya memasukkan id_wisata
@app.put("/asuransi/{id_asuransi}")
def update_asuransi_by_id(id_asuransi: str, asuransi_baru: Asuransi):
    index = get_asuransi_index(id_asuransi)
    if index is not None:
        data_asuransi[index] = asuransi_baru.dict()
        return {"message": "Data asuransi berhasil diperbarui."}
    else:
        raise HTTPException(status_code=404, detail="Data asuransi tidak ditemukan.")

# Endpoint untuk menghapus data wisata
@app.delete("/asuransi/{id_asuransi}")
def delete_asuransi(id_asuransi: str):
    index = get_asuransi_index(id_asuransi)
    if index is not None:
        del data_asuransi[index]
        return {"message": "Data asuransi berhasil dihapus."}
    else:
        raise HTTPException(status_code=404, detail="Data asuransi tidak ditemukan.")

# Model untuk Data Penduduk 
class Government(BaseModel):
    nik: int
    nama: str
    provinsi: str
    kota: str
    kecamatan: str
    desa: str

# data dari web hosting lain
def get_data_Government_from_web():
    url = "https://api-government.onrender.com/penduduk"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [Government(**item) for item in data]
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data penduduk dari web hosting.")

# Endpoint untuk mendapatkan data penduduk
@app.get("/penduduk", response_model=List[Government])
def get_Government():
    data_Government = get_data_Government_from_web()
    return data_Government

# Fungsi untuk mengambil data Goverment dari web hosting lain
def get_data_pajak_from_web():
    url = "https://api-government.onrender.com/"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data Goverment dari web hosting.")

# Model untuk Data Pajak
class Pajak(BaseModel):
    id_pajak: str
    besar_pajak: float

# Endpoint untuk mendapatkan data pajak
@app.get("/pajak", response_model=List[Pajak])
def get_pajak():
    data_pajak = get_data_pajak_from_web()
    return data_pajak

def get_pajak_index(id_pajak):
    data_pajak = get_data_pajak_from_web()
    for index, pajak in enumerate(data_pajak):
        if pajak['id_pajak'] == id_pajak:
            return index
    return None

@app.get("/pajak/{id_pajak}", response_model=Optional[Pajak])
def get_pajak_by_id(id_pajak: str):
    data_pajak = get_data_pajak_from_web()
    for pajak in data_pajak:
        if pajak['id_pajak'] == id_pajak:
            return Pajak(**pajak)
    return None

# Model untuk Data Tour Guide
class TourGuide(BaseModel):
    id_guider:str
    nama_guider: str

# Fungsi untuk mengambil data 
# guide dari web hosting lain
def get_data_tourGuide_from_web():
    url = "https://tour-guide-ks4n.onrender.com/tourguide"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        data=response.json()
        return [TourGuide(**item) for item in data]
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data Tour Guide dari web hosting.")

# Endpoint untuk mendapatkan data Tour Guide
@app.get("/tourguide", response_model=List[TourGuide])
def get_tourGuide():
    data_tourGuide = get_data_tourGuide_from_web()
    return data_tourGuide

def get_tourGuide_index(id_guider):
    data_tourGuide = get_data_tourGuide_from_web()
    for index, tourGuide in enumerate(data_tourGuide):
        if tourGuide['id_guider'] == id_guider:
            return index
    return None

@app.get("/tourguide/{id_guider}", response_model=Optional[TourGuide])
def get_tourGuide_by_id(id_guider: str):
    data_tourGuide = get_data_tourGuide_from_web()
    for tourGuide in data_tourGuide:
        if tourGuide['id_guider'] == id_guider:
            return TourGuide(**tourGuide)
    return None

# Fungsi untuk mengambil data wisata dari web hosting lain
'''def get_data_wisata_from_web():
    url = "https://example.com/api/pajak"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data Wisata dari web hosting.")

# Model untuk Data Wisata
class Asuransi(BaseModel):
    id_asuransi: int
    nama_wisata: str
    nama_daerah: str

# Endpoint untuk mendapatkan data asuransi
@app.get("/asuransi", response_model=List[Asuransi])
def get_asuransi():
    data_asuransi = get_data_asuransi_from_web()
    return data_asuransi
'''
# Fungsi untuk mengambil data hotel dari web hosting lain
def get_data_hotel_from_web():
    url = "https://example.com/api/pajak"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data Hotel dari web hosting.")

# Model untuk Data Hotel
class Hotel(BaseModel):
    id_room: int
    room_number: int
    room_type: str
    rate: str
    availability: int

# Endpoint untuk mendapatkan data hotel
@app.get("/hotel", response_model=List[Hotel])
def get_hotel():
    data_hotel = get_data_hotel_from_web()
    return data_hotel

# Fungsi untuk mengambil data bank dari web hosting lain
def get_data_bank_from_web():
    url = "https://example.com/api/pajak"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data BANK dari web hosting.")

# Model untuk Data Bank
class Bank(BaseModel):
    id_rekeneing: int
    saldo: int
    activate_date: str
    kabupaten: str

# Endpoint untuk mendapatkan data bank
@app.get("/bank", response_model=List[Bank])
def get_bank():
    data_bank = get_data_bank_from_web()
    return data_bank


def combine_wisata_pajak():
    wisata_data = get_wisata()
    pajak_data = get_pajak()

    combined_data = []
    for wisata in wisata_data:
        for pajak in pajak_data:
            combined_obj = {
                "id_wisata": wisata['id_wisata'],
                "nama_objek": wisata['nama_objek'],
                "pajak": pajak
            }
            combined_data.append(combined_obj)

    return combined_data

class WisataPajak(BaseModel):
    id_wisata: str
    nama_objek: str
    pajak: Pajak

@app.get("/wisataPajak", response_model=List[WisataPajak])
def get_combined_data():
    combined_data = combine_wisata_pajak()
    return combined_data

def combine_wisata_tour_guide():
    wisata_data = get_wisata()
    tour_guide_data = get_tourGuide()

    combined_data = []
    for wisata in wisata_data:
        for tour_guide in tour_guide_data:
            combined_obj = {
                "id_wisata": wisata['id_wisata'],
                "nama_objek": wisata['nama_objek'],
                "tour_guide": tour_guide
            }
            combined_data.append(combined_obj)

    return combined_data

class WisataTourGuide(BaseModel):
    id_wisata: str
    nama_objek: str
    tour_guide: TourGuide

@app.get("/wisataTourGuide", response_model=List[WisataTourGuide])
def get_combined_data():
    combined_data = combine_wisata_tour_guide()
    return combined_data
'''
def combine_wisata_asuransi():
    wisata_data = get_wisata()
    asuransi_data = get_asuransi()

    combined_data = []
    for wisata in wisata_data:
        for asuransi in asuransi_data:
            combined_obj = {
                "id_wisata": wisata['id_wisata'],
                "nama_objek": wisata['nama_objek'],
                "asuransi": asuransi
            }
            combined_data.append(combined_obj)

    return combined_data

class WisataAsuransi(BaseModel):
    id_wisata: str
    nama_objek: str
    asuransi: Asuransi

@app.get("/wisataAsuransi", response_model=List[WisataAsuransi])
def get_combined_data():
    combined_data = combine_wisata_asuransi()
    return combined_data
'''
def combine_wisata_hotel():
    wisata_data = get_wisata()
    hotel_data = get_hotel()

    combined_data = []
    for wisata in wisata_data:
        for hotel in hotel_data:
            combined_obj = {
                "id_wisata": wisata['id_wisata'],
                "nama_objek": wisata['nama_objek'],
                "hotel": hotel
            }
            combined_data.append(combined_obj)

    return combined_data

class WisataHotel(BaseModel):
    id_wisata: str
    nama_objek: str
    hotel: Hotel

@app.get("/wisataHotel", response_model=List[WisataHotel])
def get_combined_data():
    combined_data = combine_wisata_hotel()
    return combined_data

def combine_wisata_bank():
    wisata_data = get_wisata()
    bank_data = get_bank()

    combined_data = []
    for wisata in wisata_data:
        for bank in bank_data:
            combined_obj = {
                "id_wisata": wisata['id_wisata'],
                "nama_objek": wisata['nama_objek'],
                "bank": bank
            }
            combined_data.append(combined_obj)

    return combined_data

class WisataBank(BaseModel):
    id_wisata: str
    nama_objek: str
    bank: Bank

@app.get("/wisataBank", response_model=List[WisataBank])
def get_combined_data():
    combined_data = combine_wisata_bank()
    return combined_data