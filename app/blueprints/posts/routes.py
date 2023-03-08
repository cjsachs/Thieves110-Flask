from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import PostForm
from . import posts
from ...models import Post, User

# Create a Post
@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():

        # Grabbing our form data and storing into a dict
        new_post_data = {
            'img_url': form.img_url.data,
            'title': form.title.data.title(),
            'caption': form.caption.data,
            'user_id': current_user.id
        }

        # Create instance of Post
        new_post = Post()

        # Implementing values from our form data for our instance
        new_post.from_dict(new_post_data)

        # Save user to database
        new_post.save_to_db()

        flash('You have successfully made a post!', 'success')
        return redirect(url_for('posts.view_posts'))
    return render_template('create_post.html', form=form)

# View All Posts
@posts.route('/view_posts', methods=['GET'])
@login_required
def view_posts():
    posts = Post.query.all()
    return render_template('view_posts.html', posts=posts[::-1])


# Dynamic Routes

# view single post
@posts.route('/<int:post_id>', methods=['GET'])
@login_required
def view_single_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return render_template('view_single_post.html', post=post)
    else:
        flash('Post does not exist', 'danger')
        return redirect(url_for('posts.view_posts'))

# update your post
@posts.route('/update/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    form = PostForm()
    post = Post.query.get(post_id)
    if current_user.id == post.user_id:
        if request.method == 'POST' and form.validate_on_submit():

            # Grabbing our form data and storing into a dict
            new_post_data = {
                'img_url': form.img_url.data,
                'title': form.title.data.title(),
                'caption': form.caption.data,
                'user_id': current_user.id
            }

            # Implementing values from our form data for our instance
            post.from_dict(new_post_data)

            # Update post to database
            post.update_to_db()

            flash('You have successfully updated your post!', 'success')
            return redirect(url_for('posts.view_posts'))
    return render_template('update_post.html', form=form, post=post)

# Delete a post
@posts.route('/delete/<int:post_id>', methods=['GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if current_user.id == post.user_id:
        post.delete_post()
    else:
        flash('🐍 You do not have permission to delete another users post!', 'danger')
    return redirect(url_for('posts.view_posts'))


# follow route
@posts.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.follow_user(user)
        flash(f'Successfully followed {user.first_name}!', 'success')
    return redirect(url_for('main.home'))

# unfollow route
@posts.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.unfollow_user(user)
        flash(f'Successfully un-followed {user.first_name}!', 'warning')
    return redirect(url_for('main.home'))