from datetime import datetime
from flask import Blueprint, request
from .. import db

from ..models.novels import *

from ..models.novels import Novel

from ..middlewares.authentications import login_required, admin_only

from .. utils import errors
from uuid import uuid4

mod_novel = Blueprint('mod_novel', __name__, url_prefix='/api/novels')

@mod_novel.route('', methods=['GET'])
@login_required
def get_novel():
    novels = Novel.to_list()
    return {
        'error': None,
        'data': novels
    }

@mod_novel.route('/<id>', methods=['GET'])
@login_required
def get_novel_byid(id):
    novel = Novel.query.get(id)
    if novel is None:
        return errors.novel_not_found, 404
    return novel.json, 200

@mod_novel.route('', methods=['POST'])
@login_required
@admin_only
def create_novel():
    id = str(uuid4())
    title = request.json.get('title')
    deskripsi = request.json.get('deskripsi')
    release_date_str = request.json.get('release_date')
    release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()



    if not all([id, title, release_date, deskripsi]):
        return errors.bad_request_form, 400
    
    is_novel_exist = Novel.query.filter_by(title=title).first()

    if is_novel_exist:
        return errors.novel_exists, 200   
    
    new_novel = Novel(id=id, title=title, release_date=release_date, deskripsi=deskripsi)
    db.session.add(new_novel)
    db.session.commit()

    return {
        'error': None,
        'data': new_novel.json
    }, 201

@mod_novel.route('/<id>', methods=['PUT'])
@login_required
@admin_only
def update_novel(id):
    novel_id = Novel.query.get(id)
    title = request.json.get('title')
    release_date = request.json.get('release_date')
    deskripsi = request.json.get('deskripsi')

    if not novel_id:
        return errors.novel_not_found, 404
    if not all([novel_id, title, release_date, deskripsi]):
        return errors.bad_request_form, 400
    
    novel_id.title = title
    novel_id.release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
    novel_id.deskripsi = deskripsi
    db.session.commit()
    
    db.session.commit()
    return {
        'error': None,
        'data': novel_id.json
    }, 200

@mod_novel.route('/<id>', methods=['DELETE'])
@login_required
@admin_only
def delete_novel(id):
    novel = Novel.query.get(id)
    if novel is None:
        return errors.novel_not_found, 404
    db.session.delete(novel)
    db.session.commit()

    return {
        'error': None,
        'data': {
            'id': id
        }
    }, 200
