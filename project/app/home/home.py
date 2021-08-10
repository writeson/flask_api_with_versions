from flask import render_template, flash
from logging import getLogger
from . import home_bp

logger = getLogger(__file__)


@home_bp.get("/")
def home():
    logger.debug("rendering home page")
    return render_template("index.html")


@home_bp.get("/about")
def about():
    logger.debug("rendering about page")
    return render_template("about.html")
