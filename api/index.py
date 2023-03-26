"""WeatherApp - Asia Misner    CMSC495    3/19/2023
                Isaac Olmedo
                Lucas Cichorski
                Zachary Callahan
"""

import datetime
"""import gc"""
from functools import wraps
"""import the Quart library instead of Flask"""
from quart import Quart, flash, render_template, request, redirect, url_for, session
import pandas as pd
from wtforms import Form, TextAreaField, PasswordField, validators
from wtforms.validators import InputRequired
from passlib.hash import sha256_crypt

"""create an ASGI app instance instead of a WSGI app instance"""
app = Quart(__name__)

"""route the home page to the root URL"""

@app.route("/")
@app.route('templates/HomePage.html', methods=['GET', 'POST'])
def home_page():
    """Home Page.

    :return:
    Web page for Weatherwise, a new way to view weather..."""
    #if session['logged_in'] = True:
        #session.clear()
        #FIRSTVISIT = False
    return render_template('templates/HomePage.html', date=datetime.datetime.now())


class RegistrationForm(Form):
    """Registration form class.

    Define the requirements for the information that the user
    will be submitting into the registration page."""
    username = TextAreaField('Username (min:4, max:20)', [validators.Length(min=4, max=20),
                                                          InputRequired()])
    email = TextAreaField('Email Address (min:6, max:50)', [validators.Length(min=6, max=50),
                                                            InputRequired(), validators.Regexp("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:.[a-zA-Z0-9-]+)*$/"),
                                                            validators.EqualTo('confirm_email', message='Emails must match.')])
    confirm_email = TextAreaField('Repeat Email Address')
    password = PasswordField('Password: '
                             '\n Requirements: minimum of 12 characters\n'
                             '              at least 1 uppercase letter\n'
                             '              at least 1 lowercase letter\n'
                             '              at least 1 number\n'
                             '              at least 1 special character',
                             [InputRequired(),
                              validators.Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])"
                                                "(?=.*?[#?!@$%^&*-]).{12,}$"),
                              validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Repeat Password')


class ChangePassForm(Form):
    """ChangePassForm form class.

    Define the requirements for the information that the user
    will be submitting into the change password page."""
    username = TextAreaField('Username', [InputRequired()])
    oldpass = PasswordField('Previous Password', [InputRequired()])
    newpass = PasswordField('New Password \n'
                            'Requirements: minimum of 12 characters\n'
                            '              at least 1 uppercase letter\n'
                            '              at least 1 lowercase letter\n'
                            '              at least 1 number\n'
                            '              at least 1 special character',
                            [InputRequired(),
                             validators.Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])"
                                               "(?=.*?[#?!@$%^&*-]).{12,}$"),
                             validators.EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField('Repeat New Password')


