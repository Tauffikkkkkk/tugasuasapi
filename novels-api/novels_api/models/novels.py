from uuid import uuid4

from .. import db 
from .api_keys import APIKey
    

class Novel(db.Model):
    __tablename__ = 'novels'

    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)
    deskripsi = db.Column(db.String)
    @property
    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'deskripsi' : self.deskripsi,
            }
    
    @classmethod
    def to_list(cls):
        novels = cls.query.all()
        return [
            novel.json for novel in novels
        ]
