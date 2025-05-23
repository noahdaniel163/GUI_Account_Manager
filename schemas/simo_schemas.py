from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    created_at: datetime

class SimoRequest(BaseModel):
    service_type: str
    payload: List[dict]

class SimoResponse(BaseModel):
    status: str
    message: str
    data: Optional[dict] = None

# Các model cho từng loại SIMO
class Simo001Record(BaseModel):
    Cif: str = Field(..., max_length=36)
    SoID: str = Field(..., max_length=15)
    LoaiID: int
    TenKhachHang: str = Field(..., max_length=150)
    NgaySinh: str = Field(..., max_length=10)
    GioiTinh: int
    MaSoThue: str
    SoDienThoaiDangKyDichVu: str = Field(..., max_length=15)
    DiaChi: str = Field(..., max_length=300)
    DiaChiKiemSoatTruyCap: str = Field(..., max_length=60)
    MaSoNhanDangThietBiDiDong: str = Field(..., max_length=36)
    SoTaiKhoan: str
    LoaiTaiKhoan: int
    TrangThaiHoatDongTaiKhoan: int
    NgayMoTaiKhoan: str = Field(..., max_length=10)
    PhuongThucMoTaiKhoan: int
    NgayXacThucTaiQuay: str = Field(..., max_length=10)
    QuocTich: str = Field(..., max_length=36)

class Simo002Record(BaseModel):
    Cif: str = Field(..., max_length=36)
    SoTaiKhoan: str
    TenKhachHang: str = Field(..., max_length=150)
    TrangThaiHoatDongTaiKhoan: int
    NghiNgo: int
    GhiChu: str = Field(..., max_length=500)

class Simo003Record(BaseModel):
    Cif: str = Field(..., max_length=36)
    SoTaiKhoan: str
    TenKhachHang: str = Field(..., max_length=150)
    TrangThaiHoatDongTaiKhoan: int
    NghiNgo: int
    GhiChu: str = Field(..., max_length=500)

class Simo004Record(BaseModel):
    Cif: str = Field(..., max_length=36)
    SoID: str = Field(..., max_length=15)
    LoaiID: int
    TenKhachHang: str = Field(..., max_length=150)
    NgaySinh: str = Field(..., max_length=10)
    GioiTinh: int
    MaSoThue: str
    SoDienThoaiDangKyDichVu: str = Field(..., max_length=15)
    DiaChi: str = Field(..., max_length=300)
    DiaChiKiemSoatTruyCap: str = Field(..., max_length=60)
    MaSoNhanDangThietBiDiDong: str = Field(..., max_length=36)
    SoTaiKhoan: str
    LoaiTaiKhoan: int
    TrangThaiHoatDongTaiKhoan: int
    NgayMoTaiKhoan: str = Field(..., max_length=10)
    PhuongThucMoTaiKhoan: int
    NgayXacThucTaiQuay: str = Field(..., max_length=10)
    GhiChu: str = Field(..., max_length=500)
    QuocTich: str = Field(..., max_length=36)

class Simo011Record(BaseModel):
    Cif: str = Field(..., max_length=36)
    SoID: str = Field(..., max_length=15)
    LoaiID: int
    TenKhachHang: str = Field(..., max_length=150)
    NgaySinh: str = Field(..., max_length=10)
    GioiTinh: int
    MaSoThue: str
    SoDienThoaiDangKyDichVu: str = Field(..., max_length=15)
    DiaChi: str = Field(..., max_length=300)
    DiaChiKiemSoatTruyCap: str = Field(..., max_length=60)
    MaSoNhanDangThietBiDiDong: str = Field(..., max_length=36)
    SoTaiKhoan: str
    LoaiTaiKhoan: int
    TrangThaiHoatDongTaiKhoan: int
    NgayMoTaiKhoan: str = Field(..., max_length=10)
    PhuongThucMoTaiKhoan: int
    NgayXacThucTaiQuay: str = Field(..., max_length=10)
    QuocTich: str = Field(..., max_length=36)

class Simo012Record(BaseModel):
    Cif: str = Field(..., max_length=36)
    SoTaiKhoan: str
    TenKhachHang: str = Field(..., max_length=150)
    TrangThaiHoatDongTaiKhoan: int
    NghiNgo: int
    GhiChu: str = Field(..., max_length=500) 