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
    page=request.args.get('page',0)
    first_name=request.args.get('first_name','')
    middle_name=request.args.get('middle_name','')
    last_name=request.args.get('last_name','')

    search_kinds = [word.lower() for word in search_string.split()]
    
    cursor = conn.cursor()

    if(type==''):
        query = """
            SELECT assembly_no, part_no, srno, l_last_name, l_first_name, l_middle_name, e_last_name, e_first_name, e_middle_name, sex,
                house_no, age, vcardid, l_village, l_assemblyname, e_assemblyname, l_address, '' AS e_address, booth_no,
                l_boothaddress, '' AS e_boothaddress
            FROM voters 
            WHERE LOWER(e_first_name) LIKE ? 
            AND LOWER(e_middle_name) LIKE ? 
            AND LOWER(e_last_name) LIKE ?
            LIMIT ? OFFSET ?
        """

        # Prepare parameters with wildcard matching for LIKE
        first_name_param = f"{first_name.lower()}%"
        middle_name_param = f"{middle_name.lower()}%"
        last_name_param = f"{last_name.lower()}%"

        records_per_page = 50
        offset = int(page) * records_per_page

        # Execute the query with parameters
        cursor.execute(query, (first_name_param, middle_name_param, last_name_param,records_per_page, offset))

    elif type == "Name":
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
            WHERE {" AND ".join(["LOWER(e_first_name) LIKE ?", "LOWER(e_middle_name) LIKE ?", "LOWER(e_last_name) LIKE ?"] * len(search_kinds))}
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


@app.route("/", methods=['GET'])
def read_root():
    return render_template('index_2.html')


if __name__ == '__main__':
    app.run(debug=True)
