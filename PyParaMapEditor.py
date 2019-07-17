import sqlite3, ctypes
from tkinter import *
from PIL import Image, ImageTk
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))

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
                for province in land_provinces:
                    R = str(province[0])
                    G = str(province[1])
                    B = str(province[2])
                    params = (str(i), R, G, B, "landprov"+str(i),"x")
                    query = "INSERT OR IGNORE INTO definition(Province_id, R, G, B, Name, x) VALUES (?,?,?,?,?,?)"
                    self.query(query, params)
                    print("Created definition for province " + str(i))
                    i = i+1
                for province in sea_provinces:
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
                for province in land_provinces:
                    params = (str(i), "roman", "roman_pantheon", "cloth", "1", "1", "1", "1", "40", "0", "landprov"+str(i), "noregion")
                    query = "INSERT OR IGNORE INTO province_setup(ProvID, Culture, Religion, TradeGoods, Citizens, Freedmen, Slaves, Tribesmen, Civilization, Barbarian, NameRef, AraRef) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"
                    self.query(query, params)
                    print("Created default province setup for land province " + str(i))
                    i = i + 1
                for province in sea_provinces:
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

editorframe = Frame(frame, bd=2, relief=SUNKEN, padx=110)
editorframe.grid(row=0, column=2)

def makeentry(parent, caption, rownum, **options):
    Label(parent, text=caption, pady=10).grid(row = rownum, column = 0)
    entry = Entry(parent, width=16, font=("Arial 18"), **options)
    entry.grid(row = rownum, column = 1)
    return entry

fields = [
    "ProvID",
    "Culture",
    "Religion",
    "TradeGoods",
    "Citizens",
    "Freedmen",
    "Slaves",
    "Tribesmen",
    "Civilization",
    "Barbarian",
    "NameRef",
    "AraRef"
]

frame.pack(fill=BOTH,expand=1)

def submit_entry(event, fields):
    try:
        submission = event.widget.get()
        print("Submitting " + submission)
        event.widget.config({"background":"lime"})
        print(fields)
        widget_id = fields[list_of_entries.index(event.widget)]
        # Now find the field that corresponds to the widget
        submission_query = "UPDATE province_setup SET '" + widget_id + "'='" + str(submission) + "' WHERE ProvID = "+ list_of_entries[0].get() +";"
        db.db_commit(submission_query)
    except Exception as ex:
        print("Unacceptable input. Ignoring submission.")
        print(ex)

def create_fields():
    i = 1
    list_of_entries = []
    for field in fields:
        setting = "normal"
        if field == "ProvID":
            setting = "readonly"
        entry = makeentry(editorframe, field, i, state=setting)
        entry.bind("<KeyPress>", entry_changing)
        entry.bind("<KeyRelease>", entry_changed)
        list_of_entries.append(entry)
        i = i + 1
    return list_of_entries

entry_value = None

def entry_changing(event):
    global entry_value
    value = event.widget.get()
    entry_value = value

def entry_changed(event):
    global entry_value
    value = event.widget.get()
    if value != entry_value:
        event.widget.config({"background":"yellow"})

list_of_entries = create_fields()

#adding the image
img = ImageTk.PhotoImage(file='main_input.bmp', size=(1024,768))
pxdata = Image.open('main_input.bmp','r')
px = pxdata.load()
canvas.create_image(0,0,image=img,anchor="nw")
canvas.config(scrollregion=canvas.bbox(ALL))

prevprovince = None

#function to be called when mouse is clicked
def getprovince(event):
    global prevprovince
    #outputting x and y coords to console
    cx, cy = event2canvas(event, canvas)
    print ("click at (%d, %d) / (%d, %d)" % (event.x,event.y,cx,cy))
    colour = px[cx,cy]
    params = colour
    # Look in definition first to get the province ID from RGB
    search_query = "SELECT Province_ID FROM definition WHERE R=? AND G=? AND B=?;"
    db.query(search_query,params)
    province = str(db.db_fetchone()[0])
    # Do not repeat all this if the province is already selected
    if province != prevprovince:
        prevprovince = province
        print("province ID is " + province)
        province_data_query = "SELECT * FROM province_setup WHERE ProvID = " + province + ";"
        db.query(province_data_query, "")
        province_data = db.db_fetchone()
        for index, entry in enumerate(list_of_entries):
            entry.config(state="normal")
            entry.delete(0,999)
            entry.insert(0,province_data[index])
            entry.config({"background":"white"})
            if index == 0:
                entry.config(state="readonly")
        print(province_data)

mousewheel = 0

def _on_mousewheel_dn(event):
    global mousewheel
    global scan_anchor
    mousewheel = 1
    print(event)
    canvas.scan_mark(event.x, event.y)

def _on_mousewheel_up(event):
    global mousewheel
    mousewheel = 0
    print(event)

def scan(event):
    global mousewheel
    if mousewheel == 1:
        print(event)
        canvas.scan_dragto(event.x,event.y)
    
#mouseclick event
canvas.bind_all("<ButtonPress-2>", _on_mousewheel_dn)
canvas.bind_all("<ButtonRelease-2>", _on_mousewheel_up)
canvas.bind_all("<Motion>",scan)
canvas.bind_all("<Return>", lambda event, fieldvar=fields:submit_entry(event, fieldvar))
canvas.bind("<ButtonPress-1>",getprovince)

# Replace spaces with semicolons for input to definition.csv province names

root.mainloop()
