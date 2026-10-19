# """
# Management command: sync_images

# Place this file at:
#     traits/management/commands/sync_images.py

# Usage:
#     python manage.py sync_images
#     python manage.py sync_images --limit 50
#     python manage.py sync_images --no-traits
#     python manage.py sync_images --dry-run
#     python manage.py sync_images --since 2025-01-01   # only sync images from this date onwards

# Credentials via environment variables (never hardcode):
#     export REMOTE_API_USER=user1
#     export REMOTE_API_PASS=your_password

# Recommended workflow for first-time bulk sync:
#     1. python manage.py sync_images --since 2025-01-01 --no-traits --dry-run
#     2. python manage.py sync_images --since 2025-01-01 --no-traits
#     3. python manage.py compute_traits
# """

# import os
# from datetime import date
# from pathlib import Path

# import requests
# from django.conf import settings
# from django.core.management.base import BaseCommand

# from traits.models import PlantImage, PlantTraits
# from traits.pipeline.segmenter import run_segmentation_for_image
# from traits.engine_b.traits_from_segmented import (
#     compute_traits_from_segmented_dir,
#     compute_plant_traits_from_raw_image,
# )

# REMOTE_BASE     = "https://research-api.example.invalid"
# TOKEN_URL       = f"{REMOTE_BASE}/accounts/api/token/login/"
# REMOTE_API      = f"{REMOTE_BASE}/core/api/image/"
# REQUEST_TIMEOUT = 30

# # Images before this date have unreliable filenames (just CAM1.jpg with no timestamp)
# # so we skip them by default unless --since is set to an earlier date
# DEFAULT_SINCE = "2025-01-01"


# class Command(BaseCommand):
#     help = "Sync new plant images from the remote camera server and compute traits"

#     def add_arguments(self, parser):
#         parser.add_argument("--limit",     type=int,  default=None,
#                             help="Max number of NEW images to download")
#         parser.add_argument("--no-traits", action="store_true", default=False,
#                             help="Download images only; skip trait computation")
#         parser.add_argument("--dry-run",   action="store_true", default=False,
#                             help="Print what would be downloaded without saving anything")
#         parser.add_argument("--plant-id",  type=int,  default=1,
#                             help="plant_id to assign to synced images (default: 1)")
#         parser.add_argument("--since",     type=str,  default=DEFAULT_SINCE,
#                             help=f"Only sync images on or after this date (YYYY-MM-DD). "
#                                  f"Default: {DEFAULT_SINCE}")

#     def handle(self, *args, **options):
#         limit      = options["limit"]
#         no_traits  = options["no_traits"]
#         dry_run    = options["dry_run"]
#         plant_id   = options["plant_id"]
#         since_str  = options["since"]
#         media_root = Path(settings.MEDIA_ROOT)

#         # Parse --since date
#         try:
#             since_date = date.fromisoformat(since_str)
#         except ValueError:
#             self.stdout.write(self.style.ERROR(
#                 f"Invalid --since date '{since_str}'. Use YYYY-MM-DD format."
#             ))
#             return

#         # Load credentials from environment variables
#         username = os.environ.get("REMOTE_API_USER", "")
#         password = os.environ.get("REMOTE_API_PASS", "")

#         if not username or not password:
#             self.stdout.write(self.style.ERROR(
#                 "Missing credentials. Set environment variables:\n"
#                 "  export REMOTE_API_USER=your_username\n"
#                 "  export REMOTE_API_PASS=your_password"
#             ))
#             return

#         # Authenticate and get token
#         self.stdout.write("Authenticating with remote server ...")
#         try:
#             token_resp = requests.post(
#                 TOKEN_URL,
#                 data={"username": username, "password": password},
#                 timeout=REQUEST_TIMEOUT,
#             )
#             token_resp.raise_for_status()
#         except requests.RequestException as e:
#             self.stdout.write(self.style.ERROR(f"Authentication failed: {e}"))
#             return

#         token_data = token_resp.json()
#         token = token_data.get("auth_token") or token_data.get("token")

