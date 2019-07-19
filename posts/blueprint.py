from flask import Blueprint, request
from flask import render_template
from flask import redirect
from flask import url_for

from models import Post, Tag
from .forms import PostForm
from app import db

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def posts_list():
    search = request.args.get('search')

    if search:
        posts = Post.query.filter(Post.title.contains(search) | Post.body.contains(search)).all()
    else:
        posts = Post.query.order_by(Post.created.desc())
    return render_template('posts/posts_list.html', posts=posts)


@posts.route('/create', methods=['POST', 'GET', ])
def post_create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('posts.posts_list'))
    else:
        form = PostForm()
        return render_template('posts/post_create.html', form=form)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post=post)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts = tag.posts
    return render_template('posts/tag_detail.html', posts=posts, tag=tag)

