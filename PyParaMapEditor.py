import sqlite3, numpy, wx
from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename

im_land = Image.open('land_input.bmp','r')
im_sea = Image.open('sea_input.bmp','r')

land_colours = im_land.getcolors(maxcolors=5000)

land_provinces = []

for colour in land_colours:
    land_provinces.append(colour[1])
# Ignore white
land_provinces.remove((255,255,255))

# Sea provinces

sea_colours = im_sea.getcolors(maxcolors=5000)

sea_provinces = []

for colour in sea_colours:
    sea_provinces.append(colour[1])
# Ignore white
sea_provinces.remove((255,255,255))

total_provinces = len(sea_provinces) + len(land_provinces)

print(str(len(sea_provinces)) + " sea provinces found and " +
      str(len(land_provinces)) + " land provinces found.")
print("Total provinces = " + str(total_provinces))

# Database connection class
class database_connection(object):
    def __init__(self):
        db_path = input("Input a map name:")
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        
        self.load_db()

    def db_fetchone(self):
        return self.cursor.fetchone()

    def query(self,query,params):
        # For functions that don't need to create any new fields
        return self.cursor.execute(query,params)

    def db_commit(self,query):
        # For functions that need to create a new field
        self.cursor.execute(query)
        self.connection.commit()

    def load_db(self):
        # Populate a database with default province IDs
        db_schema = "province_setup_schema.sql"
        #Read the schema file and output it as a string
        all_schema_contents = str(open(db_schema).read())

        #Separate the schema contents into separate commands by semicolons
        individual_schema_contents = all_schema_contents.split(';')
        #Get rid of newline and tab indicators from the raw string
        for schema_command in individual_schema_contents:
            for ch in ["\n", "\t"]:
                schema_command.replace(ch, "")
        for schema_command in individual_schema_contents:
            self.db_commit(schema_command + ";")

    def fill_definition(self):
        i = 1
        while i < total_provinces:
            try:
                for province in land_province_values:
                    R = str(province[0])
                    G = str(province[1])
                    B = str(province[2])
                    params = (str(i), R, G, B, "landprov"+str(i),"x")
                    query = "INSERT OR IGNORE INTO definition(Province_id, R, G, B, Name, x) VALUES (?,?,?,?,?,?)"
                    self.query(query, params)
                    print("Created definition for province " + str(i))
                    i = i+1
                for province in sea_province_values:
                    R = str(province[0])
                    G = str(province[1])
                    B = str(province[2])
                    params = (str(i), R, G, B, "seaprov"+str(i),"x")
                    query = "INSERT OR IGNORE INTO definition(Province_id, R, G, B, Name, x) VALUES (?,?,?,?,?,?)"
                    self.query(query, params)
                    print("Created definition for province " + str(i))
                    i = i+1
            finally:
                self.db_commit("")
            break

    def default_setup(self):
        i = 1
        while i < total_provinces:
            try:
                for province in land_province_values:
                    params = (str(i), "roman", "roman_pantheon", "cloth", "1", "1", "1", "1", "40", "0", "landprov"+str(i), "noregion")
                    query = "INSERT OR IGNORE INTO province_setup(ProvID, Culture, Religion, TradeGoods, Citizens, Freedmen, Slaves, Tribesmen, Civilization, Barbarian, NameRef, AraRef) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
                    self.query(query, params)
                    print("Created default province setup for land province " + str(i))
                    i = i + 1
                for province in sea_province_values:
                    params = (str(i), "", "", "", "0", "0", "0", "0", "0", "0", "seaprov"+str(i), "")
                    query = "INSERT OR IGNORE INTO province_setup(ProvID, Culture, Religion, TradeGoods, Citizens, Freedmen, Slaves, Tribesmen, Civilization, Barbarian, NameRef, AraRef) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
                    self.query(query, params)
                    print("Created default province setup for sea province " + str(i))
                    i = i + 1
            finally:
                self.db_commit("")
            break

db = database_connection()
db.fill_definition()
db.default_setup()
