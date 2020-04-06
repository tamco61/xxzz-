from flask import Flask, render_template, request, redirect
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    email = StringField('Login / email', validators=[DataRequired()])
    password_first = PasswordField('Password', validators=[DataRequired()])
    password_second = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/login' , methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        if form.validate_on_submit():
            return redirect('/success')
        return render_template('login.html', title='Авторизация', form=form)
    elif request.method == 'POST':
        db_session.global_init('db/mars_explorer.sqlite')
        session = db_session.create_session()
        data = [i.email for i in session.query(User).all()]
        if form.email.data in data:
            return 'Error email'
        if form.password_first.data != form.password_second.data:
            return 'Error password'
        user = User()
        user.email = form.email.data
        user.name = form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.hashed_password = form.password_second.data
        session.add(user)
        session.commit()
        
        return 'OK'


def main():
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()