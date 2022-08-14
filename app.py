from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'pymysql'

mysql = MySQL(app)


@app.route("/")
def home():
    cur = mysql.connection.cursor()
    result = cur.execute("select * from todo")
    if result > 0:
        todo_list = cur.fetchall()
        return render_template("base.html", todo_list=todo_list)
    return render_template("base.html")


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    cur = mysql.connection.cursor()
    cur.execute("insert into todo(title, complete) values(%s,%s)", (title, False))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    cur = mysql.connection.cursor()
    cur.execute("select complete from todo where id = %s", str(todo_id))
    tasks = cur.fetchall()
    cur.execute('update todo set complete = %s where id = %s', (not tasks[0][0], todo_id))
    mysql.connection.commit()
    return redirect(url_for("home"))



@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    cur = mysql.connection.cursor()
    cur.execute('delete from  todo where id = %s', str(todo_id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("home"))


if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)
