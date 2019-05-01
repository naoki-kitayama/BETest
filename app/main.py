import responder

api = responder.API()

@api.route("/")
def hello_world(req, resp):
	resp.text = "Happy new era!"

if __name__ == '__main__':
	api.run(address="0.0.0.0",port=80)

