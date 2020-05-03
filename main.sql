PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "entries" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`url`	TEXT,
	`refurl`	TEXT,
	`notes`	TEXT,
	`completed`	INTEGER DEFAULT 0,
	`inprogress`	INTEGER DEFAULT 0
);
INSERT INTO "entries" VALUES(1,'One Punch S2','https://mega.nz/folder/jrJBBQ6Y#OBvPwTpQ8I73IgM2oaHiWg','https://forum.snahp.it/viewtopic.php?f=13&p=85418#p85418',NULL,1,0);
INSERT INTO "entries" VALUES(2,'Steins;Gate 0','https://mega.nz/folder/NgsFBQiI#c2IrcsZgI3DeNBgQeA_p9w','https://forum.snahp.it/viewtopic.php?f=13&t=34584',NULL,1,0);
INSERT INTO "entries" VALUES(3,'Cowboy Bebop','https://mega.nz/folder/C2ZWFYKQ#yErSOqeAAJ7dd0YPDfRmQA/folder/iiQWCASS','https://forum.snahp.it/viewtopic.php?f=13&t=34584',NULL,1,0);
INSERT INTO "entries" VALUES(4,'UP Series','https://mega.nz/folder/6nRSjCrA#9m6pkU5zRQ9RSiafMPXm9g','https://forum.snahp.it/viewtopic.php?f=73&p=160370#p160370
',NULL,0,0);
INSERT INTO "entries" VALUES(5,'Lunchbox','https://mega.nz/#!IQY1AKqL!D3GwUAIHy9eP8gzgqZhnbCmdcE4W3jT4tjUb_9OiIsI','https://forum.snahp.it/viewtopic.php?f=72&p=567969#p567969',NULL,1,0);
INSERT INTO "entries" VALUES(6,'Steins;Gate','https://mega.nz/folder/poB3DKpa#i2s2Azz6TvtNS3eRN0wQQA','https://forum.snahp.it/viewtopic.php?f=13&p=126510#p126510',NULL,0,0);
INSERT INTO "entries" VALUES(7,'Wolf Children','https://mega.nz/file/HShCmYBA#MqEkr-BjOXtN4zqj5ezrD30geWziWdo2MNOaSRLnlCA','https://forum.snahp.it/viewtopic.php?f=13&p=126510#p126510',NULL,1,0);
INSERT INTO "entries" VALUES(8,'I Want to eat your Pancreas','https://mega.nz/file/MoAjwISY#ccdBP1-gulWGcNu-ZAJJ8DYzCmMyTAmD3uqrWa_RO8c','https://forum.snahp.it/viewtopic.php?f=13&p=126510#p126510',NULL,0,0);
INSERT INTO "entries" VALUES(9,'Children who chase lost voices','https://mega.nz/file/lxBSEQhB#-9faxX78y7C6_dTgPvmS5VJQg8dz2AwdMW-KGd0YywQ','https://forum.snahp.it/viewtopic.php?f=13&p=126510#p126510',NULL,0,0);
INSERT INTO "entries" VALUES(10,'Westworld S3','https://mega.nz/folder/ETYCyKCZ#z_LPlrEKFaMlaB51kJZW_w','https://forum.snahp.it/viewtopic.php?f=57&t=203098&hilit=westworld+s03',NULL,0,0);
INSERT INTO "entries" VALUES(11,'Revolver','https://mega.nz/#F!FFk3wKwC!SoIbEPRtyHTZlfMB9a_qlA','https://forum.snahp.it/viewtopic.php?f=56&p=267362#p267362',NULL,0,0);
INSERT INTO "entries" VALUES(12,'Ship of Theseus','https://mega.nz/file/3O5lwSiT#jHM9SpqnR5msl_JPqN4dWweVglcXQW16el7L_S_db4g','https://forum.snahp.it/viewtopic.php?f=26&p=82281#p82281',NULL,0,0);
INSERT INTO "entries" VALUES(13,'Venture Brothers S1-S5','https://mega.nz/folder/djACjTgI#boYX-ARNKrVQ-fublBpyNA','https://forum.snahp.it/viewtopic.php?f=84&t=132354&hilit=venture+bros+mega',NULL,0,0);
DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('entries',13);
COMMIT;
