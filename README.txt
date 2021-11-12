PROVINCE SETUP EDITOR FOR IMPERATOR: ROME

Instructions:

Pre-prep (I don't have Python already):
	- Install Python from https://www.python.org/ftp/python/3.9.4/python-3.9.4-amd64.exe
	- Make sure when you install to install pip when prompted, and to add Python to PATH when prompted


1. Installing requirements to run the map editor
	a) With PyCharm (advanced)
		i) Open pyParaMapEditor_imp19c as a project. The folder is already set up as a PyCharm project so it should be recognised if you open the folder in PyCharm.
		ii) Install dependencies once you have opened the project, following this tutorial: https://www.jetbrains.com/help/pycharm/managing-dependencies.html
	b) With pip (if you don't have PyCharm)
		i) Enter the following command in your command line:
			pip install pandas gspread Pillow
		ii) Launch the script by double clicking it.

2. Preparing data (if you are using imp19c, these files should all be there already and you can skip this step!)
	a) All files below simply need to be present in the setup editor's
	b) You will need 3 map files: 
		your province map, (main_input.BMP)
		a map of your land provinces with sea provinces coloured white, (land_input.BMP)
		and a map of your sea provinces with land provinces coloured white. (sea_input.BMP)
		NOTE: There are a couple of ways you can go about creating the land and sea images:
			option i) If you have a corresponding heightmap, all of your land should be of a grayscale value above that of the sea. Find the grayscale value at which land begins and select all pixels of this colour and higher value in your advanced image editor of choice (GIMP, paint.net, etc.) You can then use this as a "cutout" layer copied into your provinces map image to select only the sea and only the land provinces and save the images relatedly.
			option ii) If you don't have a heightmap, you can simply paint over in white with a brush all areas that should be excluded from the respective image coloured in white. This won't be as accurate unless you have a very deft hand! But you can always go back in afterwards and correct the errors manually.
	 All of these images must be of the same dimensions.
	c) You may optionally load in an existing definition.csv and existing province_setup.csv, which will be loaded by the setup editor. 
	d) Credentials json file which should be selected when prompted by the program. It should be named "imp19c_credentials.json"
	

3. Using the editor
	 - When you launch the editor you will be prompted to create a new savefile, which you can name whatever you want. This will store your edited setup data.
	 	- You may also load a previous save this way. (In imp19c, load the existing "map_imported_file" file)
	 	- The map editor only takes database files in the expected format, so it will encounter an error and close if you try to open any other kind of file.
	 - You will also be prompted to enter a credentials file - select your config json file to link to the Google Sheet.
	 - Use the middle mouse button and drag the mouse to navigate the map. Alternatively, use the scrollbars around the province map canvas.
	 - Left-click on a province to select it. A crosshair will appear over the selected province while you are editing it.
	 - Click on any field on the right-hand side to edit that field.
	 	A changed field which has not yet been submitted will be coloured yellow.
	 	Press <Return> to submit your change. This will be saved to your file.

Info about fields:

SettlementRank - determines whether a province is a "settlement" (rural) or a "city" (urban)

Industrialisation - This uses the vanilla Civilisation value
