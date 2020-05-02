CREATE TABLE "entries" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`url`	TEXT,
	`refurl`	TEXT,
	`notes`	TEXT,
	`completed`	INTEGER DEFAULT 0
);
