from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Merchant, Transaction
from .forms import RegisterForm

import stripe

# 🔐 Your Stripe test secret key (OK for local testing)
stripe.api_key = "sk_test_51Sp0ejRuhN5mraKvG0LXQC0rVwlFi5J3xNYAomKFkpjldlz7Clt3HRELbILShb8tPUG40DLCdLoVVyDFKFiaXUHa00lDcaPf4N"


# ---------------- HOME ----------------
def home(request):
    return render(request, 'payments/home.html', {
        'merchants': Merchant.objects.all()
    })


# ---------------- REGISTER ----------------
def register(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        return redirect('home')

    return render(request, 'payments/register.html', {'form': form})


# ---------------- PAY (with amount input) ----------------
@login_required
def pay(request, merchant_id):
    merchant = get_object_or_404(Merchant, id=merchant_id)

    # If form submitted → create Stripe session
    if request.method == "POST":
        amount_rupees = int(request.POST.get("amount"))
        amount_paise = amount_rupees * 100

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': f'Payment to {merchant.store_name}',
                    },
                    'unit_amount': amount_paise,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/',
        )

        # Save transaction (for demo purpose)
        Transaction.objects.create(
            user=request.user,
            merchant=merchant,
            amount=amount_rupees,
            stripe_payment_id=session.id
        )

        return redirect(session.url)

    # If GET request → show amount input page
    return render(request, 'payments/pay_form.html', {
        'merchant': merchant
    })


# ---------------- SUCCESS ----------------
@login_required
def success(request):
    return render(request, 'payments/success.html')


# ---------------- HISTORY ----------------
@login_required
def history(request):
    txns = Transaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'payments/history.html', {'txns': txns})
