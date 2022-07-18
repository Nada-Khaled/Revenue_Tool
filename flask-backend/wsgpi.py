from app import flaskApp
if __name__ == "__main__":
    flaskApp.run(host='0.0.0.0',debug=True,use_reloader=True)
    # flaskApp.run(host='0.0.0.0',port=6000,debug=True,use_reloader=True)