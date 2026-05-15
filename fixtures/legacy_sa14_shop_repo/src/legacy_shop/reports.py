from __future__ import annotations

from sqlalchemy import Table, delete, insert, select, update
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.dml import Delete, Insert, Update

from legacy_shop.models import Customer, Invoice


def get_customer(session: Session, customer_id: int) -> Customer | None:
    return session.query(Customer).get(customer_id)


def customer_invoice_rows(session: Session) -> list[tuple[str, int]]:
    statement = (
        select([Customer.email, Invoice.total_cents])
        .select_from(Customer)
        .join(Invoice)
        .where(Invoice.status == "paid")
    )
    return [(email, total) for email, total in session.execute(statement)]


def paid_customers_with_invoices(session: Session) -> list[Customer]:
    return list(
        session.query(Customer)
        .options(joinedload("invoices"))
        .join("invoices")
        .filter(Invoice.status == "paid")
        .all()
    )


def create_invoice_statement(
    invoice_table: Table,
    customer_id: int,
    total_cents: int,
) -> Insert:
    return insert(
        invoice_table,
        values={
            "customer_id": customer_id,
            "status": "draft",
            "total_cents": total_cents,
        },
    )


def mark_invoice_paid_statement(invoice_table: Table, invoice_id: int) -> Update:
    return update(
        invoice_table,
        whereclause=invoice_table.c.id == invoice_id,
        values={"status": "paid"},
    )


def delete_invoice_statement(invoice_table: Table, invoice_id: int) -> Delete:
    return delete(invoice_table, whereclause=invoice_table.c.id == invoice_id)
