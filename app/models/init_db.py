from app.models.base import engine, Base
from app.models.contract import Contract
from app.models.ad_data import AdData
from app.models.violations import Violations

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
