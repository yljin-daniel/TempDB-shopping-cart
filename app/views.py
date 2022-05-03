from ast import For
from cgi import print_exception
from cmath import inf
from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from app.forms import CustomerRegForm, LoginForm
from app.models import Customer, Goods, Orders, OrderLineItem
import config
import random
import datetime

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
currentOrder = 2

@app.route('/reg', methods=['GET', 'POST'])
def register():
    form = CustomerRegForm(request.form)
    if request.method == 'POST'and form.validate():
        c=db.engine.execute('select * from Customers where id= ?', form.userid.data)
        row = c.fetchone()
        if row is None:
            new_customer = Customer()
            new_customer.id = form.userid.data
            new_customer.name = form.name.data
            new_customer.password = form.password.data
            new_customer.address = form.address.data
            new_customer.birthday = form.birthday.data
            new_customer.phone = form.phone.data
            # insert into Customers values (?????)
            db.session.add(new_customer) 
            db.session.commit()

            print('Register Success')
            return render_template('customer_reg_success.html', form=form)
        else:
            flash('This id has been taken.')
            return render_template('customer_reg.html', form=form)

    return render_template('customer_reg.html', form=form)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST'and form.validate():
            c = db.session.query(Customer).filter_by(id=form.userid.data).first()
            c = db.engine.execute('select * from Customers where id= ?', form.userid.data).fetchone()
            if c is not None and c[2] == form.password.data:
                print('Login Success')
                customer = {}
                customer['id'] = c[0]
                customer['name'] = c[1]
                customer['password'] = c[2]
                customer['address'] = c[3]
                customer['phone'] = c[4]
                customer['birthday'] = c[5]
                session['customer'] = customer

                return redirect(url_for('main'))
            else:
                flash('There may be errors in User id or Password.')
                return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/account', methods=['GET', 'POST'])
def show_account():
    dt = session['customer']['name']
    c = db.session.query(Orders).filter_by(user_name =session['customer']['name'])
    msg = []
    for i in c:
        msg.append(i.id)
        # msg += "\n order.id:" + str(i.id)
    # print("!!!!!!!!!!!")
    # print(msg)
    return render_template('account.html', nm = dt, od = c)

@app.route('/main')
def main():
    if 'customer' not in session.keys():
        flash('Please Login.')
        return redirect(url_for('login'))
    return render_template('main.html')


@app.route('/list')
def show_goods_list():
    if 'customer' not in session.keys():
        flash('Please Login')
        return redirect(url_for('login'))

    goodslist = db.session.query(Goods).all()
    return render_template('goods_list.html', list=goodslist)

@app.route('/newList', methods=['GET', 'POST'])
def show_goods_list_new():
    if 'customer' not in session.keys():
        flash('Please Login')
        return redirect(url_for('login'))
    ft = 999999999
    lt = ft
    if request.method == 'POST':
        ft = request.form.get('user')
    db.engine.execute('select * from Goods where price in [?, ?]',lt,ft)
    goodslist = db.session.query(Goods).filter(Goods.price<ft).all()
    return render_template('goods_list.html', list=goodslist)

@app.route('/detail')
def show_goods_detail():
    if 'customer' not in session.keys():
        flash('Please Login')
        return redirect(url_for('login'))

    goodsid = request.args['id']
    goods = db.session.query(Goods).filter_by(id=goodsid).first()

    return render_template('goods_detail.html', goods=goods)


@app.route('/add')
def add_cart():
    if 'customer' not in session.keys():
        flash('Pleases Login')
        return redirect(url_for('login'))

    goodsid = int(request.args['id'])
    goodsname = request.args['name']
    goodsprice = float(request.args['price'])

    if 'cart' not in session.keys():
        session['cart'] = []

    cart = session['cart']
    flag = 0
    for item in cart:
        if item[0] == goodsid:  # goods id
            item[3] += 1  # item count ++
            flag = 1
            break

    if flag == 0:
        # initialized item first added to 1
        cart.append([goodsid, goodsname, goodsprice, 1])

    session['cart'] = cart

    print(cart)

    flash('Item [' + goodsname + '] has added to your Cart')
    return redirect(url_for('show_goods_list'))



@app.route('/cart')
def show_cart():
    if 'customer' not in session.keys():
        flash('Please Login')
        return redirect(url_for('login'))

    if 'cart' not in session.keys():
        return render_template('cart.html', list=[], total=0.0)

    cart = session['cart']
    list = []
    total = 0.0
    for item in cart:
        subtotal = item[2] * item[3]
        total += subtotal
        new_item = (item[0], item[1], item[2], item[3], subtotal)
        list.append(new_item)

    return render_template('cart.html', list=list, total=total)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    orders = Orders()
    # Order id is produced by time stamp and one random digit
    n = random.randint(0, 9)
    d = datetime.datetime.today()
    orderid = str(int(d.timestamp() * 1e6)) + str(n)
    orders.id = orderid
    orders.user_name = session['customer']['name']
    orders.orderdate = d.strftime('%Y-%m-%d %H:%M:%S')
    orders.status = 1  # 1 Unpaid 0 Paid
    currentOrder = orderid
    print("This is order ID!" + currentOrder)
    db.session.add(orders)
    cart = session['cart']
    total = 0.0
    for item in cart:
        quantity = request.form['quantity_' + str(item[0])]
        try:
            quantity = int(quantity)
        except:
            quantity = 0
        subtotal = item[2] * quantity
        total += subtotal

        order_line_item = OrderLineItem()
        order_line_item.quantity = quantity
        order_line_item.goodsid = item[0]
        order_line_item.orderid = orderid
        order_line_item.subtotal = subtotal

        db.session.add(order_line_item)

    orders.total = total
    db.session.commit()

    # Empty cart
    session.pop('cart', None)

    return render_template('order_finish.html', orderid=orderid)
