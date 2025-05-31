from app.db.session import engine
from app.db.models.user import Base

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
