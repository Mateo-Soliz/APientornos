from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,DateField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo,ValidationError
from models import db, User
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).first():
            raise ValidationError('Email is already in use')

class TaskForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha Inicio', validators=[DataRequired()])
    fecha_fin = DateField('Fecha Fin', validators=[DataRequired()])
    submit = SubmitField('Create Task')

class EditTaskForm(FlaskForm):
    Task = StringField('Task', validators=[DataRequired()])
    Description = StringField('Description', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha Inicio', validators=[DataRequired()])
    fecha_fin = DateField('Fecha Fin', validators=[DataRequired()])
    completed = SelectField('Completed', choices=[(1, 'Completado'), (0, 'Sin completar')])
    submit = SubmitField('Update Task')