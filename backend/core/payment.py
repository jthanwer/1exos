from rest_framework.response import Response
from rest_framework import status
from users.serializers import PaymentIntentSerializer
import core.constants as cst

import stripe
import decimal


def euros2points(amount_euros):
    amount_points = amount_euros * cst.CHANGE * (1 + cst.BONUS)
    return amount_points


def stripe_create_payment(request):
    stripe.api_key = 'sk_test_l0DVglzDUUdvrm4xthnZrf5300Lq3X7bez'
    serializer = PaymentIntentSerializer(data=request.data)
    if serializer.is_valid():
        intent = stripe.PaymentIntent.create(**serializer.validated_data,
                                             confirmation_method='manual')
        return Response(intent)
    else:
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


def stripe_validate_payment(request):
    stripe.api_key = 'sk_test_l0DVglzDUUdvrm4xthnZrf5300Lq3X7bez'
    user = request.user
    payload = request.data

    if 'payment_method_id' in payload:
        intent = stripe.PaymentIntent.confirm(
            payload['payment_id'],
            payment_method=payload['payment_method_id'],
        )

    else:
        intent = stripe.PaymentIntent.confirm(
            payload['payment_id'],
        )

    if intent.status == 'succeeded':
        amount_euros = int(intent.amount / 100)
        amount_points = euros2points(amount_euros)
        user.tirelire += amount_points
        user.save()
        return Response(status=status.HTTP_200_OK)

    elif intent.status == 'requires_action':
        if intent.next_action.type == 'use_stripe_sdk':
            data = {
                'requires_action': True,
                'payment_intent_client_secret': intent.client_secret,
            }
            return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            data = {
                'requires_action': True,
                'payment_intent_client_secret': intent.client_secret,
            }
            return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
