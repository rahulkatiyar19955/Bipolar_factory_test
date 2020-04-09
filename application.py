from project import app

# app.config['SECRET_KEY'] = 'MY_SECRET_KEY'

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)