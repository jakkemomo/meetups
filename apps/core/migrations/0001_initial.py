# Generated by Django 4.2.3 on 2024-09-07 07:59

import autoslug.fields
import cities_light.abstract_models
import cities_light.validators
import django.contrib.gis.db.models.fields
import django.contrib.postgres.indexes
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies: list[tuple[str, str]] = []

    operations = [
        TrigramExtension(),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=200)),
                ("name_ascii", models.CharField(blank=True, db_index=True, max_length=200)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(editable=False, populate_from="name_ascii"),
                ),
                ("geoname_id", models.IntegerField(blank=True, null=True, unique=True)),
                ("alternate_names", models.TextField(blank=True, default="", null=True)),
                ("code2", models.CharField(blank=True, max_length=2, null=True, unique=True)),
                ("code3", models.CharField(blank=True, max_length=3, null=True, unique=True)),
                (
                    "continent",
                    models.CharField(
                        choices=[
                            ("OC", "Oceania"),
                            ("EU", "Europe"),
                            ("AF", "Africa"),
                            ("NA", "North America"),
                            ("AN", "Antarctica"),
                            ("SA", "South America"),
                            ("AS", "Asia"),
                        ],
                        db_index=True,
                        max_length=2,
                    ),
                ),
                ("tld", models.CharField(blank=True, db_index=True, max_length=5)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={"verbose_name_plural": "countries", "ordering": ["name"], "abstract": False},
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=200)),
                ("name_ascii", models.CharField(blank=True, db_index=True, max_length=200)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(editable=False, populate_from="name_ascii"),
                ),
                ("geoname_id", models.IntegerField(blank=True, null=True, unique=True)),
                ("alternate_names", models.TextField(blank=True, default="", null=True)),
                ("display_name", models.CharField(max_length=200)),
                (
                    "geoname_code",
                    models.CharField(blank=True, db_index=True, max_length=50, null=True),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.country"
                    ),
                ),
            ],
            options={
                "verbose_name": "region/state",
                "verbose_name_plural": "regions/states",
                "ordering": ["name"],
                "abstract": False,
                "unique_together": {("country", "name"), ("country", "slug")},
            },
        ),
        migrations.CreateModel(
            name="SubRegion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=200)),
                ("name_ascii", models.CharField(blank=True, db_index=True, max_length=200)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(editable=False, populate_from="name_ascii"),
                ),
                ("geoname_id", models.IntegerField(blank=True, null=True, unique=True)),
                ("alternate_names", models.TextField(blank=True, default="", null=True)),
                ("display_name", models.CharField(max_length=200)),
                (
                    "geoname_code",
                    models.CharField(blank=True, db_index=True, max_length=50, null=True),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.country"
                    ),
                ),
                (
                    "region",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.region",
                    ),
                ),
            ],
            options={
                "verbose_name": "SubRegion",
                "verbose_name_plural": "SubRegions",
                "ordering": ["name"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=200)),
                ("name_ru", models.CharField(db_index=True, max_length=200, null=True)),
                ("name_en", models.CharField(db_index=True, max_length=200, null=True)),
                ("name_ascii", models.CharField(blank=True, db_index=True, max_length=200)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(editable=False, populate_from="name_ascii"),
                ),
                ("geoname_id", models.IntegerField(blank=True, null=True, unique=True)),
                ("alternate_names", models.TextField(blank=True, default="", null=True)),
                ("display_name", models.CharField(max_length=200)),
                ("display_name_ru", models.CharField(max_length=200, null=True)),
                ("display_name_en", models.CharField(max_length=200, null=True)),
                (
                    "search_names",
                    cities_light.abstract_models.ToSearchTextField(
                        blank=True, db_index=True, default="", max_length=4000
                    ),
                ),
                (
                    "latitude",
                    models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True),
                ),
                (
                    "longitude",
                    models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True),
                ),
                ("population", models.BigIntegerField(blank=True, db_index=True, null=True)),
                (
                    "feature_code",
                    models.CharField(blank=True, db_index=True, max_length=10, null=True),
                ),
                (
                    "timezone",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=40,
                        null=True,
                        validators=[cities_light.validators.timezone_validator],
                    ),
                ),
                ("point", django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.country"
                    ),
                ),
                (
                    "region",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.region",
                    ),
                ),
                (
                    "subregion",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.subregion",
                    ),
                ),
            ],
            options={
                "indexes": [
                    django.contrib.postgres.indexes.GinIndex(
                        fields=["name_ru"],
                        name="trigram_city_name_ru_idx",
                        opclasses=["gin_trgm_ops"],
                    ),
                    django.contrib.postgres.indexes.GinIndex(
                        fields=["name_en"],
                        name="trigram_city_name_en_idx",
                        opclasses=["gin_trgm_ops"],
                    ),
                ]
            },
        ),
    ]