#         if not token:
#             self.stdout.write(self.style.ERROR(
#                 f"Could not extract token from response: {token_data}"
#             ))
#             return

#         self.stdout.write(self.style.SUCCESS("Authenticated successfully."))
#         headers = {"Authorization": f"Token {token}"}

#         if dry_run:
#             self.stdout.write(self.style.WARNING("DRY RUN - nothing will be saved."))

#         self.stdout.write(
#             f"Fetching images from {REMOTE_API} "
#             f"(filtering to on/after {since_str}) ..."
#         )

#         # Filenames already in local DB for deduplication
#         existing_filenames = set(PlantImage.objects.values_list("filename", flat=True))
#         self.stdout.write(f"Found {len(existing_filenames)} existing image(s) in local DB.")

#         new_items   = []
#         skipped_old = 0
#         url         = REMOTE_API

#         # Paginate through all pages of the remote API
#         while url:
#             try:
#                 resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
#                 resp.raise_for_status()
#             except requests.RequestException as e:
#                 self.stdout.write(self.style.ERROR(f"Failed to fetch {url}: {e}"))
#                 return

#             data    = resp.json()
#             results = data.get("results", [])

#             for item in results:
#                 item_date = date.fromisoformat(item["date"][:10])

#                 # Skip images older than --since
#                 if item_date < since_date:
#                     skipped_old += 1
#                     continue

#                 filename = item["file"].split("/")[-1]

#                 # Skip if already in local DB
#                 if filename in existing_filenames:
#                     continue

#                 new_items.append(item)

#                 if limit and len(new_items) >= limit:
#                     break

#             if limit and len(new_items) >= limit:
#                 break

#             url = data.get("next")

#         if skipped_old:
#             self.stdout.write(
#                 f"Skipped {skipped_old} image(s) older than {since_str} "
#                 f"(use --since YYYY-MM-DD to include them)."
#             )

#         if not new_items:
#             self.stdout.write(self.style.SUCCESS("Already up to date. Nothing to sync."))
#             return

#         self.stdout.write(f"Found {len(new_items)} new image(s) to sync.")

#         # Dry run: just print what would happen
#         if dry_run:
#             for item in new_items:
#                 filename = item["file"].split("/")[-1]
#                 date_str = item["date"][:10]
#                 self.stdout.write(
#                     f"  [DRY RUN] Would download: raw_images/{date_str}/{filename}"
#                 )
#             self.stdout.write(self.style.WARNING(
#                 f"Dry run complete. {len(new_items)} image(s) would be downloaded."
#             ))
#             return

#         # Download and register each new image
#         downloaded = []

#         for item in new_items:
#             file_url = item["file"]
#             filename = file_url.split("/")[-1]
#             camera   = filename.split("_")[0]   # CAM1, CAM2, CAM3
#             date_str = item["date"][:10]         # 2025-03-02
#             rel_path = f"raw_images/{date_str}/{filename}"
#             abs_path = media_root / rel_path

#             abs_path.parent.mkdir(parents=True, exist_ok=True)

#             if not abs_path.exists():
#                 try:
#                     img_resp = requests.get(
#                         file_url, headers=headers, timeout=REQUEST_TIMEOUT
#                     )
#                     img_resp.raise_for_status()
#                     abs_path.write_bytes(img_resp.content)
#                     self.stdout.write(f"  Downloaded: {rel_path}")
#                 except requests.RequestException as e:
#                     self.stdout.write(self.style.WARNING(
#                         f"  Failed to download {file_url}: {e}"
#                     ))
#                     continue
#             else:
#                 self.stdout.write(f"  Already on disk, registering: {rel_path}")

#             plant_img, created = PlantImage.objects.update_or_create(
#                 rel_path=rel_path,
#                 defaults={
#                     "plant_id":    plant_id,
#                     "date_folder": date_str,
#                     "camera":      camera,
#                     "filename":    filename,
#                 },
#             )

#             verb = "Created" if created else "Updated"
#             self.stdout.write(f"  {verb} PlantImage id={plant_img.id} -> {filename}")
#             downloaded.append(plant_img)

