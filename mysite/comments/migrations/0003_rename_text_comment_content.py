from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_alter_comment_options_comment_parent_comment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='text',
            new_name='content',
        ),
    ] 