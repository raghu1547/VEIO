from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
# from db_tools import Datediff
from vehicles.models import Flow, Regveh, Gesveh
from datetime import datetime, timedelta
from django.db.models import F
from django.contrib import messages
from vehicles.tasks import trigger


def error_404_view(request, exception):
    return redirect('register')


def checkSO(user):
    return user.userprofile.is_SO


def checkS(user):
    return not user.userprofile.is_SO


def expirein():
    out_data = []
    for item in Flow.objects.all().filter(timeout__isnull=True):
        data = Gesveh.objects.filter(
            vn=item.vn).order_by('-firstentry').first()
        if (data is not None) and (data.firstentry+timedelta(data.nod) < datetime.now()):
            inp = vars(data)
            inp.pop('_state')
            inp['timein'] = item.timein
            out_data.append(inp)
            out_data.reverse()
    return out_data


@ login_required
@ user_passes_test(checkS)
def security(request):
    if request.method == "POST":
        json = formInput(request)
        if json.get('error'):
            messages.error(request, json.get('error'))
        else:
            messages.success(request, json.get('success'))
        return redirect('security')
    expiredata = expirein()

    return render(request, 'pages/security.html', {'expiredata': expiredata})


@ login_required
@ user_passes_test(checkSO)
def securityOfficer(request):
    expiredata = expirein()
    return render(request, 'pages/security_officer.html', {'expiredata': expiredata})


# 'vehicle_no': ['adasdf'], 'transport': ['exit'], 'Entrant': [''], 'phone_no': [''], 'nod': ['']}>


def formInput(request):
    print(request.POST)
    # print(request.POST.get('transport'))
    try:
        vehicle_no = request.POST.get('vehicle_no').strip().upper()
        transport = request.POST.get('transport')
        if vehicle_no != "":
            if request.POST.get('transport') == "entry":
                if Flow.objects.filter(vn=vehicle_no, timeout__isnull=True).exists():
                    # Flow.objects.filter(vn=vehicle_no, timeout__isnull=True).update(
                    #     timeout=datetime.now())
                    raise ValueError("Vehicle exit not recorded")
                elif Regveh.objects.filter(vn=vehicle_no).exists():
                    flow = Flow(vn=vehicle_no)
                    flow.save()
                elif Gesveh.objects.order_by('-firstentry').filter(vn=vehicle_no, firstentry__gte=datetime.now()-timedelta(days=1)*F('nod')).exists():
                    flow = Flow(vn=vehicle_no)
                    flow.save()
                else:
                    name = request.POST.get('Entrant').strip()
                    phone_no = request.POST.get('phone_no').strip()
                    nod = int(request.POST.get('nod'))
                    if name != "" and phone_no != "" and nod >= 1:
                        gesveh = Gesveh(vn=vehicle_no, name=name,
                                        contact=phone_no, nod=nod)
                        gesveh.save()
                        flow = Flow(vn=vehicle_no)
                        flow.save()
                        trigger(gesveh)
                    else:
                        raise ValueError(
                            "Something went wrong, Please try again")
            elif request.POST.get('transport') == "exit":
                if not Flow.objects.filter(vn=vehicle_no, timeout__isnull=True).exists():
                    # Flow.objects.filter(vn=vehicle_no, timeout__isnull=True).update(
                    #     timeout=datetime.now())
                    raise ValueError("Vehicle entry not recorded")
                else:
                    Flow.objects.filter(vn=vehicle_no, timeout__isnull=True).update(
                        timeout=datetime.now())
            else:
                raise ValueError("Something went wrong, Please try again")
        else:
            raise ValueError("Something went wrong, Please try again")
    except Exception as e:
        return {'error': e}

    return {'success': 'Successfull'}
