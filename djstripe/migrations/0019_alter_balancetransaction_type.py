from django.db import migrations

import djstripe.enums
import djstripe.fields


class Migration(migrations.Migration):
    dependencies = [
        ("djstripe", "0018_alter_balancetransaction_reporting_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="balancetransaction",
            name="type",
            field=djstripe.fields.StripeEnumField(
                enum=djstripe.enums.BalanceTransactionType, max_length=255
            ),
        ),
    ]
