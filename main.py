import json
import sqlite3
import flask

app = flask.Flask(__name__)

def get_value_from_db(sql):
    with sqlite3.connect("netflix (9).db") as connection:
        connection.row_factory = sqlite3.Row


        result = connection.execute(sql).fetchall()

        return result

def get_value_by_title(title):
    sql = f'''select title, country, release_year, listed_in as genre, description
    where title ='{title}'
    order by release_year desc
    limit 1 
    '''

    result = get_value_from_db(sql)

    for item in result:
        print(dict(item))

@app.get("/movie/<title>")
def view_title(title):
    result = get_value_by_title(title)
    return app.response_class(
        response=json.dumps(result,
                            ensure_ascii=False,
                            indent=4
                            ),
        status=200,
        mimetype="application/json"

    )

@app.get("/movie/<int:year1>/to/<int:year2>")
def get_by_date(year1, year2):
    sql = f'''
           select title, release_year from netflix
           where release_year between '{year1}' and '{year2}'
           limit 100'''
    result = get_value_from_db(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))

    return app.response_class(
        response=json.dumps(item,
                            ensure_ascii=False,
                            indent=4
                            ),
        status=200,
        mimetype="application/json"

    )

@app.get("/rating/<rating>")
def get_by_rating(rating):
    my_dict = {
        "children": ("G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }

    sql = f'''
           select * from netflix(9)
           where rating in {my_dict.get(rating, ("G", "NC-17"))}'''
    result = get_value_from_db(sql)
    tmp = []
    for item in result:
        tmp.append(dict(item))

    return  app.response_class(
        response=json.dumps(tmp,
                            ensure_ascii=False,
                            indent=4
                            ),
        status=200,
        mimetype="application/json"

    )

@app.get("/genre/<genre>")
def get_by_genre(genre):
    sql = f'''
           select title, description, listed_in from netflix
           where listed_in like '%{str(genre)[1:]}%' '''

    result = get_value_from_db(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))

    return  app.response_class(
        response=json.dumps(tmp,
                            ensure_ascii=False,
                            indent=4
                            ),
        status=200,
        mimetype="application/json"

    )

def stop_5(name1="Rose Mclver", name2="Ben Lamb"):
    sql = f'''
          select * from netflix
          where "cast" like '%{name1} and "cast" like '%{name2}'''
    result = get_value_from_db(sql)

    tmp =[]
    names_dic = {}
    for item in result:
        names = set(dict(item).get("cast").split(", ")) - set([name1, name2])
        for name in names:
            names_dic[name.strip()] = names_dic.get(name.strip(), 0) + 1

    print(names_dic)
    for key, value in names_dic.items():
        if value > 2:
            tmp.append(key)

    return tmp

def step_6(typ, year, genre):
    sql = f'''
          select * from netflix
          where type = '{typ}' and
          release_year = '{year}' and
          listed_in like '%{genre}%' '''

    result = get_value_from_db(sql)

    tmp = []
    for item in result:
        tmp.append(dict(item))

    return json.dumps(tmp,
                      ensure_ascii=False,
                      indent=4
                      )



if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)

print(step_6(typ='TV Show', year=2020, genre='Dramas'))