#         self.stdout.write(self.style.SUCCESS(f"\nSynced {len(downloaded)} image(s)."))

#         # Trait computation
#         if no_traits:
#             self.stdout.write(
#                 "Skipping trait computation (--no-traits).\n"
#                 "Run 'python manage.py compute_traits' when ready."
#             )
#             return

#         if not downloaded:
#             return

#         self.stdout.write(f"\nComputing traits for {len(downloaded)} image(s) ...")
#         done, failed = 0, 0

#         for plant_img in downloaded:
#             abs_path = media_root / plant_img.rel_path

#             if not abs_path.exists():
#                 self.stdout.write(self.style.WARNING(
#                     f"  File missing, skipping: {abs_path}"
#                 ))
#                 failed += 1
#                 continue

#             try:
#                 plant_traits  = compute_plant_traits_from_raw_image(abs_path)
#                 seg_info      = run_segmentation_for_image(abs_path, media_root)
#                 segmented_dir = Path(seg_info["segmented_dir"])
#                 leaf_traits   = compute_traits_from_segmented_dir(segmented_dir)

#                 PlantTraits.objects.update_or_create(
#                     image=plant_img,
#                     defaults={"traits": {"plant": plant_traits, "leaf": leaf_traits}},
#                 )

#                 self.stdout.write(self.style.SUCCESS(
#                     f"  Traits done: image id={plant_img.id} "
#                     f"({leaf_traits.get('leaf_count', 0)} leaves)"
#                 ))
#                 done += 1

#             except Exception as e:
#                 self.stdout.write(self.style.WARNING(
#                     f"  Failed for id={plant_img.id}: {e}"
#                 ))
#                 failed += 1

#         self.stdout.write("")
#         self.stdout.write(self.style.SUCCESS(
#             f"All done.  Computed: {done} | Failed: {failed}"
#         ))

"""
Management command: sync_images

Syncs new images from the remote camera server, computes traits,
and saves to BOTH local SQLite AND remote MySQL (pheno_lums).

Place at: traits/management/commands/sync_images.py

Usage:
    python manage.py sync_images
    python manage.py sync_images --limit 50
    python manage.py sync_images --no-traits
    python manage.py sync_images --dry-run
    python manage.py sync_images --since 2025-01-01

Credentials via environment variables:
    export REMOTE_API_USER=user1
    export REMOTE_API_PASS=your_password

For fully automatic running, add to crontab:
    crontab -e
    */30 * * * * cd /path/to/plant_backend && source venv/bin/activate && python manage.py sync_images >> logs/sync.log 2>&1
"""

import os
from datetime import date
from pathlib import Path

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from traits.models import PlantImage, PlantTraits, PlantTraitsMySQL
from traits.pipeline.segmenter import run_segmentation_for_image
from traits.engine_b.traits_from_segmented import (
    compute_traits_from_segmented_dir,
    compute_plant_traits_from_raw_image,
)

REMOTE_BASE = os.environ.get("REMOTE_API_BASE", "https://research-api.example.invalid").rstrip("/")
TOKEN_URL       = f"{REMOTE_BASE}/accounts/api/token/login/"
REMOTE_API      = f"{REMOTE_BASE}/core/api/image/"
REQUEST_TIMEOUT = 30
DEFAULT_SINCE   = "2025-01-01"


