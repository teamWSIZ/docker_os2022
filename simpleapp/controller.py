from aiohttp import web
routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
	return web.json_response({'comment': f'hello!'})

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=5000)

