from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import PostForm
from . import posts
from ...models import Post

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
    return render_template('view_posts.html', posts=posts)
