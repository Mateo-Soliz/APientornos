from flask_restful import Api, Resource, reqparse
from models import db, Task,User
from flask import jsonify
api = Api()

class TaskApis(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Task', type=str)
        self.parser.add_argument('Description', type=str)
        self.parser.add_argument('fecha_inicio', type=str)
        self.parser.add_argument('fecha_fin', type=str)
        self.parser.add_argument('user_id', type=int)
        self.parser.add_argument('completed', type=bool)
        
    def get(self, task_id='all', completed=''):
        try:
            if task_id=='all':
                if completed == 'true' or completed == 'false':
                    tasks = db.session.query(Task).filter_by(completed=1 if completed == 'true' else 0).all()
                else:
                    tasks = db.session.query(Task).all()
                lista = []
                for task in tasks:
                    lista.append({
                        'id': task.id,
                        'Task': task.Task,
                        'Description': task.Description,
                        'fecha_inicio': task.fecha_inicio,
                        'fecha_fin': task.fecha_fin,
                        'user_id': task.user_id,
                        'completed': task.completed
                    })
                return jsonify(lista)
            else:
                task= Task.query.get_or_404(int(task_id))
                return {
                    'Task': task.Task,
                    'Description': task.Description,
                    'fecha_inicio': task.fecha_inicio,
                    'fecha_fin': task.fecha_fin,
                    'user_id': task.user_id,
                    'completed': task.completed
                }
        except Exception as e:
            return {'error': str(e)}
    def post(self):
        try:
            args = self.parser.parse_args()
            task = Task(Task=args['Task'], Description=args['Description'], fecha_inicio=args['fecha_inicio'], fecha_fin=args['fecha_fin'], user_id=args['user_id'], completed=args['completed'])
            db.session.add(task)
            db.session.commit()
            return {
                'id': task.id,
                'Task': task.Task,
                'Description': task.Description,
                'fecha_inicio': task.fecha_inicio,
                'fecha_fin': task.fecha_fin,
                'user_id': task.user_id,
                'completed': task.completed,
                'push': 'true'
            }
        except Exception as e:
            return {'error': str(e)}
    def put(self, task_id):
        try:
            args = self.parser.parse_args()
            task = Task.query.get_or_404(task_id)
            task.Task = args['Task']
            task.Description = args['Description']
            task.fecha_inicio = args['fecha_inicio']
            task.fecha_fin = args['fecha_fin']
            task.user_id = args['user_id']
            task.completed = args['completed']
            db.session.commit()
            return {
                'Task': task.Task,
                'Description': task.Description,
                'fecha_inicio': task.fecha_inicio,
                'fecha_fin': task.fecha_fin,
                'user_id': task.user_id,
                'completed': task.completed
            }
        except Exception as e:
            return {'error': str(e)}
    def delete(self, task_id):
        try:
            task = Task.query.get_or_404(task_id)
            db.session.delete(task)
            db.session.commit()
            return {'message': 'Task deleted'}
        except Exception as e:
            return {'error': str(e)}
class UserApis(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('first_name', type=str, required=True, help='first_name is required')
        self.parser.add_argument('last_name', type=str, required=True, help='last_name is required')
        self.parser.add_argument('email', type=str, required=True, help='email is required')
        self.parser.add_argument('password', type=str, required=True, help='password is required')
        
    def get(self, user_id='all'):
        try:
            if user_id=='all':
                users = db.session.query(User).all()
                lista = []
                for user in users:
                    lista.append({
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'password': user.password
                    })
                return jsonify(lista)
            else:
                user= User.query.get_or_404(user_id)
            return {
                'id' : user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user.password
            }
        except Exception as e:
            return {'error': str(e)}
    def post(self):
        try:
            args = self.parser.parse_args()
            user = User(first_name=args['first_name'], last_name=args['last_name'], email=args['email'])
            user.set_password(args['password'])
            db.session.add(user)
            db.session.commit()
            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user.password
            }
        except Exception as e:
            return {'error': str(e)}
        
    def put(self, user_id):
        try:
            args = self.parser.parse_args()
            user = db.session.query(User).get_or_404(user_id)
            user.first_name = args['first_name']
            user.last_name = args['last_name']
            user.email = args['email']
            user.update_password(args['password'])
            db.session.commit()
            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'password': user.password
            }
        except Exception as e:
            return {'error': str(e)}
        
    def delete(self, user_id):
        try:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()


            return {'message': 'User deleted'}
        except Exception as e:
            return {'error': str(e)}
    
api.add_resource(TaskApis, '/taskApi/<int:task_id>', '/taskApi', '/taskApi/<string:task_id>/<completed>')
api.add_resource(UserApis, '/userApi/<int:user_id>', '/userApi')


