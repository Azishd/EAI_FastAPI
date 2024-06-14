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
    url = "https://api-government.onrender.com/pendudukasuransi"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data penduduk dari web hosting.")

# Endpoint untuk mendapatkan data penduduk
@app.get("/pendudukasuransi", response_model=List[Government])
def get_Government():
    data_Government = get_data_Government_from_web()
    return data_Government

# Mengambil data spesifik dengan NIK
@app.get("/pendudukasuransi/{nik}", response_model=Optional[Government])
def get_penduduk_by_nik(nik: int):
    data_Government = get_data_Government_from_web()
    for government in data_Government:
        if government['nik'] == nik:
            return Government(**government)
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
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data Tour Guide dari web hosting.")

# Endpoint untuk mendapatkan data Tour Guide
@app.get("/tourguide", response_model=List[TourGuide])
def get_tourGuide():
    data_tourguide = get_data_tourGuide_from_web()
    return data_tourguide

def get_tourGuide_index(id_guider):
    data_tourguide = get_data_tourGuide_from_web()
    for index, tourguide in enumerate(data_tourguide):
        if tourguide['id_guider'] == id_guider:
            return index
    return None

@app.get("/tourguide/{id_guider}", response_model=Optional[TourGuide])
def get_tourguide_by_id(id_guider: str):
    data_tourguide = get_data_tourGuide_from_web()
    for tourguide in data_tourguide:
        if tourguide['id_guider'] == id_guider:
            return TourGuide(**tourguide)
    return None

# Model untuk Data Tour Guide
class ObjekWisata(BaseModel):
    id_wisata:str
    nama_objek: str
    alamat: str
    kontak: str

# Fungsi untuk mengambil data 
# guide dari web hosting lain
def get_data_objekWisata_from_web():
    url = "https://pajakobjekwisata.onrender.com/wisata"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data Objek Wisata dari web hosting.")

# Endpoint untuk mendapatkan data Tour Guide
@app.get("/objekwisata", response_model=List[ObjekWisata])
def get_objekWisata():
    data_objekwisata = get_data_objekWisata_from_web()
    return data_objekwisata

def get_objekWisata_index(id_wisata):
    data_objekwisata = get_data_objekWisata_from_web()
    for index, objekwisata in enumerate(data_objekwisata):
        if objekwisata['id_wisata'] == id_wisata:
            return index
    return None

@app.get("/objekwisata/{id_wisata}", response_model=Optional[ObjekWisata])
def get_objekwisata_by_id(id_wisata: str):
    data_objekwisata = get_data_objekWisata_from_web()
    for objekwisata in data_objekwisata:
        if objekwisata['id_wisata'] == id_wisata:
            return ObjekWisata(**objekwisata)
    return None



# Model untuk Data Mobil
class Mobil(BaseModel):
    id_mobil:str
    
# Fungsi untuk mengambil data 
# guide dari web hosting lain
def get_data_Mobil_from_web():
    url = "https://rental-mobil-api.onrender.com/mobil"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data Mobil dari web hosting.")

# Endpoint untuk mendapatkan data Mobil
@app.get("/mobil", response_model=List[Mobil])
def get_Mobil():
    data_Mobil = get_data_Mobil_from_web()
    return data_Mobil

def get_Mobil_index(id_mobil):
    data_Mobil = get_data_Mobil_from_web()
    for index, mobil in enumerate(data_Mobil):
        if mobil['id_mobil'] == id_mobil:
            return index
    return None

@app.get("/mobil/{id_mobil}", response_model=Optional[Mobil])
def get_Mobil_by_id(id_mobil: str):
    data_Mobil = get_data_Mobil_from_web()
    for mobil in data_Mobil:
        if mobil['id_mobil'] == id_mobil:
            return Mobil(**mobil)
    return None


# Model untuk Data Hotel
class Hotel(BaseModel):
    RoomID: str

# Fungsi untuk mengambil data hotel dari web hosting lain
def get_data_hotel_from_web():
    url = "https://hotelbaru.onrender.com/reservations"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data Hotel dari web hosting.")

# Endpoint untuk mendapatkan data hotel
@app.get("/hotel", response_model=List[Hotel])
def get_hotel():
    data_hotel = get_data_hotel_from_web()
    return data_hotel

def get_Hotel_index(RoomID):
    data_hotel = get_data_hotel_from_web()
    for index, hotel in enumerate(data_hotel):
        if hotel['RoomID'] == RoomID:
            return index
    return None

# Model untuk Data Asuransi
class Bank(BaseModel):
    id_asuransi: int
    id_bayar : int
    nama : str
    kategori: str
    jumlah: int
    tagihan: int

