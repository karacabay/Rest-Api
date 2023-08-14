from application import app
import json


if __name__ == '__main__':

    with open('config.json', 'r') as fp:
        server_cfg = json.load(fp)["ServerConfig"]

    app.run(debug=True, 
            host=server_cfg['Host'], 
            port=server_cfg['Port'])