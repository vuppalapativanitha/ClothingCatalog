#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify
from flask import session as login_session
from flask import make_response

# importing SqlAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, ClothingDB, User
import random
import string
import httplib2
import json
import requests

# importing oauth

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials

# app configuration

app = Flask(__name__)
app.secret_key = 'itsasecret'

# google client secret
secret_file = json.loads(open('client_secret.json', 'r').read())
CLIENT_ID = secret_file['web']['client_id']
APPLICATION_NAME = 'Item-Catalog'

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

engine = create_engine('sqlite:///ClothingCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# validating current loggedin user


def check_user():
    email = login_session['email']
    return session.query(User).filter_by(email=email).one_or_none()


# retreive admin user details

def check_admin():
    return session.query(User).filter_by(
        email='vuppalapativanitha@gmail.com').one_or_none()


# Add new user into database

def createUser():
    name = login_session['name']
    email = login_session['email']
    url = login_session['img']
    provider = login_session['provider']
    newUser = User(name=name, email=email, image=url, provider=provider)
    session.add(newUser)
    session.commit()


def new_state():
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits) for x in range(32))
    login_session['state'] = state
    return state


def queryAllProducts():
    return session.query(ClothingDB).all()


# App Routes

# main page

@app.route('/')
@app.route('/clothing/')
def showProducts():
    clothing = queryAllProducts()
    state = new_state()
    return render_template('main.html', clothing=clothing, currentPage='main',
                           state=state, login_session=login_session)


# To add new product

@app.route('/clothing/new/', methods=['GET', 'POST'])
def newProduct():
    if request.method == 'POST':

        # check if user is logged in or not

        if 'provider' in login_session and \
                    login_session['provider'] != 'null':
            productName = request.form['productName']
            coverUrl = request.form['productImage']
            description = request.form['productDescription']
            description = description.replace('\n', '<br>')
            productCategory = request.form['category']
            user_id = check_user().id

            if productName and description \
                    and productCategory:
                newProduct = ClothingDB(
                    productName=productName,
                    coverUrl=coverUrl,
                    description=description,
                    category=productCategory,
                    user_id=user_id,
                    )
                session.add(newProduct)
                session.commit()
                return redirect(url_for('showProducts'))
            else:
                state = new_state()
                return render_template(
                    'newItem.html',
                    currentPage='new',
                    title='Add New Product',
                    errorMsg='All Fields are Required!',
                    state=state,
                    login_session=login_session,
                    )
        else:
            state = new_state()
            books = queryAllProducts()
            return render_template(
                'main.html',
                clothing=clothing,
                currentPage='main',
                state=state,
                login_session=login_session,
                errorMsg='Please Login first to Add Product!',
                )
    elif 'provider' in login_session and login_session['provider'] \
            != 'null':
        state = new_state()
        return render_template('newItem.html', currentPage='new',
                               title='Add New Product', state=state,
                               login_session=login_session)
    else:
        state = new_state()
        clothing = queryAllProducts()
        return render_template(
            'main.html',
            clothing=clothing,
            currentPage='main',
            state=state,
            login_session=login_session,
            errorMsg='Please Login first to Add Product!',
            )


# To show product of different category

@app.route('/clothing/category/<string:category>/')
def sortProducts(category):
    clothing = session.query(ClothingDB).filter_by(category=category).all()
    state = new_state()
    return render_template(
        'main.html',
        clothing=clothing,
        currentPage='main',
        error='Sorry! No Product in Database With this Category :(',
        state=state,
        login_session=login_session)


# To show product details

@app.route('/clothing/category/<string:category>/<int:productId>/')
def productDetail(category, productId):
    product = session.query(ClothingDB).filter_by(
            id=productId,
            category=category).first()
    state = new_state()
    if product:
        return render_template('itemDetail.html', product=product,
                               currentPage='detail', state=state,
                               login_session=login_session)
    else:
        return render_template('main.html', currentPage='main',
                               error="""No Product Found with this Category
                               and Product Id :(""",
                               state=state,
                               login_session=login_session)


# To edit product details

@app.route('/clothing/category/<string:category>/<int:productId>/edit/',
           methods=['GET', 'POST'])
