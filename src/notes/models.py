from datetime import datetime

from sqlalchemy import (Integer, String, TIMESTAMP, ForeignKey,
                        Table, Column, UniqueConstraint, MetaData, PrimaryKeyConstraint)

metadata = MetaData()

notes_table = Table(
    "notes",
    metadata,
    Column("user_id", Integer),
    Column("note_id", Integer),
    Column("note_title", String(length=30)),
    Column("note_text", String(length=500)),
    Column("crated_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow),
    PrimaryKeyConstraint("user_id", "note_title", name="unique_user_note"),
    # TODO переделать ограничение уникальности на первичный ключ, причем указать столбцы в правильном порядке
)