def _push_to_mysql(img, plant_traits, leaf_traits):
    """Push flattened traits to remote MySQL. Returns True on success."""
    try:
        PlantTraitsMySQL.objects.update_or_create(
            image_id=img.id,
            defaults={
                "plant_id":     img.plant_id,
                "date_folder":  img.date_folder,
                "camera":       img.camera,
                "filename":     img.filename,

                "plant_leaf_area_px":         plant_traits.get("leaf_area_px", 0),
                "plant_aspect_ratio":         plant_traits.get("aspect_ratio", 0),
                "plant_solidity":             plant_traits.get("solidity", 0),
                "plant_vigor_pct":            plant_traits.get("vigor_pct", 0),
                "plant_color_uniformity_pct": plant_traits.get("average_color_uniformity_pct", 0),
                "plant_chlorophyll_level":    plant_traits.get("chlorophyll_level", 0),
                "plant_texture_entropy":      plant_traits.get("texture_entropy", 0),
                "plant_chlorosis_pct":        plant_traits.get("chlorosis_pct", 0),
                "plant_health_score":         plant_traits.get("health_score", 0),

                "leaf_count":                 leaf_traits.get("leaf_count", 0),
                "leaf_area_px":               leaf_traits.get("leaf_area_px", 0),
                "leaf_aspect_ratio":          leaf_traits.get("aspect_ratio", 0),
                "leaf_solidity":              leaf_traits.get("solidity", 0),
                "leaf_vigor_pct":             leaf_traits.get("vigor_pct", 0),
                "leaf_color_uniformity_pct":  leaf_traits.get("average_color_uniformity_pct", 0),
                "leaf_chlorophyll_level":     leaf_traits.get("chlorophyll_level", 0),
                "leaf_texture_entropy":       leaf_traits.get("texture_entropy", 0),
                "leaf_chlorosis_pct":         leaf_traits.get("chlorosis_pct", 0),
                "leaf_health_score":          leaf_traits.get("health_score", 0),
            },
        )
        return True
    except Exception as e:
        return str(e)


