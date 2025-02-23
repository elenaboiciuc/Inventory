from app import create_app, db

# create an instance of the Flask app
app = create_app()

with app.app_context():
     db.create_all() # create all database tables defined by the models in the application

if __name__ == "__main__":
    app.run(debug=True)