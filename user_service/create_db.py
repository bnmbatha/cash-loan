# Import the SQLAlchemy engine instance used to connect to the database
from app.db.session import engine

# Import the base class that holds metadata about all database models
from app.db.models.user import Base

# Log that the table creation process has started
print("Creating tables...")

# This line uses SQLAlchemy's metadata to create all tables defined under Base
# It checks the metadata and creates tables in the DB if they don't already exist
Base.metadata.create_all(bind=engine)

# Log that the process is finished
print("Done.")

