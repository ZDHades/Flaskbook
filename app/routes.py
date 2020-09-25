from .import db
from flask import current_app as app, render_template, request, redirect, url_for, flash, session
from app.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse


@app.context_processor
def carty_b():
    if 'cart' not in session:
        session['cart'] = {
            "items": [],
            'cart_total': 0
        }
    return {'cart': session['cart']}
