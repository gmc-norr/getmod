import sys
import flask
from PySide6.QtCore import Qt, QTimer, QSettings, QThread, QRegularExpression
from PySide6.QtGui import QIcon, QAction, QPixmap, QIntValidator, QRegularExpressionValidator
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, \
    QLabel, QWidgetAction, QWidget, QHBoxLayout, QMessageBox, QFormLayout, QLineEdit, QPushButton

import qdarktheme

from modules.flaskapp import FlaskThread

from flask import Flask, request
import requests
import resources
from urllib import parse

__version__ = "0.1.0"


class IconLabel(QWidget):

    HorizontalSpacing = -2

    def __init__(self, text):
        super(IconLabel, self).__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(2, 0, 0, 0)
        self.setLayout(layout)

        image_label = QLabel()
        image_label.setPixmap(QPixmap(":/icons/feather/life-buoy.svg").scaledToWidth(15))
        # image_label.setText(text)
        image_label.setMaximumWidth(20)
        image_label.setMaximumHeight(25)
        layout.addWidget(image_label)
        layout.addSpacing(self.HorizontalSpacing)
        label = QLabel(text)
        label.setStyleSheet("QLabel {background: rgba(41.000, 42.000, 45.000, 1.000)}")
        layout.addWidget(label)


class ButtonLabel(QWidget):

    horizontal_spacing = 0

    def __init__(self):
        super(ButtonLabel, self).__init__()

        style = """
            QPushButton {
                background-color: darkred;
            }
            
            QPushButton:checked {
                background-color: green;
            }

        """

        layout = QHBoxLayout()
        layout.setContentsMargins(1, 5, 8, 5)
        self.setLayout(layout)

        self.button = QPushButton()
        self.button.setText("OFF")
        self.button.setCheckable(True)
        self.button.setMinimumWidth(60)
        self.button.setStyleSheet(style)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.on_click)

    def on_click(self):
        if self.button.isChecked():
            self.button.setText("ON")
        else:
            self.button.setText("OFF")


class LabelEdit(QWidget):

    HorizontalSpacing = 2

    def __init__(self, label_txt, key, settings):
        super(LabelEdit, self).__init__()

        self.key = key
        self.settings = settings
        value = self.settings.value(key)

        layout = QFormLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        self.setLayout(layout)

        label = QLabel(label_txt)
        label.setMinimumWidth(70)

        self.edit = QLineEdit()
        self.edit.setValidator(self.get_validator())
        self.edit.setText(value)
        self.edit.setMaximumWidth(70)

        layout.addRow(label, self.edit)

        self.edit.textChanged.connect(self.on_change)

    def get_validator(self):
        if self.key == "institution":
            rx = QRegularExpression()
            rx.setPattern("[A-Z]{3}\\d{4}")
            return QRegularExpressionValidator(rx, self)
        else:
            return QIntValidator()

    def on_change(self):
        value = self.edit.text()
        self.settings.setValue(self.key, value)


