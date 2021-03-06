from PySide6.QtCore import QThread


class FlaskThread(QThread):
    def __init__(self, app, listen_port):
        QThread.__init__(self)
        self.app = app
        self.listen_port = listen_port

    def run(self):
        print(self.listen_port)
        self.app.run(host='127.0.0.1', port=int(self.listen_port))

