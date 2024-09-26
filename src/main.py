from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from database import get_async_session
from notes.schemas import *
from sqlalchemy import insert, select, update, values
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
    except IntegrityError:
        raise HTTPException(status_code=410, detail={
            "status": "error",
            "data": None,
            "details": "Not unique note title for this user"
        })


@app.post("/get_note")  # по-хорошему переделать на get, но при этом не безопасно так передавать user_id
async def get_note(user_id: int, note_title: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(notes_table.c.note_title, notes_table.c.note_text).where(
            notes_table.c.user_id == user_id and notes_table.c.note_title == note_title)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@app.post("/get_all")
async def get_all(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(notes_table.c.note_title, notes_table.c.note_text).where(notes_table.c.user_id == user_id)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@app.patch("/change_note")
async def change_note(user_id: int, note_title: str, note_text: str, new_title: str = None,
                      session: AsyncSession = Depends(get_async_session)):
    query = ""
    try:
        if note_title:
            query = (
                update(notes_table).where(notes_table.c.user_id == user_id and notes_table.c.note_title == note_title)
                .values(note_title=new_title, note_text=note_text, updated_at=datetime.utcnow()))
        else:
            query = (
                update(notes_table).where(notes_table.c.user_id == user_id and notes_table.c.note_title == note_title)
                .values(note_text=note_text, updated_at=datetime.utcnow()))
        await session.execute(query)
        await session.commit()
        return {"status": "success", "data": f"Changed", "details": None}
    except IntegrityError:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Not unique note title for this user"
        })