def editProductDetails(category, productId):
    product = session.query(ClothingDB).filter_by(
            id=productId,
            category=category).first()
    if request.method == 'POST':

        # check if user is logged in or not

        if 'provider' in login_session and login_session['provider'] \
                != 'null':
            productName = request.form['productName']
            coverUrl = request.form['productImage']
            description = request.form['productDescription']
            productCategory = request.form['category']
            user_id = check_user().id
            admin_id = check_admin().id

            # check if book owner is same as logged in user or admin or not

            if book.user_id == user_id or user_id == admin_id:
                if productName and description \
                        and productCategory:
                    product.productName = productName
                    product.coverUrl = coverUrl
                    description = description.replace('\n', '<br>')
                    product.description = description
                    product.category = bookCategory
                    session.add(product)
                    session.commit()
                    return redirect(url_for('productDetail',
                                    category=product.category,
                                    productId=product.id))
                else:
                    state = new_state()
                    return render_template(
                        'editItem.html',
                        currentPage='edit',
                        title='Edit Product Details',
                        product=product,
                        state=state,
                        login_session=login_session,
                        errorMsg='All Fields are Required!',
                        )
            else:
                state = new_state()
                return render_template(
                    'itemDetail.html',
                    product=product,
                    currentPage='detail',
                    state=state,
                    login_session=login_session,
                    errorMsg='Sorry! The Owner can only edit product Details!')
        else:
            state = new_state()
            return render_template(
                'itemDetail.html',
                product=product,
                currentPage='detail',
                state=state,
                login_session=login_session,
                errorMsg='Please Login to Edit the Product Details!',
                )
    elif book:
        state = new_state()
        if 'provider' in login_session and login_session['provider'] \
                != 'null':
            user_id = check_user().id
            admin_id = check_admin().id
            if user_id == book.user_id or user_id == admin_id:
                product.description = product.description.replace('<br>', '\n')
                return render_template(
                    'editItem.html',
                    currentPage='edit',
                    title='Edit Product Details',
                    product=product,
                    state=state,
                    login_session=login_session,
                    )
            else:
                return render_template(
                    'itemDetail.html',
                    product=product,
                    currentPage='detail',
                    state=state,
                    login_session=login_session,
                    errorMsg='Sorry! The Owner can only edit product Details!')
        else:
            return render_template(
                'itemDetail.html',
                product=product,
                currentPage='detail',
                state=state,
                login_session=login_session,
                errorMsg='Please Login to Edit the Product Details!',
                )
    else:
        state = new_state()
        return render_template('main.html', currentPage='main',
                               error="""Error Editing Product! No Product Found
                               with this Category and Product Id :(""",
                               state=state,
                               login_session=login_session)


# To delete products

@app.route('/clothing/category/<string:category>/<int:productId>/delete/')
def deleteProduct(category, productId):
    product = session.query(ClothingDB).filter_by(
            category=category,
            id=productId).first()
    state = new_state()
    if product:

        # check if user is logged in or not

        if 'provider' in login_session and login_session['provider'] \
                != 'null':
            user_id = check_user().id
            admin_id = check_admin().id
            if user_id == product.user_id or user_id == admin_id:
                session.delete(product)
                session.commit()
                return redirect(url_for('showProducts'))
            else:
                return render_template(
                    'itemDetail.html',
                    product=product,
                    currentPage='detail',
                    state=state,
                    login_session=login_session,
                    errorMsg='Sorry! Only the Owner Can delete the Product'
                    )
        else:
            return render_template(
                'itemDetail.html',
                product=product,
                currentPage='detail',
                state=state,
                login_session=login_session,
                errorMsg='Please Login to Delete the Product!',
                )
    else:
        return render_template('main.html', currentPage='main',
                               error="""Error Deleting Product! No Product Found
                               with this Category and Product Id :(""",
                               state=state,
                               login_session=login_session)


# JSON Endpoints

@app.route('/clothing.json/')
def productsJSON():
    clothing = session.query(ClothingDB).all()
    return jsonify(Clothings=[product.serialize for product in clothing])


@app.route('/clothing/category/<string:category>.json/')
def productCategoryJSON(category):
    clothing = session.query(ClothingDB).filter_by(category=category).all()
    return jsonify(Clothings=[product.serialize for product in clothing])


@app.route('/clothing/category/<string:category>/<int:productId>.json/')
def productJSON(category, productId):
    product = session.query(ClothingDB).filter_by(
            category=category,
            id=productId).first()
    return jsonify(Clothing=product.serialize)


# google signin function

@app.route('/gconnect', methods=['POST'])
def gConnect():
    if request.args.get('state') != login_session['state']:
        response.make_response(json.dumps('Invalid State paramenter'),
                               401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data
    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets('client_secret.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps("""Failed to upgrade the
        authorisation code"""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    header = httplib2.Http()
    result = json.loads(header.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
                            """Token's user ID does not
                            match given user ID."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            """Token's client ID
            does not match app's."""),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'),
                          200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['credentials'] = access_token
    login_session['id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # ADD PROVIDER TO LOGIN SESSION

    login_session['name'] = data['name']
    login_session['img'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'
    if not check_user():
        createUser()
    return jsonify(name=login_session['name'],
                   email=login_session['email'],
                   img=login_session['img'])


# logout user

@app.route('/logout', methods=['post'])
def logout():

    # Disconnect based on provider

    if login_session.get('provider') == 'google':
        return gdisconnect()
    else:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['credentials']

    # Only disconnect a connected user.

    if access_token is None:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % access_token
    header = httplib2.Http()
    result = header.request(url, 'GET')[0]

    if result['status'] == '200':

        # Reset the user's session.

        del login_session['credentials']
        del login_session['id']
        del login_session['name']
        del login_session['email']
        del login_session['img']
        login_session['provider'] = 'null'
        response = make_response(json.dumps({'state': 'loggedOut'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        # if given token is invalid, unable to revoke token

        response = make_response(json.dumps({'state': 'errorRevoke'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == '__main__':
    app.debug = True
    app.run(host='', port=5000)
