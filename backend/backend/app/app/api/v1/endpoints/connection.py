from fastapi import APIRouter
from collections import defaultdict
from app.database import  get_db_connection, release_db_connection

router = APIRouter()

def sortConnection(start, end, connections):
    movies = []
    actors = []
    actors_map = defaultdict(list)
    for index, connection in enumerate(connections):
        actors_map[connection[0]].append(index)
        actors_map[connection[1]].append(index)
    actors.append(start)
    visited_index = []
    while actors[-1] != end:
        for index in actors_map[actors[-1]]:
            if index not in visited_index:
                visited_index.append(index)
                if connections[index][0] == actors[-1]:
                    actors.append(connections[index][1])
                    movies.append(connections[index][2])
                
    return {'movies': movies, 'actors': actors}

@router.get("/connection")
def getSixDegrees(start: str, end: str):
    cursor = get_db_connection()
    query = (
            "WITH actor_ids AS (\n"
            "        SELECT\n"
            "            id,\n"
            "            primaryname\n"
            "        FROM\n"
            "            actors_perita\n"
            "        WHERE\n"
            "            primaryname IN ('{start}', '{end}')\n"
            "    ),\n"
            "    actor_path AS (\n"
            "        SELECT\n"
            "            source.id AS source_id,\n"
            "            target.id AS target_id\n"
            "        FROM\n"
            "            actor_ids AS source\n"
            "        CROSS JOIN\n"
            "            actor_ids AS target\n"
            "        WHERE\n"
            "            source.primaryname = '{start}' AND target.primaryname = '{end}'\n"
            "    ),\n"
            "    path_actors AS (\n"
            "        SELECT\n"
            "            dj.seq,\n"
            "            dj.node AS actor_id,\n"
            "            actors_perita.primaryname\n"
            "        FROM\n"
            "            actor_path,\n"
            "            pgr_dijkstra(\n"
            "                'SELECT * FROM dijkstra',\n"
            "                (SELECT source_id FROM actor_path),\n"
            "                (SELECT target_id FROM actor_path),\n"
            "                false\n"
            "            ) AS dj\n"
            "        JOIN\n"
            "            actors_perita ON dj.node = actors_perita.id\n"
            "    ),\n"
            "    actor_pairs AS (\n"
            "        SELECT\n"
            "            pa1.actor_id AS actor1_id,\n"
            "            pa2.actor_id AS actor2_id,\n"
            "            pa1.primaryname AS actor1_primaryname,\n"
            "            pa2.primaryname AS actor2_primaryname\n"
            "        FROM\n"
            "            path_actors pa1\n"
            "        JOIN\n"
            "            path_actors pa2 ON pa1.seq + 1 = pa2.seq\n"
            "    ),\n"
            "    movies_between_pairs AS (\n"
            "        SELECT\n"
            "            ap.actor1_id,\n"
            "            ap.actor2_id,\n"
            "            ap.actor1_primaryname,\n"
            "            ap.actor2_primaryname,\n"
            "            movies_perita.*\n"
            "        FROM\n"
            "            actor_pairs ap\n"
            "        JOIN\n"
            "            relationships_perita rp1 ON ap.actor1_id = rp1.actor_id\n"
            "        JOIN\n"
            "            relationships_perita rp2 ON ap.actor2_id = rp2.actor_id\n"
            "        JOIN\n"
            "            movies_perita ON rp1.movie_id = movies_perita.id AND rp1.movie_id = rp2.movie_id\n"
            "    )\n"
            "    SELECT\n"
            "        mbp.actor1_primaryname,\n"
            "        mbp.actor2_primaryname,\n"
            "        mbp.title AS movie_title\n"
            "    FROM\n"
            "        movies_between_pairs mbp\n"
            "    ORDER BY\n"
            "        mbp.actor1_id, mbp.actor2_id;\n"
        ).format(start=start, end=end)
    cursor.execute(query)

    data = sortConnection(start, end, cursor.fetchall())
    release_db_connection(cursor)

    return data

@router.get("/actors/{name}")
def getActors(name: str):
    cursor = get_db_connection()
    query = ("SELECT primaryname FROM actors_perita WHERE primaryname LIKE '%{name}%' ORDER BY id ASC LIMIT 5;").format(name=name)
    cursor.execute(query)
    data = cursor.fetchall()
    release_db_connection(cursor)

    return data