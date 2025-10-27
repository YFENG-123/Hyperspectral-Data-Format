from presenters import Presenters
from views import Views
from models import Models


class App:
    def __init__(self):
        self.views = Views()
        self.models = Models()
        self.presenters = Presenters(self.views, self.models)

    def run(self):
        self.views.run()

    def quit(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()
