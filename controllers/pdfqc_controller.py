from fastapi import APIRouter, Depends, HTTPException, status
from schemas.pdfqc_schema import PDFQCCreate, PDFQCRead
from services.pdfqc_service import PDFQCService
from typing import List

router = APIRouter(prefix="/pdf-qc", tags=["Pdf Quality Check"])


def get_pdfqc_service() -> PDFQCService:
    return PDFQCService()


@router.post("/", response_model=PDFQCRead, status_code=status.HTTP_201_CREATED)
async def create_pdfqc(
    pdfqc: PDFQCCreate,
    service: PDFQCService = Depends(get_pdfqc_service),
):
    return await service.create_pdf_qc(pdfqc)


@router.get("/{pdfqc_id}", response_model=PDFQCRead)
async def get_pdfqc(
    pdfqc_id: int,
    service: PDFQCService = Depends(get_pdfqc_service),
):
    pdfqc = await service.get_pdf_qc(pdfqc_id)
    if not pdfqc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="PDF QC not found"
        )
    return pdfqc


@router.get("/", response_model=List[PDFQCRead])
async def get_all_pdfqcs(
    service: PDFQCService = Depends(get_pdfqc_service),
):
    return await service.get_all_pdf_qc()

@router.delete("/{pdfqc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pdfqc(
    pdfqc_id: int,
    service: PDFQCService = Depends(get_pdfqc_service),
):
    deleted = await service.delete_pdf_qc(pdfqc_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="PDF QC not found"
        )
    return None

@router.get('/qcByFile/{file_id}',response_model=PDFQCRead)
async def get_qc_by_file(
    file_id: int,
    service: PDFQCService = Depends(get_pdfqc_service),
):
    return await service.get_qc_by_file(int(file_id))
    
