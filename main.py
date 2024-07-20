from Filler_robot.main import filler
from Filler_interface.app import app
from Raspberry.input import input_request


if __name__ == '__main__':
    app.run()
    filler.start()
    input_request.start()
