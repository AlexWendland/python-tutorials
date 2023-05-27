from sqlalchemy import create_engine, MetaData, Table

engine = create_engine("sqlite:///./books.db", echo=True, future=True)

conn = engine.connect()

metadata = MetaData()

authors = Table("author", metadata, autoload_with=engine)
