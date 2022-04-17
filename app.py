from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Test:1234@localhost:5432/test_task'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False
db = SQLAlchemy(app)


class Trips(db.Model):
    __tablename__ = 'Trips'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Trips %r>' % self.id  # будет выдаваться объект и его id


@app.route('/')
def main_page():
    return render_template("main_page.html")


@app.route('/trips', methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/trips/<int:page>', methods=['GET', 'POST'])
def all_trips(page):
    # page = request.args.get('page')
    page = page
    pages = 5
    # pages = trips.paginate(page=page, per_page=5)
    # trips = Trips.query.paginate(page, pages, error_out=False)
    trips = Trips.query.order_by(Trips.id.asc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form['tag']
        search = "% {} %".format(tag)
        trips = Trips.query.filter(Trips.title.like(search) | Trips.quantity.like(search) | Trips.quantity.like(distance)).paginate(per_page=pages, error_out=False)
        return render_template('trips.html', trips=trips, tag=tag)
    return render_template("trips.html", trips=trips)


@app.route('/create_trip', methods=['POST', 'GET'])
def create_trip():
    if request.method == "POST":
        title = request.form['title']  # название идет из name на стр create_article
        quantity = request.form['quantity']
        distance = request.form['distance']

        trip = Trips(title=title, quantity=quantity, distance=distance)
        try:
            db.session.add(trip)
            db.session.commit()
            return redirect('/trips')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create_trip.html")


if __name__ == "__main__":
    app.run(debug=True)