# Dummy data untuk asuransi-bank
data_bank = [
    {"id_asuransi": 116, "id_bayar": 201, "nama": "Ali", "kategori": "Kendaraan", "jumlah": 60, "tagihan": 100000},
    {"id_asuransi": 117, "id_bayar": 202, "nama": "Sandra", "kategori": "Furniture", "jumlah": 60, "tagihan": 200000},
    {"id_asuransi": 118, "id_bayar": 203, "nama": "Joseph", "kategori": "Kendaraan", "jumlah": 50, "tagihan": 150000},
    {"id_asuransi": 119, "id_bayar": 204, "nama": "Lisa", "kategori": "Kesehatan", "jumlah": 10, "tagihan": 150000},
    {"id_asuransi": 120, "id_bayar": 205, "nama": "Bagas", "kategori": "Kesehatan", "jumlah": 10, "tagihan": 100000},
]

# Endpoint untuk menambahkan data asuransi-bank
@app.post("/bank")
def tambah_asuransi(bank: Bank):
    data_bank.append(bank.dict())
    return {"message": "Data pembayaran berhasil ditambahkan."}

# Endpoint untuk mendapatkan data bank
@app.get("/bank", response_model=List[Bank])
def get_bank():
    url = "https://jumantaradev.my.id/api/asuransi"  # Ganti dengan URL yang sebenarnya
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Gagal mengambil data pembayaran dari web hosting.")

def get_bank_index(id_bank):
    for index, bank in enumerate(data_bank):
        if bank['id_asuransi'] == id_bank:
            return index
    return None

# Endpoint untuk detail get id
@app.get("/bank/{id_asuransi}", response_model=Optional[Bank])
def get_bank_by_id(id_asuransi: int):
    for bank in data_bank:
        if bank['id_asuransi'] == id_asuransi:
            return bank(**bank)
    return None

# Endpoint untuk memperbarui data wisata dengan hanya memasukkan id_wisata
@app.put("/bank/{id_asuransi}")
def update_bank_by_id(id_asuransi: str, bank_baru: Bank):
    index = get_bank_index(id_asuransi)
    if index is not None:
        data_bank[index] = bank_baru.dict()
        return {"message": "Data pembayaran berhasil diperbarui."}
    else:
        raise HTTPException(status_code=404, detail="Data pembayaran tidak ditemukan.")

# Endpoint untuk menghapus data wisata
@app.delete("/bank/{id_bank}")
def delete_bank(id_asuransi: str):
    index = get_bank_index(id_asuransi)
    if index is not None:
        del data_bank[index]
        return {"message": "Data pembayaran berhasil dihapus."}
    else:
        raise HTTPException(status_code=404, detail="Data pembayaran tidak ditemukan.")

def combine_asuransi_tour_guide():
    data_asuransi = get_asuransi()
    data_tourGuide = get_tourGuide()

    combined_data = []
    for asuransi in data_asuransi:
        for tour_guide in data_tourGuide:
            combined_obj = {
                "id_asuransi": asuransi['id_asuransi'],
                "jenis_asuransi": asuransi['jenis_asuransi'],
                "premi": asuransi['premi'],
                "keterangan": asuransi['keterangan'],
                "tanggal_mulai_asuransi" : asuransi['tanggal_mulai_asuransi'],
                "tanggal_selesai_asuransi" : asuransi['tanggal_selesai_asuransi'],
                "tourguide":tour_guide
            }
            combined_data.append(combined_obj)

    return combined_data

class asuransiTourGuide(BaseModel):
    id_asuransi: str
    jenis_asuransi: str
    premi: str
    keterangan: str
    tanggal_mulai_asuransi : str
    tanggal_selesai_asuransi : str
    tourguide:TourGuide

@app.get("/asuransitourguide", response_model=List[asuransiTourGuide])
def get_combined_data():
    combined_data = combine_asuransi_tour_guide()
    return combined_data

def combine_asuransi_hotel():
    data_asuransi = get_asuransi()
    data_hotel = get_hotel()

    combined_data = []
    for asuransi in data_asuransi:
        for hotel in data_hotel:
            combined_obj = {
                "id_asuransi": asuransi['id_asuransi'],
                "jenis_asuransi": asuransi['jenis_asuransi'],
                "premi": asuransi['premi'],
                "keterangan": asuransi['keterangan'],
                "hotel": hotel
            }
            combined_data.append(combined_obj)

    return combined_data

class AsuransiHotel(BaseModel):
    id_asuransi: str
    jenis_asuransi: str
    premi: str
    keterangan: str
    hotel : Hotel

@app.get("/asuransiHotel", response_model=List[AsuransiHotel])
def get_combined_data():
    combined_data = combine_asuransi_hotel()
    return combined_data

'''
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

class AsuransiBank(BaseModel):
    id_wisata: str
    nama_objek: str
    bank: Bank

@app.get("/asuransiBank", response_model=List[AsuransiBank])
def get_combined_data():
    combined_data = combine_wisata_bank()
    return combined_data
'''