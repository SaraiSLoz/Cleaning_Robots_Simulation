import flask
from flask.json import jsonify
import uuid
from botLimpiador import Maze, Bot, Garbage, Incinerator
games = {}

app = flask.Flask(__name__)


@app.route("/games", methods=["POST"])
def create():
    global games
    id = str(uuid.uuid4())
    games[id] = Maze()
    botlist = []
    garblist = []
    inclist = []
    for agent in games[id].schedule.agents:
        if isinstance(agent, Bot):
            botlist.append(
                {"id": agent.unique_id, "x": agent.pos[0], "z": agent.pos[1]})
        elif isinstance(agent, Garbage) and agent.pos is not None:
            garblist.append(
                {"id": agent.unique_id, "x": agent.pos[0], "z": agent.pos[1]})
        elif isinstance(agent, Incinerator):
            inclist.append(
                {"id": agent.unique_id,
                    "x": agent.pos[0], "z": agent.pos[1], "condition": agent.condition}
            )

    # response = flask.make_response()
    # response.headers['Location'] = f"/games/{id}"
    # response.status_code = 201
    # response.data = jsonify(lista)
    # return response

    agentlist = [botlist, garblist, inclist]
    return jsonify(agentlist), 201, {'Location': f"/games/{id}"}


@app.route("/games/<id>", methods=["GET"])
def queryState(id):
    global model
    model = games[id]
    model.step()
    botlist = []
    garblist = []
    inclist = []
    for agent in games[id].schedule.agents:
        if isinstance(agent, Bot):
            botlist.append(
                {"id": agent.unique_id, "x": agent.pos[0], "z": agent.pos[1]})
        elif isinstance(agent, Garbage) and agent.pos is not None:
            garblist.append(
                {"id": agent.unique_id, "x": agent.pos[0], "z": agent.pos[1]})
        elif isinstance(agent, Incinerator):
            inclist.append(
                {"id": agent.unique_id,
                    "x": agent.pos[0], "z": agent.pos[1], "condition": agent.condition}
            )
    agentlist = [botlist, garblist, inclist]
    return jsonify(agentlist), 201, {'Location': f"/games/{id}"}


app.run(port=5100)
