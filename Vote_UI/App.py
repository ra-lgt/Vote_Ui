from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import sqlitecloud

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# SQLite connection
conn = sqlitecloud.connect('')
create_conn = sqlitecloud.connect('sqlitecloud://chasuqamnk.sqlite.cloud:8860/userdata_145-mirabhBhaindar?apikey=0IZOcX8va89btO7M19jVGeWWfKsh83bx8BJLf3GLGh0')
# conn.row_factory = sqlite3.Row
@app.route('/search_voter', methods=['GET'])
def search_voter():
    search_string = request.args.get('search_string', "")
    type = request.args.get('type', "")
    page=request.args.get('page',0)

    search_kinds = [word.lower() for word in search_string.split()]
    
    cursor = conn.cursor()

    if type == "Name":
        # Generate the query with multiple LIKE conditions
        if len(search_kinds) == 1:
            search_kinds = [search_kinds[0]] * 3
        elif len(search_kinds) == 2:
            search_kinds = [search_kinds[0], search_kinds[1], search_kinds[1]]
        elif len(search_kinds) == 3:
            search_kinds = [search_kinds[0], search_kinds[1], search_kinds[2]]

        # Generate the query with multiple LIKE conditions
        query = f"""
            SELECT assembly_no, part_no, srno, l_last_name, l_first_name, l_middle_name, e_last_name, e_first_name, e_middle_name, sex,
                house_no, age, vcardid, l_village, l_assemblyname, e_assemblyname, l_address, '' AS e_address, booth_no,
                l_boothaddress, '' AS e_boothaddress
            FROM voters 
            WHERE {" AND ".join(["LOWER(full_name) LIKE ?"] * len(search_kinds))}
            LIMIT ? OFFSET ?
        """  

        # Create wildcard search patterns
        search_patterns = [f"%{term.lower()}%" for term in search_kinds]

        # Repeat patterns for each field and add limit and offset parameters
        params = search_patterns * 3 + [50, int(page) * 50]

        # Execute the query
        cursor.execute(query, tuple(params))
    else:
        cursor.execute(
            """
            SELECT assembly_no,part_no,srno,l_last_name, l_first_name, l_middle_name, e_last_name, e_first_name, e_middle_name, sex,
            house_no, age, vcardid, l_village, e_village, l_assemblyname, e_assemblyname, l_address,'' as e_address, booth_no,
            l_boothaddress, '' as e_boothaddress
            FROM voters
            WHERE LOWER(vcardid) = LOWER(?)
            LIMIT ? OFFSET ?
            """,
            (search_string,50,int(page)*50)
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

@app.route('/create_user_share',methods=['POST'])
def create_user_share():
    data = request.get_json()
    if not all(k in data for k in ('part_no', 'srno', 'mobileno', 'type')):
        return jsonify({"error": "Missing data fields"}), 400


    with create_conn:
        create_conn.execute('''
            CREATE TABLE IF NOT EXISTS sharehistory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                part_no INTEGER,
                srno INTEGER,
                mobileno INTEGER,
                type TEXT,
                share_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    try:
        # Insert data into the table
        with create_conn:
            create_conn.execute('''
                INSERT INTO sharehistory (part_no, srno, mobileno, type)
                VALUES (?, ?, ?, ?)
            ''', (data['part_no'], data['srno'], data['mobileno'], data['type']))
        
        return jsonify({"message": "Data inserted successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/", methods=['GET'])
def read_root():
    return render_template('index.html')


