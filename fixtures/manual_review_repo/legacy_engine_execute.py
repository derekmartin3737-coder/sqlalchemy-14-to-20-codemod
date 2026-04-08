from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload


def run_problematic_query(session, User):
    engine = create_engine("sqlite+pysqlite:///:memory:")
    engine.execute("select 1")
    return (
        session.query(User)
        .options(joinedload("orders.items"))
        .join("orders", "items")
        .from_self()
        .all()
    )
