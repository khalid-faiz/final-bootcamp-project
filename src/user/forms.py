# A script for login and regiteration forms
# Import the necessary libraries
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length # Validators for severver side validation

# Import the User Model
from src.models import User

# Create the login form class
class LoginForm(FlaskForm):
    # Properties are emal and Password
    email = EmailField("Email",validators=[DataRequired(), Email()] )
    password = PasswordField("Password", validators=[DataRequired()])


# Create the regiteration form
class RegisterForm(FlaskForm):
    # Properties are name, email, password and its confirmation
    name = StringField(
        "Name", validators=[DataRequired(), Length(min=3)]
    )
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Repeat Password",
        validators=[

            DataRequired(),
            EqualTo("password", message="Passwords should match.")
        ]
    )

    def validate(self):
        # Form vaidation
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email alreay registered")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Passwords should match")
            return False
        return True
