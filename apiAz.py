from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_apispec import MethodResource, doc, use_kwargs, marshal_with
from apispec import APISpec
from marshmallow import Schema
from marshmallow.fields import String, Integer
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

app = Flask(__name__)
api = Api(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='REST API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

images_post_args = reqparse.RequestParser()
images_post_args.add_argument('nombre', type = str, help = 'El nombre es requerido', required = True)
images_post_args.add_argument('formato', type = str, help = 'El formato es requerido', required = True)
images_post_args.add_argument('size', type = int, help = 'El tamaño es requerido', required = True)

images = {}

def abort_if_image_exist(image_id):
    if image_id in images:
        abort(409, message = 'Imagen existente')

def abort_if_image_doesnt_exist(image_id):
    if image_id not in images:
        abort(404, massege = 'No se encuentra la imagen')

class BodySchema(Schema):
    id = Integer()
    nombre = String()
    formato = String()
    size = Integer()

class AzureStorage(Resource, MethodResource):
    # características de funcionamiento
    @doc(description='GET HTTP en mi API.', tags=['AzureStorage'])
    def get(self, image_id):
        # Método GET
        abort_if_image_doesnt_exist(image_id)
        return images[image_id]

    @doc(description='POST HTTP en mi API.', tags=['AzureStorage'])
    @use_kwargs(BodySchema)
    def post(self, image_id):
        # Método POST
        abort_if_image_exist(image_id)
        args = images_post_args.parse_args()
        images[image_id] = args
        return images[image_id], 201

api.add_resource(AzureStorage, '/Storage/<int:image_id>')

docs.register(AzureStorage)


# El codigo sólo se va a ejecutar cuando se ejecute directamente y no desde otro archivo
if __name__ == '__main__':
    app.run(debug=True)


"""
    @app.route('/')
    def helloworld():
        return {'data': 'Hello World'}

    if __name__ == '__main__':
        app.run(debug=True)
"""