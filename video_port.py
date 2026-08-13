from src import create_app

app = create_app(device_type="pi")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
