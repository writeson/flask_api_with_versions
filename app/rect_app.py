from app import create_app

app = create_app()
app.logger.info("Rect App is running")