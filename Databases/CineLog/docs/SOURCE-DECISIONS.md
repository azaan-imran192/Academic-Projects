# Source decisions

Canonical source paths are listed in the main project README and repository import manifest. The alternate combined-tree backend differs in 36 files. Its nonidentical implementation is retained in `historical-backend-variant.patch` for comparison, not automatic application. The credential-bearing `appsettings.json` difference is intentionally omitted; the published API obtains credentials from the environment. All originals remain in the supplied archive.

The root `Cinelog-DBProject` and `Group10_P3/Cinelog-DBProject` trees match byte-for-byte for reviewed source. Part 2 and Part 3 ZIPs repeat unpacked submissions. Extra-credit ZIP repeats the three root deployment files. The separate backend adds `NewProcedures.sql` and `extracredit.sql` and active EF/SP switching. Desktop DTO/model classes are retained because the frontend is a separately compiled project, not mistaken for redundant backend files.
