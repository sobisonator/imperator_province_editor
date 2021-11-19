CREATE TABLE IF NOT EXISTS province_setup (
	ProvID INTEGER PRIMARY KEY,
	Culture VARCHAR,
	Religion VARCHAR,
	TradeGoods VARCHAR,
	Citizens INTEGER,
	Freedmen INTEGER,
	Slaves INTEGER,
	Tribesmen INTEGER,
	Nobles INTEGER,
	Civilization INTEGER,
	SettlementRank VARCHAR,
	Barbarian BOOLEAN,
	NameRef VARCHAR,
	AraRef VARCHAR,
	Terrain VARCHAR,
	isChanged BOOLEAN
);

CREATE TABLE IF NOT EXISTS definition (
	Province_id INTEGER PRIMARY KEY,
	R INTEGER,
	G INTEGER,
	B INTEGER,
	Name VARCHAR,
	x VARCHAR
);

CREATE TABLE IF NOT EXISTS province_checksums (
	province_checksum INTEGER PRIMARY KEY
);
