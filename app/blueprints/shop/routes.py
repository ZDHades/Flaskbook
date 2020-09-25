from .import bp as shop
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from app.blueprints.shop.models import Product

import stripe, os


stripe_keys = {
    'secret_key': os.getenv('STRIPE_SECRET_KEY'),
    'publishable_key': os.getenv('STRIPE_PUBLISHABLE_KEY')
}

stripe.api_key = stripe_keys.get('secret_key')


@shop.route('/')
def get_products():
    if 'cart' not in session:
        session['cart'] = {
            "items": [],
            'cart_total': 0
        }
    content = {
        'products': Product.query.all()
    }
    return render_template('marketplace.html', **content)

@shop.route('/add')
def add_to_cart():
    _id = int(request.args.get('id'))
    p = Product.query.get(_id)
    item = {
        "id":p.id,
        "name": p.name,
        "price": p.price,
        "image": p.image,
        "in_stock": p.in_stock,
        "description": p.description
        }
    session['cart']['items'].append(item)
    session['cart']['cart_total'] = 0
    for _ in session['cart']['items']:
        session['cart']['cart_total'] += _['price']
    flash(f"{item['name']} has been added to your cart", 'success')
    return redirect(url_for('shop.get_products'))

@shop.route('/cart')
def cart():
    display_cart = []
    for _ in session['cart']['items']:
        if _ not in display_cart:
            display_cart.append(_)
    session['display_cart']= display_cart
    context = {
        'items' : display_cart,
        'cart_total': session['cart']['cart_total'],
        'stripe_publishable_key' : stripe_keys['publishable_key']
    }
    return render_template('cart.html', **context)
 
@shop.route('/remove')
def remove_from_cart():
    _id = int(request.args.get('id'))
    for _ in session['cart']['items']:
        if _id == _['id']:
            session['cart']['items'].remove(_)
            session['cart']['cart_total'] -= _['price']
            flash('The item has been removed from your cart', 'info')
            break
    return redirect(url_for('shop.cart'))

@shop.route('/clear')
def clear_cart():
    session['cart']['items'].clear()
    session['cart']['cart_total'] = 0
    flash("All items have been removed from your cart")
    return redirect(url_for('shop.cart'))

@shop.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    stripe_line_items = []
    for _ in session['display_cart']:
        product_dict = {
            'price_data': {
                'currency' : 'usd',
                'product_data' : {
                    'name': _['name'],
                    'description' : _['description'],
                    'images' : [_['image']]
                },
                'unit_amount' : int(_['price']*100),
            },
            'quantity' : session['cart']['items'].count(_),
        }
        stripe_line_items.append(product_dict)
    stripe_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=stripe_line_items,
        mode='payment',
        success_url='http://localhost:5000/shop/checkout/success',
        cancel_url='http://localhost:5000/shop/checkout/cancel'
    )

    session['stripe_session_information'] = stripe_session
    
    session['cart']['items'].clear()
    session['cart']['cart_total'] = 0
    
    return stripe_session

@shop.route('/checkout/success')
def checkout_success():
    return render_template('checkout-success.html', stripe_session=session['stripe_session_information'])

@shop.route('/checkout/cancel')
def checkout_cancel():
    return redirect(url_for('shop.cart'))