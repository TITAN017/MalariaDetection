from server import create_app
from flask_executor import Executor
from flask_mail import Mail,Message
app = create_app()

if __name__ == '__main__':
    executor = Executor(app)
    app.run(host="0.0.0.0",debug=True)