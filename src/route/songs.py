from src.app import app, auth
from src.model.song import Song
from src.model.user import User, Role
from flask_restful import reqparse
from src.error_handler.exception_wrapper import handle_error_format
from src.error_handler.exception_wrapper import handle_server_exception


@app.route('/song/create', methods=['POST'])
@auth.login_required(role='admin')
@handle_server_exception
def create_song():
    parser = reqparse.RequestParser()

    parser.add_argument('name', help='name cannot be blank', required=True)
    parser.add_argument('artist', help='artist cannot be blank', required=True)

    data = parser.parse_args()
    name = data['name']
    artist = data['artist']

    check = Song.get_by_name(name)
    if check and check.artist == artist:
        return handle_error_format('Such song already exists.',
                                   'Field \'name\' in the request body.'), 400

    song = Song(
        name=name,
        artist=artist
    )

    try:
        song.save_to_db()

        return {'message': 'Song was successfully created'}, 200
    except:
        return {'message': 'Something went wrong'}, 500


@app.route('/song/<songId>', methods=['GET'])
@auth.login_required(role='admin')
@handle_server_exception
def get_song_by_id(songId: int):
    song = Song.get_by_id(songId)
    if not song:
        return handle_error_format('Song with such id does not exist.',
                                   'Field \'songId\' in path parameters.'), 404
    return Song.to_json(song)


# @app.route('/song/name/<name>', methods=['GET'])
# @handle_server_exception
# def get_song_by_name(name: str):
#     song = Song.get_by_name(name)
#     if not song:
#         return handle_error_format('There are no songs with such name.',
#                                    'Field \'name\' in path parameters.'), 404
#     return Song.to_json(song)


@app.route('/song/<songId>', methods=['PUT'])
@auth.login_required(role='admin')
@handle_server_exception
def update_song_by_id(songId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('name', help='name cannot be blank', required=True)
    parser.add_argument('artist', help='artist cannot be blank', required=True)

    data = parser.parse_args()
    name = data['name']
    artist = data['artist']

    song = Song.get_by_id(songId)

    if not song:
        return handle_error_format('Song with such id does not exist.',
                                   'Field \'SongId\' in path parameters.'), 404

    check = Song.get_by_name(name)
    if check and check.artist == artist:
        return handle_error_format('Such song already exists.',
                                   'Field \'name\' in the request body.'), 400

    song.name = name
    song.artist = artist
    song.save_to_db()

    return Song.to_json(song)


@app.route('/song/<songId>', methods=['DELETE'])
@auth.login_required(role='admin')
@handle_server_exception
def delete_song_by_id(songId: int):
    return Song.delete_by_id(songId)
