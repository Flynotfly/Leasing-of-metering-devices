from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ContractForm, FinanceDetailsForm, WarrantyCaseForm
from .models import Contract, FinanceDetails, Payment, WarrantyCase
from .utils import generate_payment_dates, create_payments


@login_required
def edit_contract(request, pk=None):
    user = request.user
    company_name = user.profile.display_name
    if user.profile.role != 'LR':
        return HttpResponseForbidden("You don't have permission")
    is_new = True
    contract = None
    finance_details = None
    if pk:
        is_new = False
        contract = get_object_or_404(
            Contract,
            pk=pk,
            lessor=user,
        )
        if contract:
            finance_details = get_object_or_404(
                FinanceDetails,
                contract=contract
            )

    if request.method == 'POST':
        contract_form = ContractForm(request.POST, request.FILES, instance=contract)
        finance_details_form = FinanceDetailsForm(request.POST, instance=finance_details)

        if contract_form.is_valid() and finance_details_form.is_valid():
            contract = contract_form.save(commit=False)
            contract.lessor = user
            contract.save()

            finance_details = finance_details_form.save(commit=False)
            finance_details.contract = contract
            finance_details.save()

            payment_dates = generate_payment_dates(contract.started, finance_details.period)
            monthly_payment = finance_details.monthly_payment

            create_payments(contract, payment_dates, monthly_payment)

            return redirect('list_contract')

    contract_form = ContractForm(instance=contract)
    finance_details_form = FinanceDetailsForm(instance=finance_details)

    return render(
        request,
        'contract/edit.html',
        {
            'is_new': is_new,
            'contract_form': contract_form,
            'finance_details_form': finance_details_form,
            'company_name': company_name,
            'section': 'contract',
        }
    )


@login_required
def list_contract(request):
    user = request.user
    role = user.profile.role
    is_lessor = False
    if role == 'LR':
        is_lessor = True
        contracts = Contract.objects.filter(lessor=user)
    elif role == 'LE':
        contracts = Contract.objects.filter(lessee=user)
    elif role == 'SE':
        contracts = Contract.objects.filter(seller=user)
    elif role == 'AD':
        contracts = Contract.objects.all()
    else:
        contracts = None

    return render(
        request,
        'contract/list.html',
        {
            'company_name': user.profile.display_name,
            'contracts': contracts,
            'is_lessor': is_lessor,
            'section': 'contract',
        }
    )


@login_required
def view_contract(request, pk):
    company_name = request.user.profile.display_name
    contract = get_object_or_404(Contract, pk=pk)
    finance_details = get_object_or_404(FinanceDetails, contract=contract)
    return render(
        request,
        'contract/view.html',
        {
            'contract': contract,
            'finance_details': finance_details,
            'company_name': company_name,
            'section': 'contract',
        }
    )


@login_required
def view_payments(request, pk):
    is_lessor = False
    if request.user.profile.role == 'LR':
        is_lessor = True

    contract = get_object_or_404(Contract, pk=pk)
    payments = Payment.objects.filter(contract=contract)
    return render(
        request,
        'contract/payments.html',
        {
            'payments': payments,
            'is_lessor': is_lessor,
            'company_name': request.user.profile.display_name,
            'section': 'contract',
            'contract': contract,
        }
    )


@login_required
def toggle_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    user_role = request.user.profile.role

    if request.user.profile.role == 'LR':
        if payment.paid == 'R':
            action = request.POST.get('action')
            if action == 'approve':
                payment.paid = 'T'
            elif action == 'deny':
                payment.paid = 'F'
            payment.save()
    elif user_role == 'LE':
        if payment.paid == 'F':
            payment.paid = 'R'
            payment.save()

    return redirect('view_payments', pk=payment.contract.pk)


@login_required
def list_warranty(request):
    user = request.user
    role = user.profile.role
    is_lessee = False
    is_seller = False
    is_lessor = False

    if role == 'LR':
        is_lessor = True
        warranties = WarrantyCase.objects.filter(contract__lessor=user)
    elif role == 'LE':
        is_lessee = True
        warranties = WarrantyCase.objects.filter(contract__lessee=user)
    elif role == 'SE':
        is_seller = True
        warranties = WarrantyCase.objects.filter(contract__seller=user)
    elif role == 'AD':
        warranties = WarrantyCase.objects.all()
    else:
        warranties = None

    return render(
        request,
        'warranty/list.html',
        {
            'company_name': user.profile.display_name,
            'warranties': warranties,
            'is_lessor': is_lessor,
            'is_lessee': is_lessee,
            'is_seller': is_seller,
            'section': 'warranty',
        }
    )


@login_required
def edit_warranty(request, pk=None):
    user = request.user
    company_name = user.profile.display_name
    is_new = True
    warranty = None
    if pk:
        warranty = get_object_or_404(WarrantyCase, pk=pk)
        is_new = False

    if request.user.profile.role != 'LE':
        return HttpResponseForbidden("You don't have permission to add warranty cases.")

    if request.method == 'POST':
        form = WarrantyCaseForm(request.POST, user=user, instance=warranty)
        if form.is_valid():
            warranty = form.save()
            return redirect('list_warranty')

    form = WarrantyCaseForm(user=user, instance=warranty)
    return render(
        request,
        'warranty/edit.html',
        {
            'form': form,
            'is_new': is_new,
            'company_name': company_name,
            'section': 'warranty',
        }
    )


@login_required
def view_warranty(request, pk):
    warranty = get_object_or_404(WarrantyCase, pk=pk)
    user = request.user
    is_seller = user.profile.role == 'SE'
    company_name = user.profile.display_name

    if request.method == 'POST' and is_seller:
        if warranty.resolved == 'CR':
            warranty.resolved = 'IW'
        elif warranty.resolved == 'IW':
            warranty.resolved = 'CO'
        warranty.save()
        return redirect('view_warranty', pk=warranty.pk)

    return render(
        request,
        'warranty/view.html',
        {
                'warranty': warranty,
                'is_seller': is_seller,
                'company_name': company_name,
                'section': 'warranty',
            }
        )
