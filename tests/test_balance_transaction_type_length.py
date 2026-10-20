import pytest
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator

from djstripe.models import BalanceTransaction

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "transaction_type",
    [
        "charge",
        "payout_minimum_balance_release",
        "issuing_dispute_provisional_credit_reversal",
        "future_type_" + "x" * 60,
    ],
)
def test_sync_preserves_long_transaction_types(transaction_type):
    data = {
        "id": "txn_long_type",
        "object": "balance_transaction",
        "amount": 1000000,
        "available_on": 1792369416,
        "created": 1792369416,
        "currency": "eur",
        "fee": 0,
        "fee_details": [],
        "livemode": False,
        "net": 1000000,
        "reporting_category": "other_adjustment",
        "source": None,
        "status": "available",
        "type": transaction_type,
    }

    saved = BalanceTransaction.sync_from_stripe_data(data)
    saved.refresh_from_db()
    assert saved.type == transaction_type
    assert saved.amount == saved.net == data["amount"]

    BalanceTransaction.sync_from_stripe_data(data)
    assert BalanceTransaction.objects.filter(id=data["id"]).count() == 1


def test_transaction_type_length_validator_matches_column():
    field = BalanceTransaction._meta.get_field("type")
    validators = [v for v in field.validators if isinstance(v, MaxLengthValidator)]
    assert field.max_length == 255
    assert len(validators) == 1
    validators[0]("x" * 255)
    with pytest.raises(ValidationError):
        validators[0]("x" * 256)
