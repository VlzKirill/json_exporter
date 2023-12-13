from flask import Flask, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest, make_wsgi_app
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from json_parser import process_folder
from prometheus_client.registry import Collector
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

benchmarks = process_folder()[0]
build_number = process_folder()[2]


class CustomCollector(Collector):

    def collect(self):
        for key, value in benchmarks.items():
            yield GaugeMetricFamily(key, f'Algorithm {key} bytes per second', value=value)
        yield GaugeMetricFamily("build_number", "Build number of libacm benchmarks", value=build_number)


REGISTRY.register(CustomCollector())


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == "__main__":
    app.run(debug=True)
