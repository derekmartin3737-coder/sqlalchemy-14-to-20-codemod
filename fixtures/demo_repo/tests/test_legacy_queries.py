from __future__ import annotations

from demo_repo.legacy_queries import (
    get_user,
    rename_user,
    user_names,
    users_with_addresses,
)
from demo_repo.models import Address, Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def _seed(session: Session) -> None:
    ada = User(name="Ada")
    ada.addresses.append(Address(email="ada@example.com"))
    session.add(ada)
    session.commit()


def test_user_names_returns_seeded_value() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        _seed(session)
        assert user_names(session) == ["Ada"]


def test_get_user_returns_record() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        _seed(session)
        user = session.query(User).filter(User.name == "Ada").one()
        loaded = get_user(session, user.id)
        assert loaded is not None
        assert loaded.name == "Ada"


def test_users_with_addresses_returns_joined_rows() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        _seed(session)
        result = users_with_addresses(session)
        assert len(result) == 1
        assert result[0].addresses[0].email == "ada@example.com"


def test_rename_user_statement_executes() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        _seed(session)
        statement = rename_user(User.__table__, 1, "Grace")
        session.execute(statement)
        session.commit()

        refreshed = session.query(User).filter(User.id == 1).one()
        assert refreshed.name == "Grace"
