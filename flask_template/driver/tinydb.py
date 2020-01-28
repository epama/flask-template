from tinydb import TinyDB

def init_db(app):
    db_dir = app.config["DB_DIR"]

    db = TinyDB(db_dir)
    
    return db