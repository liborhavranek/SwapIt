import pytest
import time
from colorama import Fore, init
from app import app
from extensions import db


init(autoreset=True)

def pytest_runtest_logreport(report):
    if report.when == 'call':
        if report.outcome == 'passed':
            print(Fore.GREEN + f"Test {report.nodeid} completed with outcome: PASS")
        elif report.outcome == 'failed':
            print(Fore.RED + f"Test {report.nodeid} completed with outcome: FAIL")
        elif report.outcome == 'skipped':
            print(Fore.YELLOW + f"Test {report.nodeid} completed with outcome: SKIPPED")
        time.sleep(0.1)



@pytest.fixture(scope='module')
def test_client():
    # Konfigurace aplikace pro testování
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        print("Using test database:", app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()  # Vytvoření tabulek v testovací databázi

        yield app.test_client()  # Vytvoření testovacího klienta

        db.drop_all()  # Vymazání tabulek po testech
        db.session.remove()


@pytest.fixture(scope='function')
def init_database(test_client):
    with test_client.application.app_context():
        print("Initializing database...")
        db.session.begin_nested()
        yield db
        db.session.rollback()
        print("Database rollback complete.")