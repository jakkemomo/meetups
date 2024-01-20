from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        # Replace with the name and the previous migration of your app
        (
            "events",
            "0012_alter_event_ratings_squashed_0016_alter_rating_options_rename_rating_rating_value",
        )
    ]

    def create_event_categories(apps, schema_editor):
        Category = apps.get_model("events", "Category")

        Category.objects.bulk_create(
            [
                Category(name="Music"),
                Category(name="Sports"),
                Category(name="Arts"),
                Category(name="Programming"),
                Category(name="Conference"),
            ]
        )

    # operations = [migrations.RunPython(create_event_categories)]