@app.route('/Signup.html', methods=['GET', 'POST'])
async def register():
    """Registration Page for users.

    :return:
    takes users username, password, confirmed password, and email.
    validates the input, by forcing the user to submit something in
    each field and then puts requirements on the password length and what
    it contains. Then searches the username csv to see if the username has
    already been used, if so, prompt the user to enter a different username.
    If all checks out, append the account information to the users.csv file."""
    form = RegistrationForm(await request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        d_f = pd.read_csv(r'C:\capstone\templates\accounts.csv')
        data = {
            'username': [form.username.data],
            'password': [sha256_crypt.encrypt((str(form.password.data)))],
            'email': [form.email.data]
        }
        temp_df = pd.DataFrame(data)
        for user in enumerate(d_f.username):
            print(username)
            print(user)
            if str(username) == str(user[1]):
                await flash("That username is already taken, please choose another.")
                return await render_template('Signup.html', form=form)
        temp_df.to_csv(r'C:\capstone\templates\accounts.csv',
                       mode='a', index=False, header=False)
        await flash("Thanks for registering!")
        session["logged_in"] = True
        session["username"] = username
        return redirect(url_for('home_page'))
    return await render_template("Signup.html", form=form)


@app.route('/login.html', methods=["GET", "POST"])
async def login():
    """Benefits homepage for CRNAs that want to transition to 1099 work.

    :return:
    Benefits will be placed in an unordered list."""
    date_time_obj = datetime.datetime.now()
    timestamp_str = date_time_obj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    if request.method == "POST":
        d_f = pd.read_csv(r'C:\capstone\templates\accounts.csv')
        for i, user in enumerate(d_f.username):
            if await request.form['username'] == str(user) and \
                    sha256_crypt.verify(request.form['password'], d_f.password[i]):
                session['logged_in'] = True
                session['username'] = await request.form['username']
                flash('You are logged in as ' + str(user))
                return redirect(url_for('preferences'))
        data = {
            'username': await request.form['username'],
            'ip': [await request.remote_addr],
            'timestamp': [timestamp_str]
        }
        temp_df = pd.DataFrame(data)
        temp_df.to_csv(r'C:\capstone\templates\FailedLoginAttemptsLog.csv',
                       mode='a', index=False, header=False)
        flash("Invalid credentials. Try Again.")
    return await render_template('login.html')


def login_required(func):
    """login required.

    :param func:
    :return:
    Create a wrapper to refuse access to certain pages until a user has logged in."""
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/logout.html")
@login_required
def logout():
    """logout.

    :return:
    Clear session, garbage collect and redirect user to the home page."""
    session.clear()
    flash("You have been logged out!")
    """gc.collect()"""
    return redirect(url_for('home_page'))


@app.route("/change_password.html", methods=["GET", "POST"])
@login_required
def change_password():
    """Change Password.

    :return:
    Users information will be passed to the ChangePassForm object, if validated
    and the user's username matches a previously registered username, and they
    are currently logged in as that user and their old password matches
    the previously stored password. Then their new password will be compared
    to the CommonPasswords.csv file. If their new password doesn't match
    then it will be stored in the accounts.csv as the new password"""
    form = ChangePassForm(await request.form)
    current_user = session['username']
    print(current_user)
    if request.method == "POST" and form.validate():
        d_f = pd.read_csv(r'C:\capstone\templates\accounts.csv')
        c_p = pd.read_csv\
            (r'C:\capstone\templates\CommonPasswords.csv')
        for i, user in enumerate(d_f.username):
            if form.username.data == str(user) and \
                    sha256_crypt.verify(str(form.oldpass.data), d_f.password[i]) and \
                    str(user) == session['username']:
                for k in enumerate(c_p.Passwords):
                    if str(form.newpass.data) == str(k):
                        flash("Password is too easy. Try again")
                        return await render_template('change_password.html', form=form)
                #data = {
                    #'username': [form.username.data],
                    #'password': [sha256_crypt.encrypt((str(form.newpass.data)))],
                    #'email': [d_f.email[i]]
                    #}
                #temp_df = pd.DataFrame(data)
                #d_f.password[i].drop()
                """sha256_crypt.encrypt is not an asynchronous function"""
                d_f.password[i] = await sha256_crypt.hash((str(form.password.data)))

                #d_f.drop([i,i]).to_csv
                # (r'C:\capstone\templates\accountsTest.csv')
                #print(d_f)
                #d_f.dropna().to_csv
                # (r'C:\capstone\templates\accountsTest.csv')
                #print(d_f)
                d_f.to_csv(r'C:\capstone\templates\accounts.csv')
                #temp_df.to_csv
                # (r'C:\capstone\templates\accountsTest.csv',
                               #mode='a', index=False, header=False)
                flash("Your password has been successfully changed.")
                return redirect(url_for('home_page'))
        # if count == len(d_f.username):
        # flash("Invalid credentials. Try Again.")
    return await render_template('change_password.html', form=form)


@app.route('/Preferences.html', methods=["GET", "POST"])
@login_required
def preferences():
    """Preferences webpage.

    :return:
    User will be able to enter zip code or city and state for
    which they would like to receive weather for."""
    return await render_template('Preferences.html', date=datetime.datetime.now())


@app.route('/Contact.html', methods=["GET"])
def contact():
    """Contact information for the development team.

    :return:
    POCs will be placed in an unordered list."""
    return await render_template('Contact.html', date=datetime.datetime.now())


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    """remove the debug mode that is not supported by Vercel"""
    app.run()


@app.errorhandler(404)
def page_not_found(e):
    return await render_template('404.html')

