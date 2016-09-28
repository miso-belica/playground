-- foreign key of tables
SELECT tc.table_name AS fk_table, kcu.column_name AS fk_column, tc.constraint_name, rc.delete_rule, rc.update_rule, ccu.column_name AS column
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
JOIN information_schema.referential_constraints rc ON rc.constraint_name = tc.constraint_name
WHERE constraint_type = 'FOREIGN KEY' AND ccu.table_name LIKE :table_name
ORDER BY ccu.table_name, tc.table_name, kcu.column_name;


-- table sizes
SELECT relname AS "relation", pg_size_pretty(pg_relation_size(C.oid)) AS "size", pg_size_pretty(pg_total_relation_size(C.oid)) AS "size with indexes"
FROM pg_class C LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
WHERE nspname = 'public' AND C.relkind != 'i'
ORDER BY pg_relation_size(C.oid) DESC
LIMIT 10;


-- index sizes
SELECT relname AS "index_name", pg_size_pretty(pg_total_relation_size(C.oid)) AS "size"
FROM pg_class C LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
WHERE nspname = 'public' AND C.relkind = 'i'
ORDER BY pg_total_relation_size(C.oid) DESC
LIMIT 10;


-- index sizes for tables
SELECT relname AS "table_name", pg_size_pretty(pg_relation_size(C.oid)) AS "table_size", pg_size_pretty(pg_total_relation_size(C.oid) - pg_relation_size(C.oid)) AS "indexes_size", pg_size_pretty(pg_total_relation_size(C.oid)) AS "total_size"
FROM pg_class C LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
WHERE nspname = 'public' AND C.relkind != 'i'
ORDER BY pg_total_relation_size(C.oid) - pg_relation_size(C.oid) DESC
LIMIT 10;


-- index sizes for tables (bigger than 1 GB) in percentage
SELECT
  relname AS "table_name",
  pg_size_pretty(pg_relation_size(C.oid)) AS "table_size",
  pg_size_pretty(pg_total_relation_size(C.oid) - pg_relation_size(C.oid)) AS "index_size",
  round(100 - (pg_relation_size(C.oid)::numeric/pg_total_relation_size(C.oid))*100, 1) AS "index_percentage",
  pg_size_pretty(pg_total_relation_size(C.oid)) AS "total_size"
FROM pg_class C LEFT JOIN pg_namespace N ON (N.oid = C.relnamespace)
WHERE nspname = 'public' AND C.relkind != 'i' AND
pg_relation_size(C.oid) >= 1024*1024*1024 -- bigger than 1GB
ORDER BY (pg_relation_size(C.oid)::numeric/pg_total_relation_size(C.oid))*100
LIMIT 20;
