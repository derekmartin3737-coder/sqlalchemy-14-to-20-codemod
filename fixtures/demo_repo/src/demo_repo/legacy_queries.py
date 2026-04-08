from sqlalchemy import Table, select, update
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.dml import Update

from demo_repo.models import User


def user_names(session: Session) -> list[str]:
    statement = select([User.name])
    return list(session.execute(statement).scalars())


def get_user(session: Session, user_id: int) -> User | None:
    return session.query(User).get(user_id)


def users_with_addresses(session: Session) -> list[User]:
    return list(
        session.query(User).options(joinedload("addresses")).join("addresses").all()
    )


def rename_user(user_table: Table, user_id: int, new_name: str) -> Update:
    return update(
        user_table,
        whereclause=user_table.c.id == user_id,
        values={"name": new_name},
    )
