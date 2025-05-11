import uuid
from flask import Flask, render_template, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, fields
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)

class PaymentModel(db.Model):
    """

    Payment Model
    This is the SQLAlchemy model for the Payment table.
    
    """
    id = db.Column(db.Integer, primary_key=True)
    payer = db.Column(db.String(80), nullable=False)
    payee = db.Column(db.String(80), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payerMessage = db.Column(db.String(80), nullable=True)
    paymentReference = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f"<Payment {self.payer} to {self.payee}>"

class PaymentCheckAPI(Resource):
    """

    Payment Check API that checks the payment details based on the payment reference number.

    """
    def get(self):
        """
        Get payment details based on the payment reference number.

        returns: psyment details rendered in an HTML page if found, otherwise returns a 404 error.
        """
        # Check for the reference in the query parameters
        payment_reference_number = request.args.get('PaymentReferenceNumber')
        
        # Check if the reference number is provided
        if not payment_reference_number:
            return {"message": "PaymentReferenceNumber is required"}, 400
        
        # Query database for payment with the entered payment reference
        payment = PaymentModel.query.filter_by(paymentReference=payment_reference_number).first()
        
        # If the payment is not found, return a 404 error
        if not payment:
            return{"message":"Payment not found"}, 404
        # If payment exists, pass the payment details to the template
        return make_response(render_template("paymentFound.html", payment=payment))
api.add_resource(PaymentCheckAPI, '/payment')

class PaymentInitiationAPI(Resource):
    """
    Payment Initiation API that handles the initiation of a payment.
    """
    def post(self):
        """
        Initiate a payment by creating a new payment record in the database.
        returns: payment details rendered in an HTML page.
        
        """
        data = request.form

        # Generate a unique 10-character reference number
        reference_number = str(uuid.uuid4().hex[:10]).upper()
        # print(f"Generated reference number: {reference_number}")

        new_payment = PaymentModel(
            payer=data['payer'],
            payee=data['payee'],
            currency=data['currency'],
            amount=data['amount'],
            payerMessage=data.get('payerMessage'),
            paymentReference=reference_number
        )
        db.session.add(new_payment)
        db.session.commit()
        return make_response(render_template("paymentMade.html", payment=new_payment))
api.add_resource(PaymentInitiationAPI, '/initiatePayment')

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/initiatePayment")
def initiatePayment():
    return render_template("initiatePayment.html")

@app.route("/checkPayment")
def checkPayment():
    return render_template("checkPayment.html")

if __name__ == "__main__":
    app.run(debug=True)