from app import create_app, db
from app.models import seed_defaults

app = create_app()


@app.cli.command("init-db")
def init_db():
    """Create database tables and seed the default admin."""
    db.create_all()
    seed_defaults()
    print("Database initialized.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_defaults()
    app.run(debug=True)

