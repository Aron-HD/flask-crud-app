from .secrets import SECRET_KEY
from .models import db, UserModel
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__, template_folder='templates')
app.secret_key = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# ERROR HANDLERS


@app.errorhandler(404)
def not_found(e):
    return render_template('http/404.html', error=e)


@app.errorhandler(500)
def server_error(e):
    return render_template('http/500.html', error=e)


@app.route('/home')
@app.route("/", methods=["GET", "POST"])
def home():
    contacts = UserModel.query.all()
    return render_template('index.html', contacts=contacts)


@app.route('/data', methods=['GET', 'POST'])
def RetrieveList():

    if request.method == 'GET':
        employees = UserModel.query.all()

        return render_template('data_pages/datalist.html',
                               employees=employees)

    if request.method == 'POST':
        try:
            data = {"user_id": request.form['user_id'],
                    "name": request.form['name'],
                    "surname": request.form['surname'],
                    "age": request.form['age'],
                    "role": request.form['role']}
            employee = UserModel(**data)
            db.session.add(employee)
            db.session.commit()
            employees = UserModel.query.all()
        except Exception as e:
            print(e)
            flash(
                f"Invalid request - make sure fields are not empty {e}", 'error')
            return redirect(url_for('RetrieveList'), code=404)
        flash(f"added {employee} {employee.user_id}", 'success')
        return render_template('data_pages/datalist.html', employees=employees)


@app.route('/data/<int:user_id>')
def RetrieveEmployee(user_id):
    employee = UserModel.query.filter_by(user_id=user_id).first()
    if employee:
        return render_template('data_pages/data.html', employee=employee)
    flash(f"user_id {employee.user_id} does not exist", 'error')
    return redirect(url_for('RetrieveList'), code=404)


@app.route('/data/<int:user_id>/update', methods=['GET', 'POST'])
def update(user_id):
    employee = UserModel.query.filter_by(user_id=user_id).first()
    if request.method == 'POST':
        if employee:
            try:
                db.session.delete(employee)
                db.session.commit()
                data = {
                    "user_id": user_id,
                    "name": request.form['name'],
                    "surname": request.form['surname'],
                    "age": request.form['age'],
                    "role": request.form['role']}
                employee = UserModel(**data)
                db.session.add(employee)
                db.session.commit()
                employees = UserModel.query.all()
                flash(f"updated {user_id}", 'success')
                return render_template('data_pages/datalist.html', employees=employees)
            except Exception as e:
                print(e)
                flash(f"Invalid request {user_id} not updated", 'error')
                return redirect(url_for('RetrieveList'), code=400)

        flash(f"Employee with user_id = {user_id} Doesn't exist", 'error')
        return redirect(url_for('RetrieveList'), code=404)

    return render_template('data_pages/update.html', employee=employee)


@app.route('/data/<int:user_id>/delete', methods=['GET', 'POST'])
def delete(user_id):
    employee = UserModel.query.filter_by(user_id=user_id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            flash(f"user_id {employee.user_id}", 'deleted')
            return redirect(url_for('RetrieveList'), code=200)
        flash(f"user_id {employee.user_id} does not exist", 'error')
        return redirect(url_for('RetrieveList'), code=404)
        # abort(404)

    return render_template('data_pages/delete.html', employee=employee)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
