from app.models.base import engine, Base
from app.models.contract import Contract
from app.models.social_posts import SocialPosts

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
