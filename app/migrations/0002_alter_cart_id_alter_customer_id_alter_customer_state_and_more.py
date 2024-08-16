# Generated by Django 5.0.1 on 2024-03-05 07:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="customer",
            name="state",
            field=models.CharField(
                choices=[
                    ("Andaman & Nicobar Islands", "Andaman & Nicobar Islands"),
                    ("Andra Pradesh", "Andra Pradesh"),
                    ("Assam", "Assam"),
                    ("Bihar", "Bihar"),
                    ("U.P", "U.P"),
                    ("M.P", "M.P"),
                    ("Delhi", "Delhi"),
                    ("Maharastra", "Maharastra"),
                ],
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="orderplaced",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.FloatField()),
                (
                    "razorpay_order_id",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "razorpay_payment_status",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "razorpay_payment_id",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("paid", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
