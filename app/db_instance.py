from app import db

def save(data):
    try:
        print(data)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        raise e
