# Extra credit: SQL Server on Kubernetes

Preserves the original `pvc.yaml`, `sqldeployment.yaml` and setup walkthrough from the separately packaged extra-credit work. The same files occur at the archive root. Original notes label this “PHASE 4”; the portfolio keeps the supplied distinction of Parts 1–3 plus extra credit.

The deployment uses SQL Server 2022 Developer, an 8 GiB PVC and a Secret reference for `MSSQL_SA_PASSWORD`. Supply your own strong local password through the environment before following the PowerShell walkthrough. No password is committed. SQL Server EULA/Developer-edition terms apply. Inspect the NodePort exposure and resource requirements in your own local cluster before deployment; manifests were not applied during consolidation. The optional pod-deletion demonstration is a manual coursework self-healing exercise and was not executed.
