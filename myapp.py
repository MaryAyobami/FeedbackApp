from flask import Flask , render_template , request
from sendmail import send_mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:bams@localhost:5432/feedbackapp"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    Attendant = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, Attendant, rating, comments):
        self.customer = customer
        self.Attendant = Attendant
        self.rating = rating
        self.comments = comments
    


@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/submit",methods = ["POST"])
def submission():
    if request.method == "POST":
        customer = request.form['customer']
        Attendant = request.form['Attendant']
        rating = request.form['rating']
        comments = request.form['comments']
        if customer == '' or Attendant == '':
            return render_template('index.html', message='Please enter required fields')  
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer,Attendant, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer,Attendant, rating, comments)
            return render_template('sucess.html')
        return render_template('index.html', message='You have already submitted feedback, A customer can only submit feedback once')

@app.route("/comments",methods =["GET"])
def get_comments():
    if request.method == "GET":
        comments = db.session.query(Feedback).all()
        for item in comments:
            return {
                "<h1>COMMENTS</h1>"
                "id":item.id,
                "Customer's name": item.customer,
                "Attendant": item.Attendant,
                "rating":item.rating,
                "comment":item.comments
                
            }

if __name__ == "__main__":
    app.run(debug=True)