class Command(BaseCommand):
    help = "Sync new plant images from remote camera server → compute traits → save to SQLite + MySQL"

    def add_arguments(self, parser):
        parser.add_argument("--limit",      type=int,  default=None)
        parser.add_argument("--no-traits",  action="store_true", default=False)
        parser.add_argument("--dry-run",    action="store_true", default=False)
        parser.add_argument("--plant-id",   type=int,  default=1)
        parser.add_argument("--since",      type=str,  default=DEFAULT_SINCE)
        parser.add_argument("--skip-mysql", action="store_true", default=False,
                            help="Skip MySQL push (useful if tunnel is not open)")

    def handle(self, *args, **options):
        limit      = options["limit"]
        no_traits  = options["no_traits"]
        dry_run    = options["dry_run"]
        plant_id   = options["plant_id"]
        since_str  = options["since"]
        skip_mysql = options["skip_mysql"]
        media_root = Path(settings.MEDIA_ROOT)

        try:
            since_date = date.fromisoformat(since_str)
        except ValueError:
            self.stdout.write(self.style.ERROR(
                f"Invalid --since date '{since_str}'. Use YYYY-MM-DD format."
            ))
            return

        username = os.environ.get("REMOTE_API_USER", "")
        password = os.environ.get("REMOTE_API_PASS", "")

        if not username or not password:
            self.stdout.write(self.style.ERROR(
                "Missing credentials. Set:\n"
                "  export REMOTE_API_USER=your_username\n"
                "  export REMOTE_API_PASS=your_password"
            ))
            return

        # Authenticate
        self.stdout.write("Authenticating with remote server ...")
        try:
            token_resp = requests.post(
                TOKEN_URL,
                data={"username": username, "password": password},
                timeout=REQUEST_TIMEOUT,
            )
            token_resp.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Authentication failed: {e}"))
            return

        token_data = token_resp.json()
        token = token_data.get("auth_token") or token_data.get("token")

        if not token:
            self.stdout.write(self.style.ERROR(
                f"Could not extract token: {token_data}"
            ))
            return

        self.stdout.write(self.style.SUCCESS("Authenticated."))
        headers = {"Authorization": f"Token {token}"}

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN — nothing will be saved."))

        # Fetch new images
        existing_filenames = set(PlantImage.objects.values_list("filename", flat=True))
        self.stdout.write(f"{len(existing_filenames)} existing images in local DB.")

        new_items   = []
        skipped_old = 0
        url         = REMOTE_API

        while url:
            try:
                resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
                resp.raise_for_status()
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Fetch failed: {e}"))
                return

            data    = resp.json()
            results = data.get("results", [])

            for item in results:
                item_date = date.fromisoformat(item["date"][:10])
                if item_date < since_date:
                    skipped_old += 1
                    continue

                filename = item["file"].split("/")[-1]
                if filename in existing_filenames:
                    continue

                new_items.append(item)
                if limit and len(new_items) >= limit:
                    break

            if limit and len(new_items) >= limit:
                break
            url = data.get("next")

        if skipped_old:
            self.stdout.write(f"Skipped {skipped_old} image(s) older than {since_str}.")

        if not new_items:
            self.stdout.write(self.style.SUCCESS("Already up to date. Nothing to sync."))
            return

        self.stdout.write(f"Found {len(new_items)} new image(s) to sync.")

        if dry_run:
            for item in new_items:
                fn       = item["file"].split("/")[-1]
                date_str = item["date"][:10]
                self.stdout.write(f"  [DRY RUN] Would download: raw_images/{date_str}/{fn}")
            return

        # Download + register
        downloaded = []

        for item in new_items:
            file_url = item["file"]
            filename = file_url.split("/")[-1]
            camera   = filename.split("_")[0]
            date_str = item["date"][:10]
            rel_path = f"raw_images/{date_str}/{filename}"
            abs_path = media_root / rel_path

            abs_path.parent.mkdir(parents=True, exist_ok=True)

            if not abs_path.exists():
                try:
                    img_resp = requests.get(file_url, headers=headers, timeout=REQUEST_TIMEOUT)
                    img_resp.raise_for_status()
                    abs_path.write_bytes(img_resp.content)
                    self.stdout.write(f"  Downloaded: {rel_path}")
                except requests.RequestException as e:
                    self.stdout.write(self.style.WARNING(f"  Download failed: {e}"))
                    continue
            else:
                self.stdout.write(f"  Already on disk: {rel_path}")

            plant_img, created = PlantImage.objects.update_or_create(
                rel_path=rel_path,
                defaults={
                    "plant_id":    plant_id,
                    "date_folder": date_str,
                    "camera":      camera,
                    "filename":    filename,
                },
            )
            verb = "Created" if created else "Updated"
            self.stdout.write(f"  {verb} PlantImage id={plant_img.id}")
            downloaded.append(plant_img)

        self.stdout.write(self.style.SUCCESS(f"\nSynced {len(downloaded)} image(s)."))

        if no_traits:
            self.stdout.write("Skipping traits (--no-traits). Run compute_traits manually.")
            return

        if not downloaded:
            return

        # Compute traits + push to SQLite + MySQL
        self.stdout.write(f"\nComputing traits for {len(downloaded)} image(s) ...")
        done = 0
        failed = 0
        mysql_failed = 0

        for plant_img in downloaded:
            abs_path = media_root / plant_img.rel_path

            if not abs_path.exists():
                self.stdout.write(self.style.WARNING(f"  Missing: {abs_path}"))
                failed += 1
                continue

            try:
                plant_traits  = compute_plant_traits_from_raw_image(abs_path)
                seg_info      = run_segmentation_for_image(abs_path, media_root)
                segmented_dir = Path(seg_info["segmented_dir"])
                leaf_traits   = compute_traits_from_segmented_dir(segmented_dir)

                # Save to SQLite
                PlantTraits.objects.update_or_create(
                    image=plant_img,
                    defaults={"traits": {"plant": plant_traits, "leaf": leaf_traits}},
                )

                # Save to MySQL
                if not skip_mysql:
                    result = _push_to_mysql(plant_img, plant_traits, leaf_traits)
                    if result is True:
                        mysql_status = "SQLite + MySQL ✓"
                    else:
                        mysql_status = f"SQLite only (MySQL error: {result})"
                        mysql_failed += 1
                else:
                    mysql_status = "SQLite only (--skip-mysql)"

                self.stdout.write(self.style.SUCCESS(
                    f"  Traits done: id={plant_img.id} "
                    f"({leaf_traits.get('leaf_count', 0)} leaves) | {mysql_status}"
                ))
                done += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  Failed id={plant_img.id}: {e}"))
                failed += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"All done. Computed: {done} | Failed: {failed}"
            + (f" | MySQL failures: {mysql_failed}" if mysql_failed else "")
        ))