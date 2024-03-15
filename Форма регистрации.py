from flask import Flask, render_template

from data import db_session
from data.users import User
from login_form import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/register', methods=['GET', 'POST'])
def login():
    db_session.global_init('db/mars.db')
    db_sess = db_session.create_session()
    form = LoginForm()  
    fields = ['email', 'password', 'password_again', 'surname', 'name', 
              'age', 'position', 'speciality', 'address'] 
    params = {'title': 'Регистрация',
              'fields': fields,
              'form': form,
              'message': ''}
    if form.validate_on_submit():     
        if form.password.data != form.password_again.data:
            params['message'] = 'Пароли не совпадают'
        elif db_sess.query(User).filter(User.email == form.email.data).first():
            params['message'] = 'Такой пользователь уже есть'
        else:
            user_params = {field: getattr(form, field).data for field in fields if 'password' not in field}
            user = User(**user_params)
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return render_template('successful_login.html', title='Регистрация завершена')
    return render_template('login.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')