# Generated by Django 5.1.6 on 2025-03-29 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0006_alter_review_unique_together_alter_review_project'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(condition=models.Q(('project__isnull', False)), fields=('client', 'freelancer', 'project'), name='unique_project_review'),
        ),
    ]
