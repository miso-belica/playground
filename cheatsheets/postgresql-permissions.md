# [PostgreSQL roles system](http://www.postgresql.org/docs/current/static/user-manag.html)

From PG 8.1 roles are new users and groups. Role can act as user, group of users or both. Role can have membership in another roles.

- [Auditing Users and Roles in PostgreSQL](http://blog.2ndquadrant.com/auditing-users-and-roles-in-postgresql/)
- [Application users vs. Row Level Security](http://blog.2ndquadrant.com/application-users-vs-row-level-security/)

## Roles
Create new role with [`CREATE ROLE "name" WITH LOGIN UNENCRYPTED PASSWORD 'password' [SUPERUSER]`](http://www.postgresql.org/docs/current/static/sql-createrole.html) or from CLI by `createuser "name"`.

Update role by [`ALTER ROLE "name" WITH SUPERUSER | NOSUPERUSER LOGIN PASSWORD 'password'`](http://www.postgresql.org/docs/current/static/sql-alterrole.html)

Delete role with [`DROP ROLE [IF EXISTS] "name", "..."`](http://www.postgresql.org/docs/current/static/sql-droprole.html) or from CLI by `dropuser "name"`.

To see available role execute `SELECT rolname FROM pg_roles`.

## Role attributes
To create new user you can invoke `CREATE USER "name" WITH UNENCRYPTED PASSWORD 'password'` or `CREATE ROLE "name" WITH LOGIN UNENCRYPTED PASSWORD 'password'`. User is simple role with `LOGIN` attribute.

Superuser role bypasses all perms checks (except the right to log in). Only superuser can create other superusers. Create it by `CREATE ROLE "name" WITH SUPERUSER`.

To create role role has to have attribute `CREATEDB`, so created by `CREATE ROLE "name" WITH CREATEDB`.

To create new roles role has to have `CREATEROLE` attribute.

## Role membership
Every role automaticaly inherits perms of roles it belongs to. So attribute `INHERIT` is set by default.

You can assign all perms of role to another role by `GRANT "group_role" TO "role", "..."` and remove them by `REVOKE "group_role" FROM "role", "..."`.

If some user belongs to role and have `INHERIT` attribute he inheriths all perms from those roles. If role does not inherit he has to [`SET ROLE "name"`](http://www.postgresql.org/docs/current/static/sql-set-role.html) to have perms of that role.

Created objects (databases, function, ...) are automaticaly owned by role that created them or by role the user is set to by `SET ROLE "name"`.

Role can be restored by `SET ROLE "original_user"` or `SET ROLE NONE` or `RESET ROLE`.

Attributes `LOGIN, SUPERUSER, CREATEDB, CREATEROLE` are not inherited. Must be set to role explicitly or user has to `SET ROLE` to role that has these attributes to perform the operations.

## Dropping roles and ownership
If role owns some objects (DB, ...) these objects should be deleted by [`DROP OWNED BY "role", "..." | CURRENT_USER [CASCADE | RESTRICT]`](http://www.postgresql.org/docs/current/static/sql-drop-owned.html) or reasigned first. You can do it one oby one by `ALTER TABLE bobs_table OWNER TO alice` or by [`REASSIGN OWNED BY "old_role" | CURRENT_USER TO "new_role" | CURRENT_USER`](http://www.postgresql.org/docs/current/static/sql-reassign-owned.html).

`DROP | REASSIGN OWNED` can not access objects in other databases, so it should be run in every DB. Also it does not drop DBs and tablespaces so these shuld be removed manually.

`DROP OWNED` also takes care of removing any privileges granted to the target role for objects that do not belong to it. Because `REASSIGN OWNED` does not touch such objects, it's typically necessary to run both `REASSIGN OWNED` and `DROP OWNED` (**in that order!**) to fully remove the dependencies of a role to be dropped.

In short then, the most general recipe for removing a role that has been used to own objects is:

```sql
REASSIGN OWNED BY "doomed_role" TO "successor_role";
DROP OWNED BY "doomed_role";
-- repeat the above commands in each database of the cluster

DROP ROLE "doomed_role";
```

# [Privileges](http://www.postgresql.org/docs/current/static/ddl-priv.html)
When an object is created, it is assigned an owner (current role). Only owned can manipulate with such object unless some perms are explicitly assigned.

Privileges varies depending on the object. For complete privileges see [`GRANT`](http://www.postgresql.org/docs/current/static/sql-grant.html) command.

Ownedship of the object can be changel by `ALTER OBJECT` and the user has to be member of the both roles (old and new owner).

`GRANT ALL` grants all possible perms. Special user `PUBLIC` can be used to add perms to all users on the system.

Revoke privige by `REVOKE ALL ON "object" FROM PUBLIC`.

It is possible to grant a privilege `WITH GRANT OPTION`, which gives the recipient the right to grant it in turn to others. If the grant option is subsequently revoked then all who received the privilege from that recipient (directly or through a chain of grants) will lose the privilege.

PostgreSQL grants default privileges on some types of objects to PUBLIC. No privileges are granted to PUBLIC by default on tables, columns, schemas or tablespaces. For other types, the default privileges granted to PUBLIC are as follows: CONNECT and CREATE TEMP TABLE for databases; EXECUTE privilege for functions; and USAGE privilege for languages.

## Examples

```sql
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "role-read"; -- read-only access to DB
```

```sql
ALTER DEFAULT PRIVILEGES
FOR ROLE "role-creator-of-tables"
IN SCHEMA "public"
GRANT SELECT ON TABLES TO "role-read";
```

```sql
GRANT CONNECT, TEMPORARY, TEMP ON DATABASE "database" TO "role";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA "public" TO "role";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA "public" TO "role";
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA "public" TO "role";
GRANT USAGE ON TYPE "type" TO "role";
```

Owners of tables:
```sql
select t.table_name, u.usename
from information_schema.tables t
join pg_catalog.pg_class c on (t.table_name = c.relname)
join pg_catalog.pg_user u on (c.relowner = u.usesysid)
where t.table_schema='public';
```

Privileges for tables:
```sql
SELECT grantee, table_name, string_agg(privilege_type, ', ') AS privileges
FROM information_schema.role_table_grants
WHERE table_schema = 'public' OR table_name IN ('mytable')
GROUP BY grantee, table_name
ORDER BY grantee, table_name;
```

Tables the current user owns:
```sql
select table_catalog, table_schema, table_name, table_type
from information_schema.tables
where table_schema not in ('pg_catalog', 'information_schema');
```

Obejects the [current] user owns:
```sql
select
       case cls.relkind
         when 'r' then 'TABLE'
         when 'i' then 'INDEX'
         when 'S' then 'SEQUENCE'
         when 'v' then 'VIEW'
         when 'c' then 'TYPE'
         else cls.relkind::text
       end as object_type,
       nsp.nspname as object_schema,
       cls.relname as object_name,
       rol.rolname as owner
from pg_class cls
  join pg_roles rol on rol.oid = cls.relowner
  join pg_namespace nsp on nsp.oid = cls.relnamespace
where nsp.nspname not in ('information_schema', 'pg_catalog')
  and nsp.nspname not like 'pg_toast%'
  and rol.rolname = current_user  -- remove this if you want to see all objects
order by object_type, object_type, object_name;
```
Users with attributes:
```sql
SELECT u.usename AS "User name",
  u.usesysid AS "User ID",
  CASE WHEN u.usesuper AND u.usecreatedb THEN CAST('superuser, create
database' AS pg_catalog.text)
       WHEN u.usesuper THEN CAST('superuser' AS pg_catalog.text)
       WHEN u.usecreatedb THEN CAST('create database' AS
pg_catalog.text)
       ELSE CAST('' AS pg_catalog.text)
  END AS "Attributes"
FROM pg_catalog.pg_user u
ORDER BY 1;
```
