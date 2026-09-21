from flask import Blueprint
from flask import render_template



home_bp = Blueprint(
    "home",
    __name__
)


@home_bp.route("/")
def home():

    stats = {
        "images": 0,
        "documents": 0,
        "music": 0,
        "videos": 0,
        "installers": 0,
        "others": 0
    }

    return render_template(
        "index.html",
        stats=stats
    )