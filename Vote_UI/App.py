from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import sqlitecloud

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# SQLite connection
conn = sqlitecloud.connect('sqlitecloud://ct7cilkkhz.sqlite.cloud:8860/Voter?apikey=SQMenMaDiDJkgkkLxaJ7Z5JLBuzeZqkf1ek1Y3JUS0c')
# conn.row_factory = sqlite3.Row
@app.route('/search_voter', methods=['GET'])
def search_voter():
    search_string = request.args.get('search_string', "")
    type = request.args.get('type', "")
    
    cursor = conn.cursor()

    if type == "Name":
        cursor.execute(
            """
            SELECT assembly_no,part_no,srno,l_last_name, l_first_name, l_middle_name, e_last_name, e_first_name, e_middle_name, sex,
            house_no, age, vcardid, l_village, e_village, l_assemblyname, e_assemblyname, l_address, e_address, booth_no,
            l_boothaddress, e_boothaddress 
            FROM voters 
            WHERE LOWER(e_last_name) LIKE LOWER(?) 
            OR LOWER(e_first_name) LIKE LOWER(?) 
            OR LOWER(e_middle_name) LIKE LOWER(?)
            """, 
            (f"%{search_string}%", f"%{search_string}%", f"%{search_string}%")
        )
    else:
        cursor.execute(
            """
            SELECT assembly_no,part_no,srno,l_last_name, l_first_name, l_middle_name, e_last_name, e_first_name, e_middle_name, sex,
            house_no, age, vcardid, l_village, e_village, l_assemblyname, e_assemblyname, l_address, e_address, booth_no,
            l_boothaddress, e_boothaddress 
            FROM voters
            WHERE LOWER(vcardid) = LOWER(?)
            """,
            (search_string,)
        )
    
    rows = cursor.fetchall()
    
    voter_data = []
    # Get column names
    column_names = [description[0] for description in cursor.description]
    
    for row in rows:
        row_data = dict(zip(column_names, row))  # Creates a dictionary of column names and corresponding row values
        formatted_data = {}
        
        for key in list(row_data.keys()):
            if key.startswith('e_'):
                continue
            if key.startswith('l_'):
                e_key = 'e_' + key[2:]
                if e_key in row_data:
                    formatted_data[key[2:]] = f"{row_data[e_key]} / {row_data[key]}"
                    del row_data[key]
                    del row_data[e_key]
            else:
                formatted_data[key] = row_data[key]
        voter_data.append(formatted_data)

    return jsonify({"data": voter_data})


@app.route("/", methods=['GET'])
def read_root():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
