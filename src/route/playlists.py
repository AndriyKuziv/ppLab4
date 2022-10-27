from src.app import app
from src.model.user import User
from src.model.playlist import State, Playlist
from flask_restful import reqparse


@app.route('/playlists', methods=['POST'])
def create_article():
    parser = reqparse.RequestParser()

    parser.add_argument('title', help='title cannot be blank', required=True)
    parser.add_argument('text', help='text cannot be blank', required=True)
    parser.add_argument('userId', help='userId cannot be blank', required=True)
    parser.add_argument('state', help='state cannot be blank', default=State.PUBLIC)

    data = parser.parse_args()
    name = data['name']
    user_id = int(data['userId'])
    state = State(data['state'])

    playlist = Playlist(
        name=name,
        userId=user_id,
        state=state
    )

    user = User.find_by_id(user_id)

    try:
        playlist.save_to_db()
        user.articles.append(playlist)

        return {'message': 'Playlist was successfully created'}, 200
    except:
        return {'message': 'Something went wrong'}, 500
