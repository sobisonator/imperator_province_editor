import sqlite3, numpy, wx
from PIL import Image, ImageTk
from tkinter import *
from tkinter.filedialog import askopenfilename

event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))

if __name__ == "__main__":
    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    File = askopenfilename(parent=root, initialdir="M:/",title='Choose an image.')
    print("opening %s" % File)
    img = ImageTk.PhotoImage(file=File)
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console
        cx, cy = event2canvas(event, canvas)
        print ("(%d, %d) / (%d, %d)" % (event.x,event.y,cx,cy))
    #mouseclick event
    canvas.bind("<ButtonPress-1>",printcoords)
    canvas.bind("<ButtonRelease-1>",printcoords)

    root.mainloop()

im_land = Image.open('land_input.bmp','r')
im_sea = Image.open('sea_input.bmp','r')

# Land provinces
print("Getting land province pixel colour data, please wait...")
all_pixvals_land = list(im_land.getdata())

# Now sort into unique values only, ignoring white
land_province_values = numpy.unique(all_pixvals_land, axis=0)
land_province_values = numpy.delete(land_province_values,-1,axis=0)
print(str(len(land_province_values)) + " land provinces found.")
print(land_province_values)

# Sea provinces
print("Getting sea province pixel colour data, please wait...")
all_pixvals_sea = list(im_sea.getdata())

# Now sort into unique values only, ignoring white
sea_province_values = numpy.unique(all_pixvals_sea, axis=0)
sea_province_values = numpy.delete(sea_province_values,-1,axis=0)
print(str(len(sea_province_values)) + " sea provinces found.")
print(sea_province_values)

total_provinces = len(land_province_values) + len(sea_province_values)
print(str(total_provinces) + " provinces found.")

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
