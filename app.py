from flask import render_template,redirect,url_for,Flask
from flask_login import login_required, current_user,logout_user,login_user,LoginManager
from datetime import datetime
from models import db, User, Task
from forms import LoginForm, SignupForm, TaskForm, EditTaskForm
from apiDB import api

app = Flask(__name__)
api.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

@app.route('/')
@login_required
def index():
    tareas = db.session.query(Task).filter_by(user_id=current_user.id).all()
    porcentajeCompletados = 0
    for tarea in tareas:
        if tarea.completed == 1:
            porcentajeCompletados += 1
    if len(tareas) > 0:
        porcentajeCompletado = (porcentajeCompletados/len(tareas))*100
    else:
        porcentajeCompletado = 0
    sinCompletar = len(tareas) - porcentajeCompletados
    TodasTareas = len(tareas)
    return render_template('index.html', porcentajeCompletado=porcentajeCompletado, sinCompletar=sinCompletar, TodasTareas=TodasTareas)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User( email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        print("asdasd",login_user(user))
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(Task=form.task.data, Description=form.description.data, fecha_inicio=form.fecha_inicio.data, fecha_fin=form.fecha_fin.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_task.html', form=form)

@app.route('/tasks/<tipo>', methods=['GET', 'POST'])
@login_required
def tasks(tipo='all'):
    if tipo == 'incompleted':
        tasks = db.session.query(Task).filter_by(user_id=current_user.id, completed=0).all()
    elif tipo == 'completed':
        tasks = db.session.query(Task).filter_by(user_id=current_user.id, completed=1).all()
    else:
        tasks = db.session.query(Task).filter_by(user_id=current_user.id).all()

    for task in tasks:
        task.fecha_inicio = datetime.strptime(task.fecha_inicio, '%Y-%m-%d').strftime('%d/%m/%Y')
        task.fecha_fin = datetime.strptime(task.fecha_fin, '%Y-%m-%d').strftime('%d/%m/%Y')
        
    
    return render_template('tasks.html', tasks=tasks)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = db.session.query(Task).get(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for('index'))
    if isinstance(task.fecha_inicio, str):
        task.fecha_inicio = datetime.strptime(task.fecha_inicio, '%Y-%m-%d')
    if isinstance(task.fecha_fin, str):
        task.fecha_fin = datetime.strptime(task.fecha_fin, '%Y-%m-%d')
        print(task)
    task.completed = int(task.completed)
    form = EditTaskForm(obj=task)
    if form.validate_on_submit():
        form.completed.data = int(form.completed.data)
        form.populate_obj(task)
        db.session.commit()
        try:
            return redirect(url_for('tasks', tipo='all'))
        except Exception as e:
            print(f"Error: {e}")
            raise e
    return render_template('edit_task.html', form=form, task=task)

@app.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = db.session.query(Task).get(task_id)
    if task.user_id != current_user.id:
        return redirect(url_for('index'))
    db.session.delete(task)
    db.session.commit()
    print(task.id)
    return redirect(url_for('tasks', tipo='all'))

@app.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = db.session.query(User).get(user_id)
    if not user:
        return redirect(url_for('index'))

    return render_template('profile.html', user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)