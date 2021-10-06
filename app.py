from flask import Flask , render_template, request, redirect
from datetime import datetime
from time import sleep
from flask.helpers import url_for
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import LoginManager, UserMixin, login_manager, login_user, login_required, logout_user, current_user
from werkzeug.security import  check_password_hash #use sha256



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///rds.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'KiyotakaAyanokojiRocks'
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__= 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(60), nullable=True)
    isAdmin = db.Column(db.Boolean(), nullable=False, server_default="0")
    appliedForLeave = db.Column(db.Boolean(), nullable=False, server_default="0")
    leavesApplied = relationship("Leave", back_populates="userId", cascade="all, delete",
        passive_deletes=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"{self.username}"

class Leave(db.Model):
    __tablename__= 'Leave'
    id = db.Column(db.Integer, primary_key=True)
    userId = relationship("User", back_populates="leavesApplied")
    user = db.Column(db.Integer, ForeignKey('User.id'))
    abstract = db.Column(db.String(65), nullable=False)
    fromDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    toDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    summary = db.Column(db.String(65), nullable=False, default='Plz Understand... 😭')
    leaveAccepted = db.Column(db.Boolean(), server_default="0")
    leaveRejected = db.Column(db.Boolean(), server_default="0")

    def __repr__(self) -> str:
        return f"{self.abstract}"


class LeaveHandeler:
    user:User
    def __init__(self, user:User) -> None:
        self.user = user

    def applyLeave(self, request:request) -> bool:
        if request.method=="POST":
            userId = self.user
            abstract = request.form["abstract"]
            fromDate = request.form["fromdate"]
            holdtime = list(map(int, fromDate.split("-")))
            fromDate = datetime(holdtime[0], holdtime[1], holdtime[2])
            toDate = request.form["todate"]
            holdtime = list(map(int, toDate.split("-")))
            toDate = datetime(holdtime[0], holdtime[1], holdtime[2])
            summary = request.form["summary"]
            print(fromDate, toDate)
            
            adding = Leave(userId=userId, abstract=abstract,fromDate=fromDate,toDate=toDate,summary=summary)
            
            db.session.add(adding)
            db.session.commit()
            return True
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def start_page() -> render_template:
    """
    The Start page will only include a Login page for the employer and Employee...
    Login Credintials will determine the Acount type ad the privilages one account has
    """
    user = User.query.filter_by(username="@lonewolf").first()

    login_user(user)
    
    return render_template("index.html")

@app.route("/login")#, methods=['POST'])
@login_required
def login() -> redirect:
    #user = User.querry.filter_by(username="@mr.x")

    #login_user(user)
    if current_user.isAdmin:
        return redirect(url_for("admin_dashboard"))
    else:
        return redirect(url_for("user_dashboard"))


@app.route("/commander-dashboard")
@login_required
def admin_dashboard() -> render_template:
    """
    The Start page will only include a Login page for the employer and Employee...
    Login Credintials will determine the Acount type ad the privilages one account has
    """

    return render_template("admin_dashboard.html")


@app.route("/magot-dashboard")
@login_required
def user_dashboard() -> render_template:
    """
    The Start page will only include a Login page for the employer and Employee...
    Login Credintials will determine the Acount type ad the privilages one account has
    """

    return render_template("emp_dashboard.html")


@app.route("/magot-applyLeave", methods = ["POST","GET"])
@login_required
def apply_for_leave():
    addLeave = LeaveHandeler(current_user)
    addLeave.applyLeave(request)
    return redirect(url_for("user_dashboard"))

    

@app.route("/logout")#, methods=['POST'])
@login_required
def logout() -> render_template:
    k = f"<p>{current_user.first_name} has been logout</p>"
    logout_user()
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
