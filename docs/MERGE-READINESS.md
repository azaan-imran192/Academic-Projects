# Portfolio merge readiness

Presentation review: **20 October 2026**.

## Assessment

**Ready for the owner's review as an academic source portfolio, with the open items below explicitly retained.** This is not a production-release assessment. Do not merge without the owner's approval; PR #1 remains draft.

- All nine project areas are represented in the homepage, with links to their individual documentation.
- Homepage claims are drawn from the existing audited READMEs, original reports or recorded verification. Historical metrics and executed checks are clearly separated.
- The result preview reuses an original Building Height PNG. No application screenshots, model outputs, achievements or publication claims were fabricated.
- ParkinsonPal's 30 original files remain unchanged. No project source, algorithm, dataset, original report or experiment output changes in the presentation update.
- A custom repository banner is the only new homepage media asset. No commercial-template or proprietary-company material is introduced.
- The personal profile redesign is a separate local draft for approval, not a change to the public profile repository. Its project links use the verified source commit, so they work before this PR is merged.
- Existing model/build/integration evidence is reused; only presentation, navigation and preservation checks are repeated.

## Security and licensing — separate open items

| Item | Current disposition / action |
|---|---|
| Credentials previously exposed in upstream/history | New copies are sanitized. Owners should rotate/revoke any still-active values; rotation is not verified. This PR does not rewrite history or change live credentials. |
| Otis Admin PRO | Frontend remains excluded. Written redistribution permission or separately approved replacement is required before adding it. The backend portfolio can be reviewed independently. |
| Culinary development dependencies | Seven previously recorded development-tool advisories remain; a major-version migration needs separate implementation/verification. Prior production-only audits reported zero findings on their audit date. |
| Third-party code, models and data | No repository-wide license is asserted. NLP's missing standalone license notice, Building Height baseline licensing, dataset/model rights and third-party segmentation dependencies retain the limits in the security review. Broader reuse/relicensing requires appropriate rights. |
| HCI research materials | Owner confirmed consent and explicitly required unchanged preservation. The previously identified file-specific concern remains documented; no new exclusion or anonymization was performed. |

The full findings and affected paths remain in [SECURITY-REVIEW.md](SECURITY-REVIEW.md). Nothing in the presentation closes those findings or certifies deployment safety.

## Reproducibility and attribution still pending

- Full GPU training/benchmark reproduction and authorized research datasets/checkpoints.
- Live Gemini calls with the user's own key.
- CineLog SQL-backed desktop/API integration and the exact movie-data cleaning workflow.
- Culinary external-service integrations and optional missing UI assets.
- FYP segmentation/data integration and the complete FYP contribution statement.
- Complete Culinary/Mobile team rosters, where the available evidence does not establish them.

These limits are visible in the homepage and individual READMEs. They do not imply missing source imports or invented substitutes. See [verification](VERIFICATION.md), [remaining inputs](LOCAL-FILES-NEEDED.md) and the [completion checklist](CONSOLIDATION-CHECKLIST.md).

## Final presentation refinements

- Removed the obsolete root `Urdu News Text Classification - ML` placeholder as explicitly requested. Its committed blob contained only one newline byte; the completed project remains under `Machine-Learning/Urdu-News-Classification/`.
- Retained `Culinary Cloud - SE/README.md` as a compatibility pointer. The path predates consolidation (original README commit `2e054fa`); deleting it would break old folder/README URLs. Its relative destination resolves to the canonical Culinary project. No duplicate source application remains in that directory. External bookmarks cannot be exhaustively inventoried.
- Kept the homepage design and all completed project materials unchanged. Security/licensing findings and the Otis hold remain intact.
- The unpublished profile draft now emphasizes AI engineering, backend/full-stack work and research, with owner-supplied Royal Cyber module names at a non-proprietary contribution level. Cards contain one meaningful achievement each, and statistics are compact and collapsed.
- Checked the live GitHub README at desktop and mobile widths. The page fits the viewport; wide tables use GitHub's normal internal horizontal scrolling on phones.
- Checked the unpublished profile through GitHub's stateless GFM renderer, using styles observed on the live GitHub page. Cards, banner, icons and the statistics disclosure work at desktop/mobile widths. The unpublished banner is resolved locally for this preview; final profile-page integration can only be checked after separately approved publication.
