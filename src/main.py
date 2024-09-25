from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from database import get_async_session
from notes.schemas import *
from sqlalchemy import insert, select
from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime

from notes.models import notes_table

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/add_note")
async def add_note(note: Note, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(notes_table).values(
        user_id=note.user_id, note_id=note.note_id, note_title=note.note_title, note_text=note.note_text,
        crated_at=datetime.utcnow(), updated_at=datetime.utcnow()
    )

    try:
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "data": f"Added {note.note_title} for user {note.user_id}", "details": None}
    except IntegrityError as ex:
        raise HTTPException(status_code=410, detail={
            "status": "error",
            "data": None,
            "details": "Not unique note title for this user"
        })


@app.post("/get_note")  # по-хорошему переделать на get, но при этом не безопасно так передавать user_id
async def get_note(user_id: int, note_title: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(notes_table).where(notes_table.c.user_id == user_id and notes_table.c.note_title == note_title)
        result = await session.execute(query)
        result = result.mappings().all()[0]
        data = {
            "note_title": result["note_title"],
            "note_text": result["note_text"]
        }
        return {
            "status": "200",
            "data": data,
            "details": None
        }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
