from aiohttp import web
from app.controller import LogsController
import app.db


async def health(request):
    return web.json_response({'status': True})


async def create_log(request):
    async with request.app['db'].acquire() as conn:
        data = await request.post()  # form data
        await LogsController(conn).post_log(data.get('text'))
        return web.json_response({"status": "created"})


async def get_logs_list(request):
    async with request.app['db'].acquire() as conn:
        try:
            logs = await LogsController(conn).get()
            return web.json_response({
                'logs': logs,
            })
        except app.db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))


async def get_item(request):
    log_id = request.match_info['log_id']
    async with request.app['db'].acquire() as conn:
        try:
            log = await LogsController(conn).get_by_id(log_id)
            return web.json_response(log)
        except app.db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))


async def delete_item(request):
    log_id = request.match_info['log_id']
    async with request.app['db'].acquire() as conn:
        try:
            await LogsController(conn).delete_by_id(log_id)
            return web.json_response(None, status=204)
        except app.db.RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))
