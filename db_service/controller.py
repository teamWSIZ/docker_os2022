import os

import aiohttp_cors
from aiohttp import web, ClientSession
from aiohttp.abc import BaseRequest

from service import DbService
from dotenv import load_dotenv

routes = web.RouteTableDef()


# query = req.match_info.get('query', '')  # for route-resolving, /{query}
# query = req.rel_url.query['query']  # params; required; else .get('query','default')

def answer(comment: str, status=200):
    return web.json_response({'response': comment}, status=status)

@routes.get('/status')
async def hello(req: BaseRequest):
    return answer('OK')


@routes.get('/users')
async def rootpath(req: BaseRequest):
    return web.json_response(await db().get_all_users())


# INITIATION
app = web.Application()
app.router.add_routes(routes)


def session() -> ClientSession:
    return app['http']


def db() -> DbService:
    return app['db']


#  setup generous CORS:
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})

for route in list(app.router.routes()):
    cors.add(route)


##############
# App creation

async def pre_init():
    load_dotenv()
    print('App initialization..')
    passwd = os.getenv("SOME_PASSWD", None)
    print(f'pass={passwd}')
    app['db'] = DbService()
    await db().initalize()
    app['http'] = ClientSession()
    print('App initalization complete')


async def app_factory():
    await pre_init()
    return app

APP_PORT = 5005
def run_it():
    web.run_app(app_factory(), port=APP_PORT)


run_it()
