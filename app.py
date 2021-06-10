from flask import Flask, render_template, request, jsonify
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "https://rhul.buggyrace.net"
current_path = [1]
current_id = [0]


# ------------------------------------------------------------
# validation
# ------------------------------------------------------------
def get_items():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (current_id))

    return dict(zip([column[0] for column in cur.description], cur.fetchone())).items()


def forum_check(data, type): # verification of any type gamerule as well.
    if type == 1:
        if not data.isdigit():
            return "needs a digit not a word/letters, ", 1
    return data, 0


def gather_costs():  # gather the costs here using parsing.
    print("fun")


def calculate_cost():  # compare the costs to the exiting buggy and calc a cost.
    to_check = get_items()
    # costs = gather_costs()
    # print(to_check)
    # for item in to_check:
    # print(item)
    return 20


def database_assign(item, type):  # update an existing database
    data, error = forum_check(request.form[item], type)
    if error == 1:
        msg = item + " " + data
        return msg
    else:
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                cost = calculate_cost()
                cur.execute(
                    f"UPDATE buggies set {item}=?, total_cost=? WHERE id=?",
                    (data, cost, current_id[0])
                )
                con.commit()
                # msg = "Record successfully saved"
                msg = f"value of {item} is now {data}"
        except:
            con.rollback()
            msg = "error in update for" + item
        finally:
            con.close()
            return msg


def database_new(item, type, path):
    data, error = forum_check(path, type)
    if error == 1:
        msg = item + " " + data
        return msg
    else:
        try:
            with sql.connect(DATABASE_FILE) as con:
                cur = con.cursor()
                # cost = calculate_cost()
                cur.execute(
                    f"INSERT INTO buggies ({item}) VALUES (?)",
                    (data))
                con.commit()
                # msg = "Record successfully saved"
                msg = f"value of {item} is now {data}"
        except:
            con.rollback()
            msg = "error in new data for " + item
        finally:
            con.close()
            return msg


def database_remove(id):
    try:
        with sql.connect(DATABASE_FILE) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM buggies WHERE id=?",
                        id)
            con.commit()
            # msg = "Record successfully saved"
            print('hi')
            msg = f"buggy {id} is deleted"
    except:
        con.rollback()
        msg = "error in new data for " + id
    finally:
        con.close()
        return msg


def get_table(type=0):
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    if type == 1:
        cur.execute("SELECT * FROM buggies")
        records = cur.fetchall();
    else:
        cur.execute("SELECT * FROM buggies WHERE id=?", (current_id))
        records = cur.fetchone();
    return records


# ------------------------------------------------------------
# the index page
# ------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)


@app.route('/poster')
def poster():
    return render_template('poster.html')


# ------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
# ------------------------------------------------------------
# @app.route('/new', methods = ['POST', 'GET'])
# def create_buggy():
# return render_template("buggy-form.html", buggy = get_table())

# ------------------------------------------------------------
# a page for displaying the buggy
# ------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
    return render_template("buggy.html", buggies=get_table(1))


# ------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
# ------------------------------------------------------------
@app.route('/user_id', methods=['POST', 'GET'])
def identity_edit():
    if request.method == 'GET':
        return render_template("verify.html", buggy=get_table())
    elif request.method == 'POST':
        id = request.form["id"]
        return render_template("question.html", id=id, buggies=get_table(1))


@app.route('/edit', methods=['POST', 'GET'])
def edit_option():
    if request.method == 'GET':
        return render_template("buggy-form.html", buggy=get_table(), id=current_id[0])
    elif request.method == 'POST':
        id = request.form['id']
        print(id)
        current_path.pop(0)
        current_path.append(1)
        current_id.pop(0)
        current_id.append(id)
        return render_template("buggy-form.html", buggy=get_table(), id=current_id[0])


