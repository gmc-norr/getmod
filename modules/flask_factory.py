import requests
import flask
from urllib import parse


def create_flask_app(apikey, institution, target_port, status_desc):

    target = "http://localhost:" + str(target_port)
    print(target)

    def args2str(args):
        dlist = list()
        for key, value in args.items():
            _str = f"{key}={value}"
            dlist.append(_str)

        return "&".join(dlist)

    flask_app = flask.Flask(__name__)

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

        def error_response(error_msg, target, new_path):
            return f"<html><head></head><body><h1>Communication error!</h1>" \
                   f"<p>Exception msg:      {error_msg}</p>" \
                   f"<p>Target (host:port): {target}</p>" \
                   f"<p>Get request:        {new_path}</p>" \
                   f"</body></html>"

        if flask.request.method == "GET" and flask.request.path != "/favicon.ico":

            req_path, argstr = get_mod_path(flask.request, apikey, institution)

            encoded_argstr = parse.quote(argstr, safe='&=')

            encoded_request = f'{target}/{req_path}?{encoded_argstr}'

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
                       f"<p>Target (host:port):   {target}</p>" \
                       f"<p>Get request:          {encoded_argstr}</p>" \
                       "</body></html>"

            except requests.exceptions.HTTPError as errh:
                e = "Http Error: " + str(errh)
                return error_response(e, target, encoded_argstr)

            except requests.exceptions.ConnectionError as errc:
                e = "Error Connecting: " + str(errc)
                return error_response(e, target, encoded_argstr)

            except requests.exceptions.Timeout as errt:
                e = "Error Connecting: " + str(errt)
                return error_response(e, target, encoded_argstr)

            except requests.exceptions.RequestException as err:
                e = "Error Connecting: " + str(err)
                return error_response(e, target, encoded_argstr)

        return f"<html><head></head><body><h1>Something's wrong!</h1>" \
               f"<p>No errors detected but no valid response from target either ... </p>" \
               f"</body></html>"

    return flask_app