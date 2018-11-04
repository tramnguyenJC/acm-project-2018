from flask import render_template, flash, redirect, request, url_for, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, RequestForm, SearchForm, EmailContentForm
from app.models import User, Request
from werkzeug.urls import url_parse
from app.email import send_request_email

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
    requests   = user.requests.all()

    return render_template('user.html', user=user, current_user = current_user, 
        requests = requests)


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



# sending email notification to user
@app.route('/email_notification', methods=['GET', 'POST'])
def email_notification():
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    form = EmailContentForm()
    if form.validate_on_submit():
        sender_name = form.name.data
        sender_contact1 = form.contact1.data
        sender_contact2 = form.contact2.data
        sender_message = form.message.data
        user = request.args.get('user')
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        date = request.args.get('date')
        recipient = User.query.filter_by(username=user).first()
        recipient_username = recipient.username
        recipient_email = recipient.email
        if sender_name and sender_contact1 and recipient_username and recipient_email and origin and destination and date:
            send_request_email(sender_name, sender_contact1, sender_contact2, sender_message,
                                recipient_username, recipient_email, origin, destination, date)
            flash('Request Sent!')
            return redirect(url_for('index'))
    # requests = Request.query.all()
    return render_template('email_content.html', form=form)


@app.route('/delete_request/<request_id>')
@login_required
def delete_request(request_id):
    request = Request.query.filter_by(id=request_id).first()
    db.session.delete(request)
    db.session.commit()
    flash('Request has been deleted.')
    return redirect(url_for('user', username=current_user.username))


@app.route('/edit_request/<request_id>', methods=['GET', 'POST'])
@login_required
def edit_request(request_id):
    old_request = Request.query.filter_by(id=request_id).first()
    form = RequestForm(
        origin_city = old_request.origin_city,
        origin = old_request.origin,
        destination_city = old_request.destination_city,
        destination = old_request.destination,
        date = old_request.date,
        time = old_request.time,
        description = old_request.description)
    form.origin_city.choices        = app.config['CITIES']
    form.origin.choices             = app.config['LOCATIONS']
    form.destination_city.choices   = app.config['CITIES']
    form.destination.choices        = app.config['LOCATIONS']

    if form.validate_on_submit():
        request = old_request
        request.origin_city       = form.origin_city.data
        request.origin            = form.origin.data
        request.destination_city  = form.destination_city.data
        request.destination       = form.destination.data
        request.date              = form.date.data
        request.time              = form.time.data
        request.description       = form.description.data

        if form.destination.data == form.origin.data:
            flash("Origin and Destination cannot be the same")
        else:
            db.session.add(request)
            db.session.commit()
            flash('Your request has been edited!')
            return redirect(url_for('user', username=current_user.username))
    return render_template('requestForm.html', title='Request', form=form)