@app.route('/create', methods=['POST', 'GET'])
def create_option():
    if request.method == 'GET':
        current_path.pop(0)
        current_path.append(0)
        print(decider("4", 'qty_wheels', 1))
        return render_template("updated.html", msg="new buggy has been created feel free to edit it")
    elif request.method == 'POST':
        return render_template("buggy-form.html", buggy=get_table(), id=current_id[0])


@app.route('/delete', methods=['POST', 'GET'])
def delete_option():
    if request.method == 'GET':
        return render_template("updated.html", msg="new buggy has been created feel free to edit it")
    elif request.method == 'POST':
        id = request.form['id']
        msg = database_remove(id)
        return render_template("updated.html", msg=msg)


def decider(path, item, type):
    if path == 1:
        return database_assign(item, type)
    else:
        return database_new(item, type, path)


@app.route('/warfare', methods=['POST', 'GET'])
def warfare_edit():
    if request.method == 'GET':
        return render_template("buggy-form-warfare.html", buggy=get_table())
    elif request.method == 'POST':
        msg = ""
        # warfare
        path = current_path[0]
        armour = decider(path, 'armour', 0)
        attack = decider(path, 'attack', 0)
        qty_attacks = decider(path, 'qty_attacks', 1)
        fireproof = decider(path, 'fireproof', 0)
        insulated = decider(path, 'insulated', 0)
        antibiotic = decider(path, 'antibiotic', 0)
        banging = decider(path, 'banging', 0)
        algo = decider(path, 'algo', 0)

        return render_template("updated.html", msg=armour, msg2=attack, msg3=qty_attacks, msg4=fireproof,
                               msg5=insulated, msg6=antibiotic, msg7=banging, msg8=algo)


@app.route('/wheel', methods=['POST', 'GET'])
def wheel_edit():
    if request.method == 'GET':
        return render_template("buggy-form-wheel.html", buggy=get_table())
    elif request.method == 'POST':
        msg = ""
        # wheels
        path = current_path[0]
        qty_wheels = decider(path, 'qty_wheels', 1)
        tyres = decider(path, 'tyres', 0)
        qty_tyres = decider(path, 'qty_tyres', 1)

        return render_template("updated.html", msg=qty_wheels, msg2=tyres, msg3=qty_tyres)


@app.route('/power', methods=['POST', 'GET'])
def power_edit():
    if request.method == 'GET':
        return render_template("buggy-form-power.html", buggy=get_table())
    elif request.method == 'POST':
        msg = ""
        # power
        path = current_path[0]
        power_type = decider(path, 'power_type', 0)
        power_units = decider(path, 'power_units', 1)
        aux_power_type = decider(path, 'aux_power_type', 0)
        aux_power_units = decider(path, 'aux_power_units', 1)
        hamster_booster = decider(path, 'hamster_booster', 1)

        return render_template("updated.html", msg=power_type, msg2=power_units, msg3=aux_power_type,
                               msg4=aux_power_units, msg5=hamster_booster)


@app.route('/flag', methods=['POST', 'GET'])
def flag_edit():
    if request.method == 'GET':
        return render_template("buggy-form-flag.html", buggy=get_table())
    elif request.method == 'POST':
        msg = ""
        # flag
        path = current_path[0]
        flag_color = decider(path, 'flag_color', 0)
        flag_pattern = decider(path, 'flag_pattern', 0)
        flag_color_secondary = decider(path, 'flag_color_secondary', 0)

        return render_template("updated.html", msg=flag_color, msg2=flag_pattern, msg3=flag_color_secondary)


# ------------------------------------------------------------
# You probably don't need to edit this... unless you want to ;)
#
# get JSON from current record
#  This reads the buggy record from the database, turns it
#  into JSON format (excluding any empty values), and returns
#  it. There's no .html template here because it's *only* returning
#  the data, so in effect jsonify() is rendering the data.
# ------------------------------------------------------------

@app.route('/json')
def summary():
    buggies = get_items()
    return jsonify({key: val for key, val in buggies if (val != "" and val is not None)})


# You shouldn't need to add anything below this!
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
