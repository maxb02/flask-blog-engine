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
    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if search:
        posts = Post.query.filter(Post.title.contains(search) | Post.body.contains(search))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=3)

    return render_template('posts/posts_list.html', posts=posts, pages=pages)


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


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
def post_edit(slug):
    post = Post.query.filter(Post.slug == slug).first()
    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_detail', slug=post.slug))
    else:
        form = PostForm(obj=post)
        return render_template('posts/post_edit.html', post=post, form=form)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    return render_template('posts/post_detail.html', post=post)


@posts.route('/tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts = tag.posts
    return render_template('posts/tag_detail.html', posts=posts, tag=tag)
