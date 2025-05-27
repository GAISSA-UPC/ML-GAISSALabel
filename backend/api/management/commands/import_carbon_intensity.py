from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Country, CarbonIntensity
import csv, io, sys, urllib.request, random, string


class Command(BaseCommand):
    help = "Import carbon intensity data from CSV file or URL."

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, help="Path to CSV file")
        parser.add_argument(
            "--url",
            type=str,
            help="URL to download CSV data",
            default="https://ourworldindata.org/grapher/carbon-intensity-electricity.csv?v=1&csvType=full&useColumnShortNames=true",
        )
        parser.add_argument("--verbose", action="store_true")

    def handle(self, *args, **opts):
        verbose = opts["verbose"]

        # Import CSV data from file or URL
        csv_data = self._get_csv_data(opts.get("file"), opts.get("url"), verbose)
        if not csv_data:
            self.stderr.write("No CSV data available.")
            return

        # Extract and import data
        stats = self._import_data(csv_data, verbose)

        self.stdout.write(
            self.style.SUCCESS(
                f"Import done: {stats['countries_created']} countries created, "
                f"{stats['intensity_records_created']} records created, "
                f"{stats['intensity_records_updated']} updated."
            )
        )

    def _get_csv_data(self, file_path, url, verbose):
        """
        Retrieve CSV data from a source. Returns the CSV content as a string.
        """
        try:
            if file_path:
                with open(file_path, "r", encoding="utf-8") as f:
                    if verbose:
                        self.stdout.write(f"Reading from file: {file_path}")
                    return f.read()
            elif url:
                if verbose:
                    self.stdout.write(f"Downloading from URL: {url}")
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                return urllib.request.urlopen(req).read().decode("utf-8")
            else:
                return sys.stdin.read()
        except Exception as e:
            self.stderr.write(f"Error reading CSV: {e}")
            return None

    def _import_data(self, csv_data, verbose):
        stats = {
            "countries_created": 0,
            "intensity_records_created": 0,
            "intensity_records_updated": 0,
        }
        reader = csv.DictReader(io.StringIO(csv_data))
        countries = {c.name: c for c in Country.objects.all()}
        codes = {c.country_code: c for c in Country.objects.all() if c.country_code}

        with transaction.atomic():
            for row in reader:
                name, code, year, intensity = self._extract_row(row)
                if not (name and year and intensity):
                    continue

                name = self._clean_name(name)
                code = code or self._gen_code(name)
                country = countries.get(name) or codes.get(code)

                if not country:
                    code = self._ensure_unique_code(code, codes)
                    country = Country.objects.create(name=name, country_code=code)
                    countries[name] = country
                    codes[code] = country
                    stats["countries_created"] += 1
                    if verbose:
                        self.stdout.write(f"Created country: {name} ({code})")

                obj, created = CarbonIntensity.objects.update_or_create(
                    country=country,
                    data_year=int(year),
                    defaults={"carbon_intensity": float(intensity)},
                )
                stats[
                    (
                        "intensity_records_created"
                        if created
                        else "intensity_records_updated"
                    )
                ] += 1
        return stats

    def _extract_row(self, row):
        code = row.get("Code", "")
        # Remove OWID_ prefix from country code if present
        if code and code.startswith("OWID_"):
            code = code[5:]

        return (
            row.get("Entity"),
            code[:5],
            row.get("Year"),
            row.get("co2_intensity__gco2_kwh"),
        )

    def _clean_name(self, name):
        """
        Clean up country name by removing tags and extra information.
        """
        return name.split("(")[0].strip() if name else name

    def _gen_code(self, country_name):
        """
        Generate a 5-letter country code from the country name.
        """
        words = country_name.split()
        if len(words) > 1:
            # For multi-word names, use first letters of the first 3 words
            code_chars = [word[0] for word in words[:5]]
            country_code = "".join(code_chars).upper()
        else:
            # For single word names, use first 3 letters
            country_code = country_name[:5].upper()

        return country_code

    def _ensure_unique_code(self, base, existing):
        base = base[:5].upper()
        if base not in existing:
            return base
        for i in range(1, 100):
            alt = f"{base[:3]}{i}"
            if alt not in existing:
                return alt
        raise ValueError(
            "Unable to generate a unique country code after 100 attempts for base: "
            + base
        )
