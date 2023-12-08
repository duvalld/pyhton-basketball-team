BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "cities" (
	"id"	INTEGER,
	"city"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "teams" (
	"id"	INTEGER,
	"team"	TEXT NOT NULL,
	"city_id"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "players" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"team_id"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "coaches" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"role"	TEXT NOT NULL,
	"team_id"	INTEGER NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "seasons" (
	"id"	INTEGER,
	"season"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "games" (
	"id"	INTEGER,
	"season_id"	INTEGER NOT NULL,
	"home_team_id"	INTEGER NOT NULL,
	"visitor_team_id"	INTEGER NOT NULL,
	"result"	TEXT,
	PRIMARY KEY("id")
);
INSERT INTO "cities" VALUES (1,'Miami');
INSERT INTO "cities" VALUES (2,'Los Angeles');
INSERT INTO "teams" VALUES (1,'Heat',1);
INSERT INTO "teams" VALUES (2,'Lakers',2);
INSERT INTO "players" VALUES (1,'Butler',1);
INSERT INTO "players" VALUES (2,'Hero',1);
INSERT INTO "coaches" VALUES (1,'Heat Coach 1','Offensive',1);
INSERT INTO "coaches" VALUES (2,'Heat Coach 2','Defensive',1);
INSERT INTO "coaches" VALUES (3,'Heat Coach 3','Physical Training',1);
INSERT INTO "seasons" VALUES (1,'Season 23');
INSERT INTO "games" VALUES (1,1,1,2,NULL);
COMMIT;
