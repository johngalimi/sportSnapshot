import psycopg2 as db
from flask import Flask, jsonify, request

app = Flask(__name__)


def execute_query(query):

    connection = db.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="host.docker.internal",
        port="5432",
    )

    cursor = connection.cursor()
    cursor.execute(query)

    column_names = [desc[0] for desc in cursor.description]

    query_result = [dict(zip(column_names, record)) for record in cursor]

    connection.close()
    cursor.close()

    return query_result


@app.route("/")
def index():
    return jsonify({"app": "Sports Snapshot Service"})


@app.route("/performance")
def rankings():

    league, season = (
        request.args.get("league"),
        request.args.get("season"),
    )

    query = f"""
        SELECT
            CONCAT(team.team_location, ' ', team.team_name) as team,
            SUM(CASE WHEN game.team_points > game.opponent_points THEN 1 ELSE 0 END) wins,
            SUM(CASE WHEN game.team_points < game.opponent_points AND game.is_overtime IS FALSE THEN 1 ELSE 0 END) losses,
            SUM(CASE WHEN game.team_points < game.opponent_points AND game.is_overtime IS TRUE THEN 1 ELSE 0 END) ot_losses
        FROM tblGameRaw game
        INNER JOIN tblTeam team ON game.team_id = team.id
        INNER JOIN tblLeague league ON team.league_id = league.id
        WHERE league.league_abbr = '{league}'
            AND game.game_season = '{season}'
        GROUP BY team
        ORDER BY wins DESC
    """

    query_result = execute_query(query)

    return jsonify(query_result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
