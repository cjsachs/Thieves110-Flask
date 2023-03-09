from flask import request
from . import api
from ...models import Post, User

# GET api routes

# view all posts in a JSON format
@api.route('/view_posts', methods=['GET'])
def view_posts_api():
    posts = Post.query.all()
    posts_json = []
    for post in posts:
        post_data = {
            'post_id': post.id,
            'img_url': post.img_url,
            'title': post.title,
            'caption': post.caption,
            'date_created': post.date_created,
            'author': f'{post.author.first_name} {post.author.last_name}'
        }
        posts_json.append(post_data)
    return {
        'status': 'ok',
        'data': posts_json
    }


# view a single post in JSON format
@api.route('/<int:post_id>', methods=['GET'])
def view_single_post_api(post_id):
    post = Post.query.get(post_id)
    if post:
        return {
            'status': 'ok',
            'data': {
                'post_id': post.id,
                'img_url': post.img_url,
                'title': post.title,
                'caption': post.caption,
                'date_created': post.date_created,
                'author': f'{post.author.first_name} {post.author.last_name}'
            }
        }
    else:
        return {
            'status': 'not ok',
            'message': 'post does not exist!'
        }
    
# POST api route

@api.route('/create', methods=['POST'])
def create_post_api():
    data = request.json # this is coming from POST request body
    
    # check if the user exists
    user = User.query.get(data["user_id"])
    if user:
        # unpack our JSON data
        new_post_data = {
            'img_url': data["img_url"],
            'title': data["title"],
            'caption': data["caption"],
            'user_id': data["user_id"]
        }

        # create an instance of post
        new_post = Post()

        # implementing values from new_post_data to our instance
        new_post.from_dict(new_post_data)

        # save post to db
        new_post.save_to_db()

        return {
            'status': 'ok',
            'message': 'Post was successfully created.'
        }
    else:
        return {
            'status': 'not ok',
            'message': 'That user does not exist.'
        }