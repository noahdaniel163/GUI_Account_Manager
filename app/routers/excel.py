from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from app.services import excel_service, simo_service
from schemas import simo_schemas
import os
import json
from typing import Dict, Any, List

router = APIRouter()

@router.post("/convert/{simo_code}")
async def convert_excel(
    simo_code: str,
    file: UploadFile = File(...),
    save_path: str = Form(None)
):
    """Chuyển đổi file Excel sang JSON"""
    try:
        # 1. Kiểm tra mã SIMO hợp lệ
        if simo_code not in ["001", "002", "003", "004", "011", "012"]:
            raise HTTPException(status_code=400, detail="Mã SIMO không hợp lệ")

        # 2. Lưu file tạm
        temp_file = f"temp_{simo_code}.xlsx"
        with open(temp_file, "wb") as f:
            f.write(await file.read())

        try:
            # 3. Đọc file Excel
            data = await excel_service.ExcelService.read_excel_to_dict(temp_file)
            
            # 4. Chuyển đổi dữ liệu
            converted_data = await excel_service.ExcelService.convert_to_simo_format(data, simo_code)
            
            # 5. Lưu file JSON nếu có yêu cầu
            if save_path:
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(converted_data, f, ensure_ascii=False, indent=2)
            
            # 6. Trả về kết quả
            return {
                "status": "success",
                "message": "Chuyển đổi thành công",
                "data": converted_data
            }
            
        finally:
            # Xóa file tạm
            if os.path.exists(temp_file):
                os.remove(temp_file)
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send/{simo_code}")
async def send_simo_data(
    simo_code: str,
    data: List[Dict[str, Any]] = Body(...)
):
    """Gửi dữ liệu SIMO"""
    try:
        # 1. Kiểm tra mã SIMO hợp lệ
        if simo_code not in ["001", "002", "003", "004", "011", "012"]:
            raise HTTPException(status_code=400, detail="Mã SIMO không hợp lệ")

        # 2. Kiểm tra và xử lý dữ liệu
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail="Dữ liệu phải là mảng JSON")

        # 3. Gửi dữ liệu
        result = await simo_service.SimoService.send_data(simo_code, data)
        
        # 4. Trả về kết quả
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 