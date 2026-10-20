# Database setup and source mapping

Use a fresh, isolated **local** SQL Server instance. These scripts are retained coursework, not a production migration system. Nothing here was executed against an existing database during consolidation.

1. `create_table.sql` comes from Part 2. Its original automatic `ALTER DATABASE ... ROLLBACK IMMEDIATE` / `DROP DATABASE` reset was removed. It now uses SQLCMD `:ON ERROR EXIT` plus an existing-database guard and will stop rather than replace `CineLog`. Run through `sqlcmd -b` (or SQLCMD mode in SSMS); do not strip the guard/directive.
2. It builds schema/partitioning, imports `/var/opt/mssql/movies_utf8.csv`, generates the large synthetic workload, then creates triggers, procedures, functions, views and indexes. The CSV path is on the **SQL Server host**, not necessarily the desktop running the client. Inspect the staging-table column order and BULK INSERT options before supplying the authorized cleaned UTF-8 CSV. The original link is in `../data/DriveLinkToCSV.md`. No verified raw-to-cleaned transformation script exists in the archive.
3. Run `NewProcedures.sql` after successful Part 2 setup. It adds Part 3 indexes and application procedures. Two missing GO separators were repaired and exploratory calls, including an undefined procedure name, were commented. Some index creation is not idempotent; do not rerun blindly.
4. `extracredit.sql` is diagnostic (`@@VERSION`, `@@SERVERNAME`, database names). Kubernetes manifests are under `../deployment/extra-credit/`; they are optional, not a required extra numbered course part.

Example after explicitly configuring your own fresh local instance, credentials and data:

```powershell
# SQLCMDPASSWORD should contain your own local password; do not commit it.
sqlcmd -S localhost,1433 -U YOUR_LOCAL_USER -C -b -i database/create_table.sql
sqlcmd -S localhost,1433 -U YOUR_LOCAL_USER -C -b -i database/NewProcedures.sql
```

This can create a million synthetic reviews and consume substantial resources. It is not a small smoke-test seed. No automatic database deletion command remains in the published setup. To preserve existing work, use another isolated instance if `CineLog` already exists; resetting any database is a separate owner decision.

The reports and original source hashes preserve the original coursework provenance. The published script differs only in the protective setup block; business SQL is retained. Known trigger/mode-switch limitations are described in the project README. Database-backed execution is recorded separately from compilation.
