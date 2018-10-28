from flask import render_template, flash, redirect, request, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, RequestForm, SearchForm
from app.models import User, Post, Request
from werkzeug.urls import url_parse

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    requests = Request.query.all()
    search = SearchForm(request.form)
    search.origin.choices = sorted(app.config['LOCATIONS'], key=lambda x: x[1])
    search.destination.choices = sorted(app.config['LOCATIONS'], key=lambda x: x[1])

    if search.validate_on_submit():
        if search.destination.data == search.origin.data:
            flash("Origin and Destination cannot be the same")
        else:
            return redirect(url_for('search_results', origin=search.origin.data,
            destination=search.destination.data, date=search.date.data))


    if current_user.is_authenticated:
        return render_template('index.html', user=current_user, requests=requests, form=search)

    else:
        return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        # Using .first() so that now user references a real User object,
        # as opposed to a stored query. We cannot access a User Object attribute
        # (password) from a Query Object
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods = ['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username = form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')

        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)



# username is dynamically determined. In url_for calls, also
# needs to set the username argument.
# etc: url_for('user', username=current_user.username).
@app.route('/user/<username>')
@login_required
def user(username):
    user    = User.query.filter_by(username=username).first_or_404()
    posts   = user.posts.order_by(Post.timestamp.desc()).all()

    return render_template('user.html', user=user, posts=posts)



@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)

        db.session.add(post)
        db.session.commit()

        flash('Your post is now live!')

        return redirect(url_for('chat'))

    posts = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template("chat.html", title='Home Page', form=form,
                           posts=posts)



# Very basic links to look at and clear databases
@app.route('/showdb')
def showdb():
    out = ""
    for u in User.query.all():
        out += str(u.id) +" -- "+ u.username +" -- "+ u.email +"<br/>"

    out += "<br/>"

    for r in Request.query.all():
        out += r.author.username +" is going from "+ r.origin +" to "+ r.destination +" on "
        out += str(r.date) + " at " + str(r.time) + " because \"" + r.description + "\"<br/>"

    return out



@app.route('/cleardb')
def cleardb():
    for u in User.query.all():
        db.session.delete(u)

    db.session.commit()         # commits changes; to be used if editing database

    return "database cleared"



@app.route('/request_form', methods=['GET', 'POST'])
@login_required
def request_form():
    form = RequestForm()
    form.origin_city.choices        = app.config['CITIES']
    form.origin.choices             = app.config['LOCATIONS']
    form.destination_city.choices   = app.config['CITIES']
    form.destination.choices        = app.config['LOCATIONS']

    if form.validate_on_submit():
        request = Request(
            origin_city       = form.origin_city.data,
            origin            = form.origin.data,
            destination_city  = form.destination_city.data,
            destination       = form.destination.data,
            date              = form.date.data,
            time              = form.time.data,
            author            = current_user,
            description       = form.description.data
        )

        if form.destination.data == form.origin.data:
            flash("Origin and Destination cannot be the same")
        else:
            db.session.add(request)
            db.session.commit()
            flash('Your request has been posted!')
            # return redirect(url_for('index'))
    return render_template('requestForm.html', title='Request', form=form)



@app.route('/get_origin_locations')
def _get_origin_locations():
    # Get available locations to display in SelectField after User
    # has selected the city SelectField.
    # For JavaScript request.
    city        = request.args.get('origin_city', "Richmond", type=str)
    locations   = app.config['LOCATIONS_BY_CITY'].get(city)

    return jsonify(locations)



@app.route('/get_destination_locations')
def _get_destination_locations():
    # Get available locations to display in SelectField after User
    # has selected the city SelectField.
    # For JavaScript request.
    city = request.args.get('destination_city', "Washington D.C.", type=str)
    locations = app.config['LOCATIONS_BY_CITY'].get(city)

    return jsonify(locations)

@app.route('/search_results')
def search_results():
    origin_requested = request.args.get('origin')
    destination_requested = request.args.get('destination')
    date_requested = request.args.get('date')
    results = Request.query.filter_by(origin = origin_requested,
                                      destination = destination_requested,
                                      date = date_requested).all()
    return render_template('results.html', results = results)

