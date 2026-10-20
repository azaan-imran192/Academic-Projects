# Security, privacy, and redistribution review

Date: **19 October 2026**. This is a source review with pattern-based scanning, not a guarantee that every secret, privacy issue, dependency vulnerability, or license condition has been discovered. No credential values are included.

## Findings and action

| Priority | Location / issue | Action in consolidation | Owner action remaining |
|---|---|---|---|
| High | Source dashboard `plant_backend/config/settings.py`: literal Django secret and database password; debug enabled | Imported copy requires environment secret, environment DB credentials, defaults debug off, uses local SQLite unless MySQL explicitly enabled | Rotate/revoke exposed values wherever used; inspect use and logs; invalidate sessions as appropriate |
| High | Shared Culinary `frontend/.env`: Google API-key-shaped value | Environment file omitted; only non-secret frontend API URL template included | Key owner should rotate/revoke it and review usage; never ship it in browser variables |
| High | Dashboard `plant_phenotyping/package.json` and template source: Otis Admin PRO | Entire frontend held at owner's direction | Obtain written public redistribution permission or authorize a replacement |
| Review requested | `Human-Computer-Interaction/ParkinsonPal/01-User-Research/Group08_UserResearch_2025.pdf` contains named interview quotations; its `.docx` counterpart warrants the same review | All original files and READMEs relocated unchanged, as explicitly requested after the concern was reported | Owner confirms consent and permissions. Any anonymization, replacement, exclusion, removal, or history cleanup requires separate explicit approval. Composite design reports may repeat research details; this is a review item, not a confirmed finding about every file. |
| Medium | Source dashboard SQLite database and captured media | Excluded; fresh empty local verification database is ignored | Confirm research ownership/data release before any future import |
| Medium | Culinary uploaded user images and generated cache | Excluded | Import only cleared artifacts if needed |
| Medium | Mobile survey timestamps and notebook row previews | Timestamps removed; saved cell outputs cleared | Respect consent and avoid re-identification from demographic combinations |
| Medium | Source MySQL version-support bypass and infrastructure endpoints | Bypass removed in imported copy; external host replaced with configurable placeholder | Use supported DB version; explicitly configure only authorized infrastructure |
| Medium | Culinary fallback JWT secret | Fallback removed; missing configuration fails closed | Set strong unique development secrets; review sessions/OAuth/upload handling before deployment |
| Medium | Model binaries, research datasets and vendor source | Excluded; source model references retained | Retrieve separately under applicable terms; no ordinary Git weight commits |

## Redistribution boundaries

- The owner confirmed HCI/survey consent and news-corpus redistribution permission in this chat on 19 October 2026. This does not justify disclosing participant identifiers or attaching a blanket software license to participant/news data.
- The plant-classification MIT notice is preserved. Both MIT notices from the shared repository are preserved without conflict markers. No new repository-wide license overrides third-party or dataset rights.
- Creative Tim's [license page](https://www.creative-tim.com/license), checked on the audit date, requires written consent for public delivery of its source in open-source projects. Owner instructed that frontend remain on hold.
- The original dashboard vendors GroundingDINO (Apache-2.0 notice) and FastSAM/Ultralytics (AGPL-3.0 notice). These trees are not recopied. Installing them separately still requires observing their license conditions.
- No proprietary-company material, CSaLT research, interview recordings, completed consent forms, or unrelated shared projects were added. Binary Figma internals and arbitrary image/document metadata are not exhaustively certified.

## Credential/history remediation

The Culinary key-shaped value is also present in this repository's existing historical archive at commit `e1889e2`, path `Culinary Cloud - SE/code files.zip`, member `CulinaryCloud_RecipeSharingPlatform/frontend/.env`. The archive is not restored in this change. This finding reinforces the need for owner-led rotation; deleting the current file does not erase historical exposure.

The history scan covered 836 unique text blobs across the eight inspected clones, with a 15 MB text-blob limit and shared-repository scope restricted to the two authorized projects and root files. Historical ZIP members were also inspected. Binary documents, images, and Figma internals are not comprehensively covered by credential patterns.

