from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Step 1: Setting up the Database
# Create the database and the "films" table
engine = create_engine('sqlite:///films_db.db')  # SQLite database
Base = declarative_base()


class Film(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    director = Column(String)
    release_year = Column(Integer)


# Create the table in the database
Base.metadata.create_all(engine)

# Step 2: Manipulating the Database
# Add films to the table
Session = sessionmaker(bind=engine)
session = Session()

# Add 3 films to the table
film1 = Film(title="Film 1", director="Director 1", release_year=2000)
film2 = Film(title="Film 2", director="Director 2", release_year=2010)
film3 = Film(title="Film 3", director="Director 3", release_year=2020)

session.add_all([film1, film2, film3])
session.commit()

# Update a film (for example, updating the release year of Film 1)
film_to_update = session.query(Film).filter_by(title="Film 1").first()
if film_to_update:
    film_to_update.release_year = 2001
    session.commit()

# Print data from the table
films = session.query(Film).all()
for film in films:
    print(f"Title: {film.title}, Director: {film.director}, Release Year: {film.release_year}")

# Delete all data from the table
session.query(Film).delete()
session.commit()

# Close the session
session.close()
