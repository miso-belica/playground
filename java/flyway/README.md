# Experiments with [flyway](http://flywaydb.org/) DB migration tool

0. Create script for baseline by command `pg_dump --schema-only --quote-all-identifiers --no-security-labels --no-owner --no-privileges -U postgres -d playground -f src/main/resources/db/migration/v2015.04.11.0__Base_line.sql`.
1. Apply script `src/main/resources/db/migration/v2015.04.11.0__Base_line.sql` into new database called *playground*.
2. Create meta table with applied updates by command `mvn clean compile flyway:baseline -Dflyway.password=postgres`.
3. See info about updates by command `mvn clean compile flyway:info -Dflyway.password=postgres`.
4. Apply migrations by command `mvn clean compile flyway:migrate -Dflyway.password=postgres`.
5. See info about updates by command `mvn clean compile flyway:info -Dflyway.password=postgres`.
6. Truncate database *playground*.
7. Play with various order of applications of migration scripts.
