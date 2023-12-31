""" 
Importing necessary modules and classes 
"""
from app import app, bcrypt, db
from app.forms import RegistrationForm
from app.models import User, ShoppingCart
from flask import flash, render_template, redirect, url_for
from flask_login import login_user

"""
Creating a new account route
"""
@app.route("/create_account", methods=["GET", "POST"])
def create_user():
    form = RegistrationForm()

    """
    Validate form submission
    """
    if form.validate_on_submit():
        try:
            username = form.username.data
            """
            Check if the username has no spaces
            """
            if " " in username:
                flash("Username needs to be a single word without spaces", category="danger")
            else:
                """
                Extract form data
                """
                first_name = form.first_name.data
                last_name = form.last_name.data
                email_address = form.email_address.data
                category = form.category.data
                password_hash = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')

                """
                Create a new user
                """
                new_user = User(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email_address=email_address,
                    category=category,
                    password_hash=password_hash
                )
                
                """
                Add new user to the database
                """
                db.session.add(new_user)
                db.session.commit()

                """
                Log in the new user
                """
                login_user(new_user)

                """
                Create a shopping cart for the new user
                """
                cart = ShoppingCart(user_id=new_user.id, total_amount=0)
                db.session.add(cart)
                db.session.commit()

                """
                Display success message and redirect to user dashboard
                """
                flash(f"Success in creating account. You are logged in as {new_user.username}", category="success")
                return redirect(url_for('user_dashboard', username=new_user.username))
        except Exception as e:
            """
            Rollback in case of an exception
            """
            db.session.rollback()
            flash(f"Error creating account: Try again", category="danger")

    """
    Display form validation errors
    """
    if form.errors:
        for error_msg in form.errors.values():
            flash(f"You have the following error: {error_msg}", category='danger')

    """
    Render the create_user.html template with the form
    """
    return render_template("create_user.html", form=form)
