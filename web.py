import uvicorn

from src.infrastructure.config.parse_config import load_config, BASE_DIR
from src.presentation.web.application_build import Director, DevelopmentApplicationBuilder


# from src.utils.gunicorn_app import StandaloneApplication


def run_application() -> None:
    config = load_config(BASE_DIR / "infrastructure" / "config" / "config.yaml")
    director = Director(DevelopmentApplicationBuilder(config=config))
    app = director.build_app()
    uvicorn.run(app=app, host=config.server.host, port=config.server.port)
    # options = {
    #     "bind": "%s:%s" % (config.server.host, config.server.port),
    #     "worker_class": "uvicorn.workers.UvicornWorker",
    #     "reload": True,
    #     "disable_existing_loggers": False,
    #     "preload_app": True,
    # }
    # gunicorn_app = StandaloneApplication(app, options)
    # gunicorn_app.run()


if __name__ == "__main__":
    run_application()
