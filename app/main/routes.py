from datetime import date
from flask import render_template, request, redirect, url_for, flash, abort
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from app.extensions import db, bcrypt
from app.main import main
from app.main.models import Inventory, User


@main.route('/', methods=['GET'])
@login_required # require user to be logged in to access this route
def home():
    inventory_list = Inventory.query.all()

    return render_template('home.html', inventory = inventory_list)

@main.route('/my_items')
@login_required
def my_items():
    user_items = Inventory.query.filter_by(user_id=current_user.user_id).all() # fetch items belonging to the logged-in user
    return render_template('home.html', inventory=user_items)


@main.route('/book_release_item/<int:item_id>', methods=['POST'])
@login_required
def book_release_item(item_id):
    item = Inventory.query.get_or_404(item_id) # fetch the item by its ID, or return 404 if not found

    # check if the item is free (OK status and Free booked state)
    if item.booked == 'Free' and item.status == 'OK':
        # book the item for the current user
        item.user_id = current_user.user_id
        item.booked = 'In use'  # not free anymore
    elif item.user_id == current_user.user_id or current_user.user_name == 'admin':
        # release the item if it's booked by the current user or if the current user is an admin
        item.user_id = None
        item.booked = 'Free'  # make it free again
    else:
        # optional: Handle cases where the item is booked by another user
        flash('You cannot release this item. It is booked by another user.', 'error')
        return redirect(url_for('main.home'))

    try:
        db.session.commit()
        flash('Item status updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'error')

    return redirect(url_for('main.home'))

@main.route('/register_login', methods=['GET', 'POST'])
def register_login():
    if request.method == 'POST':
        form_type = request.form.get('form_type') # get the form type (register or login)

        if form_type == 'register':
            user_name = request.form.get('user_name')
            user_email = request.form.get('user_email')
            user_password = request.form.get('user_password')
            user_password_confirmed = request.form.get('user_password_confirmed')

            if user_password != user_password_confirmed:
                flash("Passwords do not match.", 'error')
            elif User.query.filter_by(user_name=user_name).first():
                flash("User already exists.", 'error')
            else:
                hashed_password = generate_password_hash(user_password).decode('utf-8')
                user = User(user_name=user_name,
                            user_password=hashed_password,
                            user_email=user_email)
                try:
                    db.session.add(user)
                    db.session.commit()
                    flash("Registration successful!", 'success')
                except IntegrityError:
                    db.session.rollback()
                    flash("Username or email already exists.", 'error')
                except Exception as e:
                    db.session.rollback()
                    flash(f"An error occurred: {str(e)}", 'error')

        elif form_type == 'login':
            user_name = request.form.get('user_name')
            user_password = request.form.get('user_password')

            user = User.query.filter_by(user_name=user_name).first()  # find the user by username
            if user and check_password_hash(user.user_password, user_password):  # check password hash
                login_user(user)
                return redirect(url_for('main.home'))
            else:
                flash("Invalid username or password.", 'error')

    return render_template('register_login.html')

@main.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        print("Debug: Current user " + current_user.user_name + " is logged out")
    logout_user()
    return redirect(url_for('main.register_login'))


@main.route('/admin')
@login_required
def admin():
    if not current_user.user_name == 'admin':
        flash('Only admins have access to the Admin tab.')
        return redirect(url_for('main.register_login'))

    inventory_list = Inventory.query.all()
    return render_template('admin.html', inventory = inventory_list)

@main.route('/add_item', methods=['POST'])
def add_item():
    try:
        number = request.form['number']
        description = request.form['description']
        registration_date = date.fromisoformat(request.form['registration_date'])
        status = request.form['status']
        booked = request.form['booked']

        new_item = Inventory(number=number, description=description, registration_date=registration_date, status=status, booked=booked)
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!', 'success')
    except IntegrityError:
        # rollback the session in case of error
        db.session.rollback()
        flash('Number already exists. Please choose a different number.', 'error')
    except Exception as e:
        # handle any other exceptions
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'error')

    return redirect(url_for('main.admin'))

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Inventory.query.get_or_404(id)

    if request.method == 'POST':
        try:
            # check if item is in use and status change is attempted
            if item.booked == 'In use' and item.status != request.form['status']:
                flash('The status cannot be changed while the item is in use. Please release the item before making any changes.', 'warning')
                return redirect(url_for('main.edit_item', id=id))

            item.number = request.form['number']
            item.description = request.form['description']
            item.registration_date = date.fromisoformat(request.form['registration_date'])
            item.status = request.form['status']
            item.booked = request.form['booked']
            db.session.commit()
            return redirect(url_for('main.admin'))
        except IntegrityError:
            # rollback the session in case of error
            db.session.rollback()
            flash('Number already exists. Please choose a different number.', 'warning')

    return render_template('edit_item.html', item=item)

@main.route('/delete/<int:id>', methods=['POST'])
def delete_item(id):
    try:
        # attempt to add and commit the new category to the database
        db.session.delete(Inventory.query.get_or_404(id))
        db.session.commit()
        flash('Item deleted successfully!', 'success')
    except IntegrityError:
        # rollback the session in case of error
        db.session.rollback()
        flash('Cannot delete! This item is booked by {{ user.user_name }}.', 'error')
    return redirect(url_for('main.admin'))


@main.route('/about')
def about():
    return render_template('about.html')

