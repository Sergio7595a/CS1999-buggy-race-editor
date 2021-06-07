from flask import Flask, render_template, request, jsonify
import sqlite3 as sql

# app - The flask application where all the magical things are configured.
app = Flask(__name__)

# Constants - Stuff that we need to know that won't ever change!
DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
BUGGY_RACE_SERVER_URL = "https://rhul.buggyrace.net"


# ------------------------------------------------------------
# validation
# ------------------------------------------------------------
def get_items():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))

    return dict(zip([column[0] for column in cur.description], cur.fetchone())).items()


def forum_check(data, type):
    if type == 1:
        if not data.isdigit():
            return "needs a digit not a word/letters, ", 1
    return data, 0


def gather_costs():
    print("fun")


def calculate_cost():
    to_check = get_items()
    # costs = gather_costs()
    # print(to_check)
    # for item in to_check:
    # print(item)
    return 20


def database_assign(item, type):
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
                    (data, cost, DEFAULT_BUGGY_ID)
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


def get_table():
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone();
    return record


# ------------------------------------------------------------
# the index page
# ------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)


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
    return render_template("buggy.html", buggy=get_table())


# ------------------------------------------------------------
# a placeholder page for editing the buggy: you'll need
# to change this when you tackle task 2-EDIT
# ------------------------------------------------------------
def edit_buggy(module):
    return render_template(module, buggy=get_table())


@app.route('/edit')
def show_option():
    return edit_buggy("buggy-form.html")


@app.route('/warfare', methods=['POST', 'GET'])
def warfare_edit():
    if request.method == 'GET':
        return edit_buggy("buggy-form-warfare.html")
    elif request.method == 'POST':
        msg = ""
        # warfare
        armour = database_assign('armour', 0)
        attack = database_assign('attack', 0)
        qty_attacks = database_assign('qty_attacks', 1)
        fireproof = database_assign('fireproof', 0)
        insulated = database_assign('insulated', 0)
        antibiotic = database_assign('antibiotic', 0)
        banging = database_assign('banging', 0)
        algo = database_assign('algo', 0)

        return render_template("updated.html", msg=armour, msg2=attack, msg3=qty_attacks, msg4=fireproof,
                               msg5=insulated, msg6=antibiotic, msg7=banging, msg8=algo)


@app.route('/wheel', methods=['POST', 'GET'])
def wheel_edit():
    if request.method == 'GET':
        return edit_buggy("buggy-form-wheel.html")
    elif request.method == 'POST':
        msg = ""
        # wheels
        qty_wheels = database_assign('qty_wheels', 1)
        tyres = database_assign('tyres', 0)
        qty_tyres = database_assign('qty_tyres', 1)

        return render_template("updated.html", msg=qty_wheels, msg2=tyres, msg3=qty_tyres)


@app.route('/power', methods=['POST', 'GET'])
def power_edit():
    if request.method == 'GET':
        return edit_buggy("buggy-form-power.html")
    elif request.method == 'POST':
        msg = ""
        # power
        power_type = database_assign('power_type', 0)
        power_units = database_assign('power_units', 1)
        aux_power_type = database_assign('aux_power_type', 0)
        aux_power_units = database_assign('aux_power_units', 1)
        hamster_booster = database_assign('hamster_booster', 1)

        return render_template("updated.html", msg=power_type, msg2=power_units, msg3=aux_power_type,
                               msg4=aux_power_units, msg5=hamster_booster)


@app.route('/flag', methods=['POST', 'GET'])
def flag_edit():
    if request.method == 'GET':
        return edit_buggy("buggy-form-flag.html")
    elif request.method == 'POST':
        msg = ""
        # flag
        flag_color = database_assign('flag_color', 0)
        flag_pattern = database_assign('flag_pattern', 0)
        flag_color_secondary = database_assign('flag_color_secondary', 0)

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
