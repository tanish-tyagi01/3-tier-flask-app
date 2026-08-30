from app import app, db, Todo, User

'''with app.app_context():
    user = User.query.get(1)
    for todo in user.todos:
        print(todo.task)


    todo = Todo.query.get(2)
    print(todo.user.name) # here relationship(backref = user) use hua hai jiski vjh se hm user to access kr pa rhe hai'''

with app.app_context():
    users = User.query.all()
    for user in users:
        print("User: ", user.name)

        for todo in user.todos:
            print(" Task:", todo.task)