# -*- coding: utf-8 -*-
from core.server import create_app


app = create_app()


if __name__ == '__main__':
    import uvicorn
    # 输出所有的路由
    for route in app.routes:
        if hasattr(route, 'methods'):
            print({'path': route.path, 'name': route.name, 'methods': route.methods})
    uvicorn.run(app='main:app', host='127.0.0.1', port=80, reload=True)
