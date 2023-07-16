from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
app = Flask(__name__)

@app.route('/')
@app.route('/retrieve')
def retrieve():
    con=sql.connect("user_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from user_table")
    data=cur.fetchall()
    return render_template('retrieve.html',datas=data)

@app.route('/create',methods=['POST','GET'])
def create():
    if request.method=='POST':
        name=request.form['name']
        contact=request.form['contact']
        con=sql.connect("user_db.db")
        cur=con.cursor()
        cur.execute("insert into user_table(name,contact) values(?,?)",[name,contact])
        con.commit()
        flash('Data Saved','success')
        return redirect(url_for("retrieve"))
    return render_template('create.html')

@app.route('/update/<string:id>',methods=['POST','GET'])
def update(id):
    con=sql.connect("user_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from user_table where id=?",[id])
    data=cur.fetchone()
    if request.method=='POST':
        name=request.form['name']
        contact=request.form['contact']
        con=sql.connect("user_db.db")
        cur=con.cursor()
        cur.execute("update user_table set name=?,contact=? where id=?",[name,contact,id])
        con.commit()
        flash('Data updated','success')
        return redirect(url_for("retrieve"))
    return render_template('update.html',datas=data)

@app.route('/delete/<string:id>',methods=['GET'])
def delete(id):
    con=sql.connect("user_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("delete from user_table where id=?",[id])
    con.commit()
    flash('Data Deleted','warning')
    return redirect(url_for("retrieve"))

if __name__ =='__main__':
    app.secret_key='admin123'
    app.run(debug=True)
