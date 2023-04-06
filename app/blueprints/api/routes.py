from flask import request,  g
from . import api
from ...models import Post, User
from .auth import basic_auth, token_auth

@api.get('/token')
@basic_auth.login_required()
def get_token():
    token = g.current_user.get_token()
    return {'token': token}


# CRUD - Create, Read, Update, Delete

# GET (Read) api routes
# view all posts in a JSON format
@api.get('/view_posts')
@token_auth.login_required()
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
@api.get('/<int:post_id>')
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
    


# POST (Create) api route
@api.post('/create')
def create_post_api():
    data = request.get_json() # this is coming from POST request body
    
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



# PUT (Update) api route
@api.put('/update/<int:post_id>')
def update_post_api(post_id):
    data = request.get_json()

    # Query the post and user objects
    post = Post.query.get(post_id)
    user = User.query.get(data["user_id"])

    if user and post:
        # check if the user is the owner of the post
        if user.id == post.user_id:
            # unpack our JSON data
            new_post_data = {
                'img_url': data["img_url"],
                'title': data["title"],
                'caption': data["caption"],
                'user_id': data["user_id"]
            }

            # updating values for our post object from new_post_data
            post.from_dict(new_post_data)

            # save post to db
            post.update_to_db()

            return {
                'status': 'ok',
                'message': 'Post was successfully updated.'
            }
        else:
            return {
                'status': 'not ok',
                'message': '🐍 That user does not have permission to update another users post!'
            }
    else:
        return {
            'status': 'not ok',
            'message': 'User or/and Post does not exist.'
        }

# DELETE a Post
@api.delete('/delete/<int:post_id>/<int:user_id>')
def delete_post(post_id, user_id):

    # query the post and user objects
    post = Post.query.get(post_id)
    user = User.query.get(user_id)
    
    if post and user:
        if user.id == post.user_id:
            post.delete_post()
            return {
                'status': 'ok',
                'message': 'Post deleted.'
            }
        else:
            return {
                'status': 'not ok',
                'message': '🐍 That user does not have permission to delete another users post!'
            }
    else:
        return {
            'status': 'not ok',
            'message': 'User or/and Post does not exist.'
        }
    

