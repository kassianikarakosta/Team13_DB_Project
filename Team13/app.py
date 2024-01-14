#ΕΡΓΑΣΙΑ ΣΤΑ ΠΛΑΙΣΙΑ ΤΟΥ ΜΑΘΗΜΑΤΟΣ "ΒΑΣΕΙΣ ΔΕΔΟΜΕΝΩΝ - ΔΙΔΑΣΚΑΛΙΑ 2023-2024"
#
#Ο ΠΑΡΟΝ ΚΩΔΙΚΑΣ ΔΗΜΙΟΥΡΓΗΘΗΚΕ ΓΙΑ ΤΙΣ ΑΝΑΓΚΕΣ ΤΟΥ ΜΑΘΗΜΑΤΟΣ ΚΑΙ ΑΝΗΚΕΙ ΣΤΟΥΣ ΦΟΙΤΗΤΕΣ:
#ΚΑΣΣΙΑΝΗ ΚΑΡΑΚΩΣΤΑ, ΑΜ: 1083922
#ΖΑΡΡΗΣ ΑΡΙΣΤΕΙΔΗΣ ΣΤΥΛΙΑΝΟΣ, ΑΜ: 1083625

from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os

app = Flask(__name__)

# Function to get the SQLite connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('music.db')
    return db

# Function to get the SQLite cursor
def get_cursor():
    return get_db().cursor()

# Teardown function to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Function to execute SQL file
def execute_sql_file(sql_file):
    with app.app_context():
        with get_db() as db:
            cursor = db.cursor()

            with open(sql_file, 'r') as file:
                sql_statements = file.read()

            # Wrap the script execution in a try-except block
            try:
                cursor.executescript(sql_statements)
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")

            # Commit the transaction
            db.commit()

# Load database schema and initial data
execute_sql_file('database.sql')




