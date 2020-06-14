all:

dumpdb:
	@echo "Dumping all to [main.sql]"
	@echo ".dump" | sqlite3 ./main.db > ./main.sql

dumpschema:
	@echo "Dumping schema to [main.sql]"
	@echo ".schema" | sqlite3 ./main.db > ./main.sql
