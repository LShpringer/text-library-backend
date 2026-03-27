from fastapi import Security
from main import verify_api_key

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import TextItem
from schemas import TextCreate, TextUpdate, TextResponse

router = APIRouter(prefix="/texts", tags=["texts"])


@router.get("/", response_model=List[TextResponse])
def get_texts(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(TextItem)

    if search:
        query = query.filter(
            TextItem.title.contains(search) | TextItem.content.contains(search)
        )

    if category:
        query = query.filter(TextItem.category == category)

    if tag:
        query = query.filter(TextItem.tags.contains(tag))

    return query.order_by(TextItem.created_at.desc()).all()



@router.get("/{text_id}", response_model=TextResponse)
def get_text(text_id: int, db: Session = Depends(get_db)):
    text = db.query(TextItem).filter(TextItem.id == text_id).first()
    if not text:
        raise HTTPException(status_code=404, detail="Текст не найден")
    return text


@router.post("/", response_model=TextResponse)
def create_text(
    text: TextCreate,
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key),
):
    db_text = TextItem(**text.model_dump())
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text


@router.put("/{text_id}", response_model=TextResponse)
def update_text(
    text_id: int,
    text: TextUpdate,
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key),
):
    db_text = db.query(TextItem).filter(TextItem.id == text_id).first()
    if not db_text:
        raise HTTPException(status_code=404, detail="Текст не найден")
    for key, value in text.model_dump(exclude_unset=True).items():
        setattr(db_text, key, value)
    db.commit()
    db.refresh(db_text)
    return db_text


@router.delete("/{text_id}")
def delete_text(
    text_id: int,
    db: Session = Depends(get_db),
    api_key: str = Security(verify_api_key),
):
    db_text = db.query(TextItem).filter(TextItem.id == text_id).first()
    if not db_text:
        raise HTTPException(status_code=404, detail="Текст не найден")
    db.delete(db_text)
    db.commit()
    return {"message": "Удалено успешно"}