# Define the route for the Creator form
@app.route('/creator', methods=['GET', 'POST'])
def creator():
    if request.method == 'POST':

        submit=request.form['submit']

        # Insert data into the database
        if submit == 'sub': 
            # Get data from the form
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            artist_name = request.form['artist_name']
            role = request.form['role']
            phone = request.form['phone']
            streetname = request.form['streetname']
            streetnum = request.form['streetnum']
            city = request.form['city']
            postcode = request.form['postcode']
            start_date = request.form['start_date']
            end_date = request.form['end_date']

            
            with get_db() as db:
                cursor = db.cursor()

                if artist_name is None: 

                    artist_name = " "
                    cursor.execute("INSERT INTO CREATOR (firstname, lastname, artist_name, artist_role, phone, street, streetnum, city, postcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (firstname, lastname, artist_name, role, phone, streetname, streetnum, city, postcode))
                else:
                    cursor.execute("INSERT INTO CREATOR (firstname, lastname, artist_name, artist_role, phone, street, streetnum, city, postcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (firstname, lastname, artist_name, role, phone, streetname, streetnum, city, postcode))

                # Get the last inserted creator_id
                creator_id = cursor.lastrowid

                # Insert data into the CONTRACT_S table
                cursor.execute("INSERT INTO CONTRACT_S (date_start, date_end, creator_id) VALUES (?, ?, ?)",
                            (start_date, end_date, creator_id))

            # Redirect to the home page or any other page
            return redirect(url_for('creator'))
        # Delete data from the database
        elif submit == 'del':  
            # Get data from the form for deletion
            fullname = request.form['fullname']
            print(fullname)
            print("test")

            with get_db() as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM CREATOR WHERE firstname || ' ' || lastname || ' - ' || artist_name = ?", (fullname,))
                db.commit()

            return redirect(url_for('creator'))
        # Update data into the database
        elif submit == 'upd':
            full_name = request.form['full_name']
            artist_name = request.form['artist_name']
            artist_role = request.form['role']
            phone = request.form['phone']
            street = request.form['streetname']
            streetnum = request.form['streetnum']
            city = request.form['city']
            postcode = request.form['postcode']
            date_start = request.form['start_date']
            date_end = request.form['end_date']

            with get_db() as db:
                cursor = db.cursor()

                cursor.execute("SELECT creator_id FROM CREATOR WHERE firstname || ' ' || lastname = ?", (full_name,))
                artist_id = cursor.fetchone()[0]

                if artist_name!="":
                    cursor.execute("UPDATE CREATOR SET artist_name = ? WHERE firstname || ' ' || lastname = ?", (artist_name, full_name,))
                    db.commit()

                if artist_role!="":
                    cursor.execute("UPDATE CREATOR SET artist_role = ? WHERE firstname || ' ' || lastname = ?", (artist_role, full_name,))
                    db.commit()

                if phone!="":
                    cursor.execute("UPDATE CREATOR SET phone = ? WHERE firstname || ' ' || lastname = ?", (phone, full_name,))
                    db.commit()
                    print(phone)

                if street!="":
                    cursor.execute("UPDATE CREATOR SET street = ? WHERE firstname || ' ' || lastname = ?", (street, full_name,))
                    db.commit()
                    print(street)

                if streetnum!="":
                    cursor.execute("UPDATE CREATOR SET streetnum = ? WHERE firstname || ' ' || lastname = ?", (streetnum, full_name,))
                    db.commit()
                    print(streetnum)


                if city!="":
                    cursor.execute("UPDATE CREATOR SET city = ? WHERE firstname || ' ' || lastname = ?", (city, full_name,))
                    db.commit()
                    print(city)

                if postcode!="":
                    cursor.execute("UPDATE CREATOR SET postcode = ? WHERE firstname || ' ' || lastname = ?", (postcode, full_name,))
                    db.commit()
                    print(postcode)

                if date_start!="":
                    cursor.execute("UPDATE CONTRACT_S SET date_start = ? WHERE creator_id = ?", (date_start, artist_id,))
                    db.commit()

                if date_end!="":
                    cursor.execute("UPDATE CONTRACT_S SET date_end = ? WHERE creator_id = ?", (date_end, artist_id,))
                    db.commit()

            return redirect(url_for('creator'))

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT firstname || ' ' || lastname || ' - ' || artist_name FROM CREATOR")
        fullnames = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT firstname || ' ' || lastname FROM CREATOR")
        full_names = [row[0] for row in cursor.fetchall()]

    return render_template('creator.html', fullnames=fullnames, full_names=full_names)


# Define the route for the album form
@app.route('/album', methods=['GET', 'POST'])
def album():
    if request.method == 'POST':
        submit=request.form['submit']

        if submit == 'sub': 
            # Get data from the form
            album_title = request.form['album_title']
            release_date = request.form['release_date']
            

            # Insert data into the database
            with get_db() as db:
                cursor = db.cursor()
                cursor.execute("INSERT INTO ALBUM (album_title, release_date) VALUES (?, ?)",
                            (album_title, release_date))

                # # Get the last inserted creator_id
                album_id = cursor.lastrowid

            # Redirect to the home page or any other page
            return redirect(url_for('album'))
        
        elif submit == 'del':
            # Get data from the form for deletion
            a_name = request.form['album']

            with get_db() as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM ALBUM WHERE album_title = ?", (a_name,))
                db.commit()

            return redirect(url_for('album'))

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT album_title FROM ALBUM")
        albums = [row[0] for row in cursor.fetchall()]


    return render_template('album.html',albums=albums)

# Define the route for the producer form
@app.route('/producer', methods=['GET', 'POST'])
def producer():
    if request.method == 'POST':

        submit=request.form['submit']

        if submit == 'sub':
            # Get data from the form
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            phone = request.form['phone']
            streetname = request.form['streetname']
            streetnum = request.form['streetnum']
            city = request.form['city']
            postcode = request.form['postcode']

            # Insert data into the database
            with get_db() as db:
                cursor = db.cursor()
                cursor.execute("INSERT INTO PRODUCER (firstname, lastname, phone, streetname, streetnum, city, postcode) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (firstname, lastname, phone, streetname, streetnum, city, postcode))

                # # Get the last inserted creator_id
                producer_id = cursor.lastrowid

            # Redirect to the home page or any other page
            return redirect(url_for('producer'))
        
        elif submit == 'del':
            # Get data from the form for deletion
            p_name = request.form['producer']

            with get_db() as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM PRODUCER WHERE firstname || ' ' || lastname = ?", (p_name,))
                db.commit()

            return redirect(url_for('producer'))
        
        elif submit == 'upd':
            p_name = request.form['producer_name']
            phone = request.form['phone']
            streetname = request.form['streetname']
            streetnum = request.form['streetnum']
            city = request.form['city']
            postcode = request.form['postcode']

            with get_db() as db:
                cursor = db.cursor()

                if phone!="":
                    cursor.execute("UPDATE PRODUCER SET phone = ? WHERE firstname || ' ' || lastname = ?", (phone, p_name,))
                    db.commit()

                if streetname!="":
                    cursor.execute("UPDATE PRODUCER SET streetname = ? WHERE firstname || ' ' || lastname = ?", (streetname, p_name,))
                    db.commit()

                if streetnum!="":
                    cursor.execute("UPDATE PRODUCER SET streetnum = ? WHERE firstname || ' ' || lastname = ?", (streetnum, p_name,))
                    db.commit()

                if city!="":
                    cursor.execute("UPDATE PRODUCER SET city = ? WHERE firstname || ' ' || lastname = ?", (city, p_name,))
                    db.commit()

                if postcode!="":
                    cursor.execute("UPDATE PRODUCER SET postcode = ? WHERE firstname || ' ' || lastname = ?", (postcode, p_name,))
                    db.commit()

            return redirect(url_for('producer'))

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT firstname || ' ' || lastname FROM PRODUCER")
        producers = [row[0] for row in cursor.fetchall()]
            


    return render_template('producer.html',producers=producers)

# Define the route for the song form
@app.route('/song', methods=['GET', 'POST'])
def song():
    with get_db() as db:
        # Fetch data for dropdowns from the database
        cursor = db.cursor()

        cursor.execute("SELECT album_title FROM ALBUM")
        album_titles = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT studio_name FROM STUDIO")
        studio_names = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT firstname || ' ' || lastname FROM CREATOR UNION SELECT DISTINCT artist_name FROM CREATOR")
        artist_names = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT firstname || ' ' || lastname FROM CREATOR WHERE artist_role='lyricist'")
        lyricist_names = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT firstname || ' ' || lastname FROM CREATOR WHERE artist_role='composer'")
        composer_names = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT firstname || ' ' || lastname FROM PRODUCER")
        producer_names = [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        submit=request.form['submit']

        if submit == 'sub':
            # Extract form data
            song_title = request.form['song_title']
            album_title = request.form['album_title']
            category = request.form['category']
            studio_name = request.form['studio_name']
            artist_name = request.form['artist_name']
            producer_name = request.form['producer_name']
            duration = request.form['duration']
            release_date = request.form['release_date']

            with get_db() as db:
                cursor = db.cursor()

                cursor.execute("SELECT album_id FROM ALBUM WHERE album_title = ?", (album_title,))
                album_id = cursor.fetchone()[0]

                cursor.execute("SELECT studio_id FROM STUDIO WHERE studio_name = ?", (studio_name,))
                studio_id = cursor.fetchone()[0]

                cursor.execute("SELECT DISTINCT creator_id FROM CREATOR WHERE firstname || ' ' || lastname = ? OR artist_name=?", (artist_name,artist_name))
                creator_id = cursor.fetchall()
                # print(creator_id)
                # creator_id = cursor.fetchall()[0]

                cursor.execute("SELECT producer_id FROM PRODUCER WHERE firstname || ' ' || lastname = ?", (producer_name,))
                producer_id = cursor.fetchone()[0]

                cursor.execute("INSERT INTO SONG (song_title, duration, category, release_date, studio_id, producer_id) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            (song_title, duration, category, release_date, studio_id, producer_id))
                db.commit()

                cursor.execute("SELECT last_insert_rowid()")
                song_id = cursor.fetchone()[0]

                # for row in range(len(creator_id)):
                #     print(creator_id[row])


                for row in range(len(creator_id)):
                    
                    cursor.execute("INSERT INTO RECORDING (song_id, singer_id) VALUES (?, ?)", (song_id, creator_id[row][0]))
                    db.commit()

                cursor.execute("INSERT INTO INCLUDES (song_id, album_id) VALUES (?, ?)", (song_id, album_id))
                db.commit()

            return redirect(url_for('song'))
        
        elif submit == 'del':
            # Get data from the form for deletion
            s_name = request.form['song']

            with get_db() as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM SONG WHERE song_title = ?", (s_name,))
                db.commit()

            return redirect(url_for('song'))

    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT song_title FROM SONG")
        songs = [row[0] for row in cursor.fetchall()]

    return render_template('song.html', album_titles=album_titles, studio_names=studio_names,
                           artist_names=artist_names, producer_names=producer_names, composer_names=composer_names, lyricist_names=lyricist_names, songs=songs)

# Define the route for the Creator form
@app.route('/studio', methods=['GET', 'POST'])
def studio():
    if request.method == 'POST':
        submit=request.form['submit']

        if submit == 'sub':
            # Get data from the form
            studio_name = request.form['studio_name']
            phone = request.form['phone']
            streetname = request.form['streetname']
            streetnum = request.form['streetnum']
            city = request.form['city']
            postcode = request.form['postcode']

            # Insert data into the database
            with get_db() as db:
                cursor = db.cursor()
                cursor.execute("INSERT INTO STUDIO (studio_name, phone, street, streetnum, city, postcode) VALUES (?, ?, ?, ?, ?, ?)",
                            (studio_name, phone, streetname, streetnum, city, postcode))

                # Get the last inserted creator_id
                studio_id = cursor.lastrowid

            # Redirect to the home page or any other page
            return redirect(url_for('studio'))
        
        elif submit == 'del':
            # Get data from the form for deletion
            s_name = request.form['studio']

            with get_db() as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM STUDIO WHERE studio_name = ?", (s_name,))
                db.commit()

            return redirect(url_for('studio'))

        elif submit == 'upd':
            s_name = request.form['studio_name']
            phone = request.form['phone']
            streetname = request.form['streetname']
            streetnum = request.form['streetnum']
            city = request.form['city']
            postcode = request.form['postcode']

            with get_db() as db:
                cursor = db.cursor()

                if phone!="":
                    cursor.execute("UPDATE STUDIO SET phone = ? WHERE studio_name = ?", (phone, s_name,))
                    db.commit()

                if streetname!="":
                    cursor.execute("UPDATE STUDIO SET streetname = ? WHERE studio_name = ?", (streetname, s_name,))
                    db.commit()

                if streetnum!="":
                    cursor.execute("UPDATE STUDIO SET streetnum = ? WHERE studio_name = ?", (streetnum, s_name,))
                    db.commit()

                if city!="":
                    cursor.execute("UPDATE STUDIO SET city = ? WHERE studio_name = ?", (city, s_name,))
                    db.commit()

                if postcode!="":
                    cursor.execute("UPDATE STUDIO SET postcode = ? WHERE studio_name = ?", (postcode, s_name,))
                    db.commit()

            return redirect(url_for('studio'))


    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT DISTINCT studio_name FROM STUDIO")
        studios = [row[0] for row in cursor.fetchall()]

    return render_template('studio.html',studios=studios)

# Add the home route
@app.route('/home')
def home():
    return render_template('home.html')

# Define the route for the sales form
@app.route('/sales', methods=['GET', 'POST'])
def sales():
    

    if request.method == 'POST':
        submit=request.form['submit']

        if submit == 'sub':
            # Extract form data
            album_title = request.form['album_title']
            album_qtty = request.form['album_qtty']
            s_month = request.form['s_month']
            s_year = request.form['s_year']

            with get_db() as db:
                cursor = db.cursor()

                cursor.execute("SELECT album_id FROM ALBUM WHERE album_title = ?", (album_title,))
                album_id = cursor.fetchone()[0]

                cursor.execute("INSERT INTO SALES (album_id, album_qtty, s_month, s_year) "
                            "VALUES (?, ?, ?, ?)",
                            (album_id, album_qtty, s_month, s_year))
                db.commit()

            # Redirect to the home page or any other page
            return redirect(url_for('sales'))
        
        if submit == 'del':
            # Get data from the form for deletion
            album_title = request.form['album_title']
            s_month = request.form['s_month']
            s_year = request.form['year']

            with get_db() as db:
                cursor = db.cursor()
                cursor.execute("SELECT album_id FROM ALBUM WHERE album_title = ?", (album_title,))
                album_id = cursor.fetchone()[0]

                cursor.execute("DELETE FROM SALES WHERE album_id = ? AND s_month = ? AND s_year = ?", (album_id,s_month,s_year,))
                db.commit()

            return redirect(url_for('sales'))

    
    with get_db() as db:
        # Fetch data for dropdowns from the database
        cursor = db.cursor()

        cursor.execute("SELECT album_title FROM ALBUM")
        album_titles = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT min(s_year) FROM SALES ORDER BY S_YEAR")
        min_year = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT max(s_year) FROM SALES ORDER BY S_YEAR")
        max_year = [row[0] for row in cursor.fetchall()]

        years = [year for year in range(min_year[0],max_year[0]+1,1)]

        cursor.execute("SELECT s_month FROM SALES")
        months = [row[0] for row in cursor.fetchall()]



    return render_template('sales.html',album_titles=album_titles, years=years,months=months)



# Add the data route
@app.route('/data')
def data():
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT STUDIO.studio_name AS StudioName, COUNT(SONG.song_id) AS SongCount FROM STUDIO LEFT JOIN SONG ON STUDIO.studio_id = SONG.studio_id GROUP BY STUDIO.studio_id ORDER BY SongCount DESC;")
        studio_data = cursor.fetchall()

        cursor.execute("SELECT SALES.s_year, ALBUM.album_title AS most_popular_album FROM ALBUM JOIN SALES ON ALBUM.album_id = SALES.album_id GROUP BY SALES.s_year ORDER BY SALES.s_year;")
        album_sales_data = cursor.fetchall()

        cursor.execute("SELECT P.firstname || ' ' || P.lastname AS producer_name, COUNT(S.song_id) AS song_count FROM PRODUCER P LEFT JOIN SONG S ON P.producer_id = S.producer_id GROUP BY producer_name;")
        producer_data = cursor.fetchall()

        cursor.execute("SELECT s_year, category FROM(SELECT category, album_qtty*COUNT(SONG.song_id) AS CAT_SONG_SOLD, SALES.s_year FROM ALBUM, SALES, INCLUDES, SONG WHERE ALBUM.album_id=SALES.album_id AND ALBUM.album_id=INCLUDES.album_id AND INCLUDES.song_id=SONG.song_id GROUP BY ALBUM.album_id, SALES.s_year, SONG.category) GROUP BY s_year;")
        category_data = cursor.fetchall()

    return render_template('data.html', studio_data=studio_data, album_sales_data=album_sales_data,producer_data=producer_data,category_data=category_data)

if __name__ == '__main__':
    app.run(debug=True)
