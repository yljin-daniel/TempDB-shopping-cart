from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from app.forms import RegistrationForm, LoginForm
from app.models import cart, information, User

app=Flask(__name__)

app.config['SECRET_KEY'] = 'enydM2ANhdcoKwdVa0jWvEsbPFuQpMjf'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///../db/shopping.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['DEBUG']=True
db=SQLAlchemy(app)


@app.route('/')
def index():  # 主页
    return render_template("index.html", data = 1)

@app.route('/productList', methods=['GET', 'POST'])
def productList():  # 产品列表
    if request.method == 'POST':

        if request.form['buy']=="p1":  # 购买product1
            itemName = "Product1"
            tempUser = cart(name = itemName)
            db.session.add(tempUser)
        elif request.form['buy']=="p2":  # 购买product2
            itemName = "Product2"
            tempUser = cart(name = itemName)
            db.session.add(tempUser)
        elif request.form['buy']=="p3":  # 购买product3
            itemName = "Product3"
            tempUser = cart(name = itemName)
            db.session.add(tempUser)

    return render_template("productList.html", data = 1)

@app.route('/cart', methods=['GET', 'POST'])
def cart_view():  # 购物车页面
    list = cart.query.all()  # 展示购物车数据库
    return render_template("cart.html", data = list)  # 把购物车数据库传入前端

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():#结算页面
    if request.method == 'POST':
        fn = request.form.get('firstname')
        ln = request.form.get('lastname')
        pays = request.form.get('pays')
        for items in cart.query.all():
            print('test')
            tempUser = information(firstName=fn, lastName=ln, payment=pays, itemName=items.name)
            db.session.add(tempUser)
    return render_template("checkout.html", data = 1)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST'and form.validate():
            c = db.session.query(User).filter_by(id=form.userid.data).first()
            if c is not None and c.password == form.password.data:
                print('Login Success')
                customer = {}
                customer['id'] = c.id
                customer['name'] = c.name
                customer['password'] = c.password
                customer['address'] = c.address
                customer['phone'] = c.phone
                customer['email'] = c.email
                # customer保持到HTTP Session
                session['customer'] = customer

                return redirect(url_for('main'))
            else:
                flash('The username is not matched with password input.')
                return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        uid=form.userid.data
        userN = form.username.data
        pas = form.password.data
        Email = form.email.data
        phoneNumber = form.phone.data
        addr = form.address.data
        tempUser = User(id=uid, name = userN, password = pas, email = Email,  address = addr, phone = phoneNumber)
        db.session.add(tempUser)
        db.session.commit()
        return render_template('login.html', form=form)
    return render_template('registration.html', form = form)

@app.route('/main')
def main():
    if 'customer' not in session.keys():
        flash('You should Login first.')
        return redirect(url_for('login'))
    return render_template('index.html')

if __name__=="__main__":
    db.drop_all()
    db.create_all()#删除并重新创建数据库
    app.run(port=2020,host="127.0.0.1",debug=True)
