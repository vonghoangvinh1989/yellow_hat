# Generated by Django 5.1.1 on 2024-10-18 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0002_penetrationtest_pen_test_leader_signature_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='penetrationtest',
            name='pen_test_leader_signature_image',
            field=models.ImageField(blank=True, null=True, upload_to='E:\\SaskPolyTechCourses\\LearningEthicalHackingAndExploit\\FinalProject\\yellow_hat\\signatures'),
        ),
        migrations.AlterField(
            model_name='penetrationtest',
            name='target_signature_image',
            field=models.ImageField(blank=True, null=True, upload_to='E:\\SaskPolyTechCourses\\LearningEthicalHackingAndExploit\\FinalProject\\yellow_hat\\signatures'),
        ),
    ]