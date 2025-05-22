from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_rename_text_comment_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ] 