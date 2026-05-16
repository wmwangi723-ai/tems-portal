from app import create_app

# Instantiate the app using the factory pattern
app = create_app()

if __name__ == '__main__':
    # debug=True is crucial for local development. 
    app.run(debug=True, port=5000)