class SysTrayApp:

    status_desc = {
        100: 'Continue',
        101: 'Switching Protocols',
        102: 'Processing',
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non-authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        206: 'Partial Content',
        207: 'Multi-Status',
        208: 'Already Reported',
        226: 'IM Used',
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        307: 'Temporary Redirect',
        308: 'Permanent Redirect',
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Payload Too Large',
        414: 'Request-URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Requested Range Not Satisfiable',
        417: 'Expectation Failed',
        418: 'Im a teapot',
        421: 'Misdirected Request',
        422: 'Unprocessable Entity',
        423: 'Locked',
        424: 'Failed Dependency',
        426: 'Upgrade Required',
        428: 'Precondition Required',
        429: 'Too Many Requests',
        431: 'Request Header Fields Too Large',
        444: 'Connection Closed Without Response',
        451: 'Unavailable For Legal Reasons',
        499: 'Client Closed Request',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported',
        506: 'Variant Also Negotiates',
        507: 'Insufficient Storage',
        508: 'Loop Detected',
        510: 'Not Extended',
        511: 'Network Authentication Required',
        599: 'Network Connect Timeout Error'
    }

    def __init__(self, app):
        self.app = app
        self.settings = QSettings("Region Västerbotten", "getmod")

        self.thread = QThread()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_flask_status)

        self.tray = QSystemTrayIcon(QIcon(":/icons/feather/life-buoy.svg"), self.app)
        self.menu = QMenu()
        self.menu.setMinimumWidth(80)
        self.menu.setContentsMargins(10, 2, 2, 2)

        header = IconLabel("- GetMod " + __version__ + " -")
        header.setStyleSheet("margin-left: 0px; margin-top: 0px; margin-bottom: 5px")
        header_action = QWidgetAction(self.menu)
        header_action.setDefaultWidget(header)
        self.menu.addAction(header_action)

        self.action_onoff = ButtonLabel()
        action_onoff = QWidgetAction(self.menu)
        action_onoff.setDefaultWidget(self.action_onoff)
        self.menu.addAction(action_onoff)
        self.action_onoff.button.clicked.connect(self.onoff_clicked)

        self.submenu_settings = self.menu.addMenu("Settings")
        self.submenu_settings.setMaximumWidth(200)
        listen = LabelEdit("Listen port", "listen_port", self.settings)
        listen_action = QWidgetAction(self.submenu_settings)
        listen_action.setDefaultWidget(listen)
        self.submenu_settings.addAction(listen_action)

        target = LabelEdit("Target port", "target_port", self.settings)
        target_action = QWidgetAction(self.submenu_settings)
        target_action.setDefaultWidget(target)
        self.submenu_settings.addAction(target_action)

        apikey = LabelEdit("API key", "apikey", self.settings)
        apikey_action = QWidgetAction(self.submenu_settings)
        apikey_action.setDefaultWidget(apikey)
        self.submenu_settings.addAction(apikey_action)

        instutution = LabelEdit("Institution", "institution", self.settings)
        instutution_action = QWidgetAction(self.submenu_settings)
        instutution_action.setDefaultWidget(instutution)
        self.submenu_settings.addAction(instutution_action)

        self.action_exit = QAction("Exit")
        self.action_exit.triggered.connect(self.exit)
        self.menu.addAction(self.action_exit)

        self.tray.setToolTip("GetMod - get request modifier")
        self.tray.setContextMenu(self.menu)
        self.tray.setVisible(True)
        self.tray.show()

        self.app.setStyleSheet(qdarktheme.load_stylesheet())

        sys.exit(self.app.exec())

    def exit(self):
        self.thread.terminate()
        self.thread.wait()
        self.tray.hide()
        self.app.exit()

    def check_flask_status(self):
        if not self.thread.isRunning():
            self.action_onoff.setChecked(False)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setWindowIcon(QIcon(":/icons/feather/life-buoy.svg"))
            msgBox.setWindowTitle("Critical Error")
            msgBox.setText("Houston, the flask server did not start!")
            msgBox.exec()

    def onoff_clicked(self):
        if self.action_onoff.button.isChecked():
            self.start_flask()
        else:
            self.thread.terminate()
            print("Flask off!")

    def start_flask(self):
        apikey = self.settings.value('apikey')
        institution = self.settings.value('institution')
        listen_port = self.settings.value('listen_port')
        relay_port = self.settings.value('relay_port')

        flask_app = self.create_flask_app(apikey, institution, relay_port, self.status_desc)

        self.thread = FlaskThread(flask_app, listen_port)
        self.thread.start()
        self.timer.singleShot(1000, self.check_flask_status)

    @staticmethod
    def create_flask_app(apikey, institution, relay_port, status_desc):

        site_relay = "http://localhost:" + str(relay_port)

        def args2str(args):
            dlist = list()
            for key, value in args.items():
                _str = f"{key}={value}"
                dlist.append(_str)

            return "&".join(dlist)

        flask_app = Flask(__name__)

        # @flask_app.route('/', defaults={'path': ''})
        @flask_app.route('/<path:path>', methods=['GET'])
        def proxy(path):

            def get_mod_path(request: flask.request, apikey, institution):
                args = request.args.to_dict()
                request_path = request.path
                outdata = {}
                outdata['apikey'] = apikey
                outdata['institution'] = institution

                for key in args:
                    value = args[key]
                    if key == "request":
                        if value.startswith('BAM<'):
                            new_key1 = "path"
                            new_value1 = "file:///" + value.lstrip('BAM<')
                            new_key2 = "filetype"
                            new_value2 = "bam"

                            outdata[new_key1] = new_value1.replace('\\', "/")
                            outdata[new_key2] = new_value2
                            request_path = "open"
                        else:
                            outdata[key] = value
                            request_path = "search"

                return request_path, args2str(outdata)

            def error_response(e, site_relay, new_path):
                return f"<html><head></head><body><h1>Communication error!</h1>" \
                       f"<p>Exception msg:      {e}</p>" \
                       f"<p>Target (host:port): {site_relay}</p>" \
                       f"<p>Get request:        {new_path}</p>" \
                       f"</body></html>"

            if request.method == "GET" and request.path != "/favicon.ico":

                req_path, argstr = get_mod_path(request, apikey, institution)

                encoded_argstr = parse.quote(argstr, safe='&=')

                encoded_request = f'{site_relay}/{req_path}?{encoded_argstr}'

                print(encoded_request)
                print(argstr)

                try:
                    ret = requests.get(encoded_request, timeout=10)

                    status = int(ret.status_code)

                    if status in range(200, 300):
                        header = "Success!"
                    else:
                        header = "Problem!"

                    return f"<html><head></head><body><h1>{header}</h1>" \
                           f"<p>Target status code: {ret.status_code} {status_desc[status]}</p>" \
                           f"<p>Target (host:port):   {site_relay}</p>" \
                           f"<p>Get request:          {encoded_argstr}</p>" \
                           "</body></html>"

                except requests.exceptions.HTTPError as errh:
                    e = "Http Error: " + str(errh)
                    return error_response(e, site_relay, encoded_argstr)

                except requests.exceptions.ConnectionError as errc:
                    e = "Error Connecting: " + str(errc)
                    return error_response(e, site_relay, encoded_argstr)

                except requests.exceptions.Timeout as errt:
                    e = "Error Connecting: " + str(errt)
                    return error_response(e, site_relay, encoded_argstr)

                except requests.exceptions.RequestException as err:
                    e = "Error Connecting: " + str(err)
                    return error_response(e, site_relay, encoded_argstr)

            return f"<html><head></head><body><h1>Something's wrong!</h1>" \
                   f"<p>No errors detected but no valid response from target either ... </p>" \
                   f"</body></html>"

        return flask_app


if __name__ == "__main__":
    app = QApplication(sys.argv)
    tray = SysTrayApp(app)
    sys.exit(app.exec())

