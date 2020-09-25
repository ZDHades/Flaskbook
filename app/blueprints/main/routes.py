from .import bp as main
from app import db
from flask import current_app as app, render_template, request, redirect, url_for, flash, session
from app.models import User, Post
from flask_login import current_user, login_required

@main.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        posts = current_user.followed_posts().all()
    else:
        posts = []
    return render_template('index.html', posts=posts)


@main.route('/about')
@login_required
def about():
    return render_template('about.html')