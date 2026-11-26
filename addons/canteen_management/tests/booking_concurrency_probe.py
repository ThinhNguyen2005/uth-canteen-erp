"""Run via Odoo shell on a disposable uth_erp56_ database, after install."""

from concurrent.futures import ThreadPoolExecutor
from threading import Event
from time import monotonic, sleep

from odoo import SUPERUSER_ID, api
from odoo.exceptions import UserError
from psycopg2.errors import SerializationFailure


def run_race(registry, mode):
    with registry.cursor() as cursor:
        test_env = api.Environment(cursor, SUPERUSER_ID, {})
        product = test_env["product.product"].create({"name": f"ERP56 {mode} meal"})
        partners = test_env["res.partner"].create(
            [{"name": f"ERP56 {mode} partner {number}"} for number in range(5)]
        )
        slot = test_env["canteen.meal.slot"].create({
            "name": f"ERP56 {mode} contention",
            "product_id": product.id,
            "start_at": "2026-12-01 11:00:00",
            "end_at": "2026-12-01 12:00:00",
            "capacity": 10,
        })
        slot.action_open_slot()
        bookings = test_env["canteen.meal.booking"]
        for partner in partners[:3]:
            bookings.create_booking_safe(partner.id, slot.id, quantity=3)
        assert (slot.booked_count, slot.state) == (9, "open")
        slot_id = slot.id
        partner_ids = partners[3:].ids
        draft_ids = bookings.create([
            {"partner_id": partner_id, "slot_id": slot_id, "state": "draft"}
            for partner_id in partner_ids
        ]).ids if mode == "confirm" else []
        cursor.commit()

    winner_ready = Event()
    loser_ready = Event()
    release_winner = Event()
    pids = {}

    def reserve(worker_env, index):
        model = worker_env["canteen.meal.booking"]
        if mode == "create":
            model.create_booking_safe(partner_ids[index], slot_id, quantity=1)
        else:
            model.browse(draft_ids[index]).action_confirm_booking()

    def worker(index):
        retries = 0
        for attempt in range(2):
            with registry.cursor() as cursor:
                worker_env = api.Environment(cursor, SUPERUSER_ID, {})
                cursor.execute("SET LOCAL statement_timeout = '8s'")
                if not attempt:
                    cursor.execute("SELECT pg_backend_pid()")
                    pids[index] = cursor.fetchone()[0]
                if index == 1:
                    loser_ready.set()
                try:
                    reserve(worker_env, index)
                    if index == 0:
                        winner_ready.set()
                        if not release_winner.wait(6):
                            raise TimeoutError("Winner was never released")
                    cursor.commit()
                    return "committed", retries
                except SerializationFailure:
                    cursor.rollback()
                    if index == 0 or attempt:
                        raise
                    retries += 1
                except UserError:
                    cursor.rollback()
                    if index == 0:
                        raise
                    return "capacity rejected", retries
        raise AssertionError("Contention retry did not complete")

    with ThreadPoolExecutor(max_workers=2) as executor:
        winner = executor.submit(worker, 0)
        try:
            assert winner_ready.wait(6), "Winner did not reserve the slot"
            loser = executor.submit(worker, 1)
            assert loser_ready.wait(4), "Second transaction did not start"
            assert pids[0] != pids[1], pids
            with registry.cursor() as observer:
                deadline = monotonic() + 2
                while monotonic() < deadline:
                    observer.execute("SELECT pg_blocking_pids(%s)", (pids[1],))
                    if pids[0] in observer.fetchone()[0]:
                        break
                    sleep(0.025)
                else:
                    raise AssertionError("PostgreSQL did not observe concurrent lock contention")
        finally:
            release_winner.set()
        assert winner.result(timeout=10) == ("committed", 0)
        outcome, retries = loser.result(timeout=10)
        assert outcome == "capacity rejected", (outcome, retries)

    with registry.cursor() as cursor:
        verifier = api.Environment(cursor, SUPERUSER_ID, {})
        slot = verifier["canteen.meal.slot"].browse(slot_id)
        records = verifier["canteen.meal.booking"].search([("slot_id", "=", slot_id)])
        confirmed = records.filtered(lambda record: record.state == "confirmed")
        assert (slot.capacity, slot.booked_count, slot.state) == (10, 10, "full")
        assert len(confirmed) == 4 and sum(confirmed.mapped("quantity")) == 10
        assert confirmed.mapped("partner_id").ids.count(partner_ids[0]) == 1
        loser_records = records.filtered(lambda record: record.partner_id.id == partner_ids[1])
        assert loser_records.mapped("state") == (["draft"] if mode == "confirm" else [])
    print(f"PASS {mode}: two PostgreSQL backends, observed lock wait, one commit, "
          f"one rejection, serialization retries={retries}, count=10, state=full")


if not env.cr.dbname.startswith("uth_erp56_"):
    raise RuntimeError("Use a disposable uth_erp56_ database")
for scenario in ("create", "confirm"):
    run_race(env.registry, scenario)
