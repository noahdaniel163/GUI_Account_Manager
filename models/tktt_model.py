from utils.db_handler import DatabaseHandler
from utils.logger import Logger
import json

logger = Logger('tktt_model')

class TKTTModel:
    def __init__(self):
        self.db_handler = DatabaseHandler()
        
    def get_total_records(self):
        """Lấy tổng số bản ghi"""
        query = "SELECT COUNT(*) FROM TKTT WHERE LoaiKhachHang = N'Ca Nhan'"
        result = self.db_handler.execute_query(query, fetchall=False)
        return result[0] if result else 0
        
    def get_records(self, offset, limit, search_conditions=None):
        """Lấy danh sách bản ghi có phân trang và tìm kiếm"""
        base_query = """
            SELECT 
                CAST(Cif AS VARCHAR(36)) AS Cif,
                CAST(Soid AS VARCHAR(15)) AS Soid,
                CAST(LoaiD AS INT) AS LoaiD,
                CAST(TenKhachHang AS NVARCHAR(150)) AS TenKhachHang,
                CONVERT(VARCHAR(10), NgaySinh, 103) AS NgaySinh,
                CAST(GioiTinh AS INT) AS GioiTinh,
                CAST(MaSoThue AS VARCHAR(50)) AS MaSoThue,
                CAST(SoDienThoaiDangKyDichVu AS VARCHAR(15)) AS SoDienThoaiDangKyDichVu,
                CAST(DiaChi AS NVARCHAR(300)) AS DiaChi,
                CAST(DiaChiKiemSoatTruyCap AS NVARCHAR(60)) AS DiaChiKiemSoatTruyCap,
                CAST(MaSoNhanDangThietBiDong AS VARCHAR(36)) AS MaSoNhanDangThietBiDong,
                CAST(SoTaiKhoan AS VARCHAR(50)) AS SoTaiKhoan,
                CAST(LoaiTaiKhoan AS INT) AS LoaiTaiKhoan,
                CAST(TrangThaiHoatDongTaiKhoan AS INT) AS TrangThaiHoatDongTaiKhoan,
                CONVERT(VARCHAR(10), NgayMoTaiKhoan, 103) AS NgayMoTaiKhoan,
                CAST(PhuongThucMoTaiKhoan AS INT) AS PhuongThucMoTaiKhoan,
                CONVERT(VARCHAR(10), NgayXacThucTaiQuay, 103) AS NgayXacThucTaiQuay,
                CAST(QuocTich AS NVARCHAR(36)) AS QuocTich,
                CAST(LoaiKhachHang AS NVARCHAR(50)) AS LoaiKhachHang,
                CAST(GhiChu AS NVARCHAR(500)) AS GhiChu,
                CONVERT(VARCHAR(10), UpdateDate, 103) AS UpdateDate,
                CAST(NghiNgo AS INT) AS NghiNgo
            FROM TKTT 
            WHERE LoaiKhachHang = N'Ca Nhan'
        """
        
        params = []
        where_clause = ""
        
        if search_conditions:
            conditions = []
            if search_conditions.get('cif_soid'):
                search_term = search_conditions['cif_soid']
                conditions.append("(CAST(Cif AS VARCHAR(36)) LIKE ? OR CAST(Soid AS VARCHAR(15)) LIKE ?)")
                params.extend([f"%{search_term}%", f"%{search_term}%"])
                
            if search_conditions.get('customer_name'):
                conditions.append("TenKhachHang LIKE ?")
                params.append(f"%{search_conditions['customer_name']}%")
                
            if conditions:
                where_clause = " AND " + " AND ".join(conditions)
        
        query = f"{base_query}{where_clause} ORDER BY UpdateDate DESC OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        params.extend([offset, limit])
        
        return self.db_handler.execute_query(query, params=params)
        
    def verify_data(self, selected_data):
        """Xác thực dữ liệu với database"""
        verified_data = []
        
        for record in selected_data:
            if "Cif" not in record or "SoTaiKhoan" not in record:
                continue
                
            query = """
                SELECT 
                    Cif, Soid, LoaiD, TenKhachHang,
                    CONVERT(VARCHAR(10), NgaySinh, 103) AS NgaySinh,
                    GioiTinh, MaSoThue, SoDienThoaiDangKyDichVu, DiaChi,
                    DiaChiKiemSoatTruyCap, MaSoNhanDangThietBiDong,
                    SoTaiKhoan, LoaiTaiKhoan, TrangThaiHoatDongTaiKhoan,
                    CONVERT(VARCHAR(10), NgayMoTaiKhoan, 103) AS NgayMoTaiKhoan,
                    PhuongThucMoTaiKhoan,
                    CONVERT(VARCHAR(10), NgayXacThucTaiQuay, 103) AS NgayXacThucTaiQuay,
                    QuocTich, LoaiKhachHang, GhiChu,
                    CONVERT(VARCHAR(10), UpdateDate, 103) AS UpdateDate,
                    NghiNgo
                FROM TKTT 
                WHERE Cif = ? AND SoTaiKhoan = ?
            """
            
            result = self.db_handler.execute_query(query, params=(record["Cif"], record["SoTaiKhoan"]), fetchall=False)
            
            if result:
                verified_record = {}
                columns = [column[0] for column in result.cursor_description]
                for i, value in enumerate(result):
                    if value is not None:
                        if columns[i] in ["LoaiD", "GioiTinh", "LoaiTaiKhoan", 
                                        "TrangThaiHoatDongTaiKhoan", "PhuongThucMoTaiKhoan", "NghiNgo"]:
                            verified_record[columns[i]] = int(value)
                        else:
                            verified_record[columns[i]] = str(value).strip()
                
                verified_data.append(verified_record)
        
        return verified_data