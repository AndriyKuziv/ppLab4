from src.app import app, auth
from src.model.user import User
from src.model.song import Song
from src.model.playlist import State, Playlist
from src.model.playlist_song import PlaylistSong
from flask_restful import reqparse
from src.error_handler.exception_wrapper import handle_error_format
from src.error_handler.exception_wrapper import handle_server_exception


@app.route('/playlist/<userId>', methods=['POST'])
@auth.login_required(role=['user', 'admin'])
@handle_server_exception
def create_playlist(userId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('name', help='name cannot be blank', required=True)
    parser.add_argument('state', help='state cannot be blank', default=State.PUBLIC)

    data = parser.parse_args()
    name = data['name']
    state = State(data['state'])

    user = User.get_by_id(userId)

    if not user:
        return handle_error_format('User with such id does not exist.',
                                   'Field \'userId\' in path parameters.'), 400

    playlist = Playlist(
        name=name,
        userId=userId,
        state=state
    )

    try:
        playlist.save_to_db()

        return {'message': 'Playlist was successfully created'}, 200
    except:
        return {'message': 'Something went wrong'}, 500


@app.route('/playlist/<playlistId>', methods=['DELETE'])
@auth.login_required(role=['user', 'admin'])
@handle_server_exception
def delete_playlist_by_id(playlistId: int):
    return Playlist.delete_by_id(playlistId)


@app.route('/playlist/<playlistId>', methods=['GET'])
@auth.login_required(role=['user', 'admin'])
@handle_server_exception
def get_playlist_by_id(playlistId: int):
    playlist = Playlist.get_by_id(playlistId)

    if not playlist:
        return handle_error_format('Playlist with such id does not exist.',
                                   'Field \'playlistId\' in path parameters.'), 404

    return Playlist.to_json(playlist)


@app.route('/playlist/<playlistId>', methods=['PUT'])
@handle_server_exception
@auth.login_required(role=['user', 'admin'])
def update_playlist_by_id(playlistId: int):
    parser = reqparse.RequestParser()

    parser.add_argument('name', help='name cannot be blank', required=True)
    parser.add_argument('state', help='state cannot be blank', required=True)

    data = parser.parse_args()
    name = data['name']
    state = data['state']

    playlist = Playlist.get_by_id(playlistId)

    if not playlist:
        return handle_error_format('Playlist with such id does not exist.',
                                   'Field \'playlistId\' in path parameters.'), 404

    if Playlist.get_by_name(name) and not (name == playlist.name):
        return handle_error_format('Playlist with such name already exists.',
                                   'Field \'name\' in the request body.'), 400

    playlist.name = name
    playlist.state = state
    playlist.save_to_db()

    return Playlist.to_json(playlist)


@app.route('/playlist/<playlistId>/songs', methods=['GET'])
@handle_server_exception
def get_playlist_songs_by_id(playlistId: int):
    playlist = Playlist.get_by_id(playlistId)

    if not playlist:
        return handle_error_format('Playlist with such id does not exist.',
                                   'Field \'playlistId\' in path parameters.'), 404

    return PlaylistSong.return_all_by_playlist_id(playlistId)


@app.route('/playlist/<playlistId>/addSong', methods=['POST'])
@handle_server_exception
@auth.login_required(role=['user', 'admin'])
def add_song_to_playlist(playlistId: int):
    playlist = Playlist.get_by_id(playlistId)

    if not playlist:
        return handle_error_format('Playlist with such id does not exist.',
                                   'Field \'playlistId\' in path parameters.'), 404

    parser = reqparse.RequestParser()

    parser.add_argument('song_id', help='song_id cannot be blank', required=True)

    data = parser.parse_args()
    song_id = data['song_id']

    if not Song.get_by_id(song_id):
        return handle_error_format('Song with such id does not exist.',
                                   'Field \'songId\' in path parameters.'), 404

    playlist_song = PlaylistSong(
        playlist_id=playlistId,
        song_id=song_id
    )

    try:
        playlist_song.save_to_db()

        return {'message': 'Song was successfully added to playlist'}, 200
    except:
        return {'message': 'Something went wrong'}, 500


@app.route('/playlist/<playlistId>/remSong', methods=['DELETE'])
@handle_server_exception
@auth.login_required(role=['user', 'admin'])
def remove_song_from_playlist(playlistId: int):
    playlist = Playlist.get_by_id(playlistId)

    if not playlist:
        return handle_error_format('Playlist with such id does not exist.',
                                   'Field \'playlistId\' in path parameters.'), 404

    parser = reqparse.RequestParser()

    parser.add_argument('song_id', help='name cannot be blank', required=True)

    data = parser.parse_args()
    song_id = data['song_id']

    if not Song.get_by_id(song_id):
        return handle_error_format('Song with such id does not exist.',
                                   'Field \'songId\' in path parameters.'), 404

    return PlaylistSong.delete_by_song_id_and_playlist_id(song_id, playlistId)





