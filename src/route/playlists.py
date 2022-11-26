from src.app import app, auth
from src.model.user import User
from src.model.playlist import State, Playlist
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