Replacing credentials in a new snapshot does not remove them from the original public repositories or Git history. Treat exposed values as compromised unless their owners establish they were never usable. Rotation/revocation should precede any optional history cleanup. Check hosting environments, database accounts, sessions, logs, and cached copies. No production settings, credentials, remote datasets, repository visibility, or source history were changed by this consolidation.

The owner explicitly directed preservation of the complete ParkinsonPal project, confirmed consent and permissions, and instructed that privacy concerns be reported before any content edits. All 30 original files, including research/design reports, Figma, questionnaires, evaluation materials and READMEs, are relocated unchanged. The named-quotation concern is recorded above without repeating names. No anonymization, exclusion, replacement or history cleanup is performed. This relocation does not independently certify the scope of participant consent.

## Large files

Existing HCI PDFs and editable design documents are already part of the target's history; some exceed 10 MB. Relocated standalone PDFs reuse existing content rather than adding duplicate archives. Checkpoint pointers are converted into model-reference metadata so no absent LFS object is promised by this repository. Future model releases should use LFS or an appropriate artifact host only after rights and size review; no LFS binary upload was made here.

## Dependency findings

Compatible Culinary dependency updates and removal of an unused backend Tailwind dependency were applied. Final backend and frontend production-only npm audits each report zero vulnerabilities on the audit date. The frontend full audit still reports seven development dependency advisories (five high, two moderate), associated with the Tailwind 3 build dependency tree. The suggested resolution crosses a major Tailwind version and is deferred for a separately verified migration. Run builds only with trusted project inputs; these results do not establish deployment readiness or replace application security review.

## Three-project extension — 20 October 2026

- **Academic Gemini demo configuration:** `Natural-Language-Processing/Urdu-Roman-Urdu-LLM-Safety/notebooks/4_end_to_end_pipeline_with_gemini_UPDATED.ipynb` originally contained a demonstration key. The imported cell now reads `GOOGLE_API_KEY`; the Streamlit demo supports environment/Streamlit secrets and a masked field. Tests no longer print key fragments. No actual key is copied, tested or revoked. If the old demo key is still active, revocation/rotation is sensible; this does not block the project import. Ahmad's repository is unchanged.
- **CineLog local SQL credentials:** source `Project/backend/Cinelog-DBProject/CineLog.API/appsettings.json`, its duplicated combined/Part 3 variants, and `Project/kubernetes_setup.txt` contained database connection/secret values. Imported configuration uses an empty tracked connection string plus environment override; deployment notes use the owner's environment value. Historical backend patch omits the credential-bearing configuration diff. Consider changing old values if still used.
- **Database preservation:** the source Part 2 reset block was replaced by a SQLCMD stop-on-error/existing-database guard, with no automatic database deletion or forced rollback. No SQL or Kubernetes command was executed against user infrastructure. Additional procedure scripts remain manual coursework setup, not production migrations.
- **Dependencies:** the CineLog OpenAPI dependency was raised to the patched 2.7.5 line for [GHSA-v5pm-xwqc-g5wc](https://github.com/advisories/GHSA-v5pm-xwqc-g5wc), and reverified. Earlier Culinary development-tool advisories remain as documented above.
- **External assets:** all NLP data/model LFS objects remain external; only hashes/sizes/availability and a checksum-validating local importer are published. CineLog's two large movie CSVs (1,106,372,806 bytes together), embedded Git databases and build/IDE artifacts are excluded. No raw building dataset or weights are imported. Corpus/movie/model rights are not inferred from public availability.
- **Attribution/licensing:** NLP source README claims MIT but has no standalone license notice in the audited snapshot. Building Height credits the DFC2023 baseline and HGDNet; no top-level upstream baseline license grant was found. CineLog has no explicit blanket license in the supplied archive. No license is invented for third-party code/data; original academic authorship and source references are retained, with broader reuse/relicensing limitations stated.
- **Known academic limitations:** CineLog's numeric user selector is not authentication; its API/mode switch is suitable only for trusted local demonstration. NLP output checks can classify a response as sanitize while the UI still displays the raw response; this existing behavior is explicitly documented rather than represented as a reliable safety guarantee.

All new notebook result outputs, course PDFs and genuine Building Height PNGs are preserved. ParkinsonPal has no new changes. No source repository, original archive, production credential, deployment or history was modified.
