from django.shortcuts import render
from thesite.models import *
import locale
# Create your views here.
from django.http import HttpResponse

from .api import search

locale.setlocale(locale.LC_ALL, 'cs_CZ')

def index(request):
    r = Performance.objects.order_by('?').all()
    backs = []
    for perf in r[0:min(3, len(r))]:
        results = search(perf.artist + ' band', max_results=1)
        a =  results["results"]    
        print("------")
        print(a[0]["image"])
        backs.append((a[0]["image"], perf.artist))
        
    f = Festival.objects.last()
    print(f.date.strftime("%H"))
    date = f.date.strftime("%d. %m. %Y")
    name = backs[0][1]
    return render(request, 'index.html', {'perfs':r, 'first_back':backs[0], 'first_back_name':name, 'backs':backs[1:], 'festival':f, 'date':date})

def employee(request):
    r = Performance.objects.all()
    p = Podium.objects.all()
    return render(request, 'employee.html', {'performances':r, 'podiums':p})

def festivalForm(request):
    if request.method == 'POST':
        form = FestivalForm(request.POST)
        if form.is_valid():
            f = Festival();
            f.name = form.cleaned_data["name"]
            f.location = form.cleaned_data["address"]
            f.date = datetime(int(form.cleaned_data["year"]), int(form.cleaned_data["month"]), int(form.cleaned_data["day"]), 
                                    0,0,0,0)
            f.save()
            return render(request, 'close.html', {})

    else:
        form = FestivalForm()

    return render(request, 'festivalForm.html', {'form': form})
def festival(request):
    if request.method == 'POST':
        f = FestivalForm();
        f.name = request.POST["name"]
        f.location = request.POST["address"]
        f.date = datetime(int(request.POST["rok"]), int(request.POST["mesic"]), int(request.POST["den"]), 
                                0,0,0,0)
        print(f)
        f.save()
        return render(request, 'close.html', {})
    return render(request, 'festival.html', {})

def addPerformance(request):
    if request.method == 'POST':
        p = Performance()
        p.artist = request.POST["name"]
        p.arrives = datetime(int(request.POST["rok"]), int(request.POST["mesic"]), int(request.POST["den"]), 
                             int(request.POST["hodiny"]), int(request.POST["minuty"]), 0, 0)
        p.performance_time = p.arrives
        f = Festival.objects.filter()[:1].get()
        p.festival_iteration = f
        p.genre = Genre.objects.filter().get(name=request.POST["hack2"])
        p.podium = Podium.objects.get(id = int(request.POST["hack"]))
        p.save()
        return render(request, 'close.html', {})
  
    p = Podium.objects.all()
    g = Genre.objects.all()
    return render(request, 'addPerformance.html', {'podiums':p, 'genres':g})

def editPerformance(request):
    if request.method == 'POST':
        p = Performance.objects.get(id=int(request.POST["perfId"]))
        p.artist = request.POST["name"]
        p.arrives = datetime(int(request.POST["rok"]), int(request.POST["mesic"]), int(request.POST["den"]), 
                             int(request.POST["hodiny"]), int(request.POST["minuty"]), 0, 0)
        p.performance_time = p.arrives
        f = Festival.objects.get(id=int(request.POST["iteration"]))
        p.festival_iteration = f
        p.genre = Genre.objects.filter().get(name=request.POST["hack2"])
        p.podium = Podium.objects.get(name = request.POST["hack"])
        p.save()
        return render(request, 'close.html', {})
    
    if request.GET.get('id') is not None:
        performance = Performance.objects.get(id=int(request.GET.get('id')))    
        p = Podium.objects.all()
        g = Genre.objects.all()
        return render(request, 'editPerformance.html', {'performance':performance, 'podiums':p, 'genres':g})
    return render(request, 'editPerformance.html', {})


def deletePerformance():
    # get parameter and delete from db
    return render(request, 'employee.html', {})

def festival_info(request, fest_id):
    try:
        r = Festival.objects.get(id = fest_id)
    except Festival.DoesNotExist:
        raise Http404('Neexistuje')
    return render(request, 'festival.html', {'fest':r})

def busyness(request):
    r = Performance.objects.all()
    p = Podium.objects.all()
    dict = {}
    for podium in p:
        for perf in r:
            if perf.podium == podium:
                if podium not in dict:
                    dict[podium] = 1
                else:
                    dict[podium] += 1
    print (dict)
    
    return render(request, 'busyness.html', {'podiums':dict})

def owner(request):
    s = Staff.objects.all()
    return render(request, 'owner.html', {'staff':s})

def deletePerformance(request):
    if request.GET.get('id') is not None:
        Performance.objects.filter(id=int(request.GET.get('id'))).delete()
    r = Performance.objects.all()
    p = Podium.objects.all()
    return render(request, 'employee.html', {'performances':r, 'podiums':p})

def sellTicket(request):
    if request.method == 'POST':
        try:
            ticket = Ticket.objects.get(username=request.POST["fname"])
            print("BAD already in")
            message = '<div class="alert alert-danger" role="alert">'
            message = message +'Vstupenka pro tohoto zákazníka existuje!! Kategorie: ' + ticket.category
            message = message + '</div>'
            return render(request, 'sellTicket.html', {'message':message})
        except:
            t = Ticket()
            t.category = request.POST["hack"]
            t.username = request.POST["fname"]
            t.valid_from = 1
            t.valid_to = 4
            f = Festival.objects.filter()[:1].get()
            t.iteration = f
            t.save()
            
            r = Performance.objects.all()
            p = Podium.objects.all()
            return render(request, 'employee.html', {'performances':r, 'podiums':p})
    return render(request, 'sellTicket.html', {'message':''})

def addEmployee(request):
    if request.method == 'POST':
        s = Staff()
        s.first_name = request.POST["fname"]
        s.last_name = request.POST["lname"]
        f = Festival.objects.filter()[:1].get()
        s.iteration = f
        s.role = request.POST["hack"]
        s.save()
        return render(request, 'close.html', {})
    return render(request, 'addEmployee.html', {})

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import *

def addEmployeeForm(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            s = Staff()
            s.first_name = form.cleaned_data["first_name"]
            s.last_name = form.cleaned_data["last_name"]
            f = Festival.objects.filter()[:1].get()
            s.iteration = f
            s.role = form.cleaned_data["role"]
            s.save()
            return render(request, 'close.html', {})

    else:
        form = EmployeeForm()

    return render(request, 'addEmployeeForm.html', {'form': form})

def sellTicketForm(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TicketForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                ticket = Ticket.objects.get(username=form.cleaned_data["username"])
                print("BAD already in")
                message = '<div class="alert alert-danger" role="alert">'
                message = message +'Vstupenka pro tohoto zákazníka existuje!! Kategorie: ' + ticket.category
                message = message + '</div>'
                return render(request, 'sellTicketForm.html', {'message':message})
            except:                
                t = Ticket()
                t.category = form.cleaned_data["category"]
                t.username = form.cleaned_data["username"]
                t.valid_from = 1
                t.valid_to = 4
                f = Festival.objects.filter()[:1].get()
                t.iteration = f
                t.save()
            
            # return HttpResponseRedirect('/thesite')
            return render(request, 'close.html', {})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TicketForm()

    return render(request, 'sellTicketForm.html', {'form': form})

def editEmployee(request):
    if request.method == 'POST':
        s = Staff.objects.get(id=int(request.POST["staffId"]))
        s.first_name = request.POST["fname"]
        s.last_name = request.POST["lname"]
        f = Festival.objects.filter()[:1].get()
        s.iteration = f
        s.role = request.POST["hack"]
        s.save()
        return render(request, 'close.html', {})
    
    if request.GET.get('id') is not None:
        staff = Staff.objects.get(id=int(request.GET.get('id')))    
        
        return render(request, 'editEmployee.html', {'staff':staff})
    else:
        return render(request, 'close.html', {})

def editEmployeeForm(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():       
            s = Staff.objects.get(id=int(request.POST["staffId"]))
            s.first_name = form.cleaned_data["first_name"]
            s.last_name = form.cleaned_data["last_name"]
            f = Festival.objects.filter()[:1].get()
            s.iteration = f
            s.role = form.cleaned_data["role"]
            s.save()
            return render(request, 'close.html', {})

    else:
        if request.GET.get('id') is not None:
            staff = Staff.objects.get(id=int(request.GET.get('id')))
            first_name = staff.first_name 
            initial_dict = {
            "first_name" : staff.first_name,
            "last_name" : staff.last_name,
            "role ":staff.role,
            }
        form = EmployeeForm(request.POST or None, initial = initial_dict)
        
    return render(request, 'editEmployeeForm.html', {'form': form, 'staff':staff})

def delEmployee(request):
    if request.GET.get('id') is not None:
        Staff.objects.filter(id=int(request.GET.get('id'))).delete()
    staff = Staff.objects.all()
    return render(request, 'owner.html', {'staff':staff})

def validateTicket(request):
    if request.method == 'POST':
        try:
            ticket = Ticket.objects.get(username=request.POST["fname"])
            message = '<div class="alert alert-success" role="alert">'
            message = message +'Vstupenka pro tohoto zákazníka existuje! Kategorie: ' + ticket.category
            message = message + '</div>'
        except:
            message = '<div class="alert alert-danger" role="alert">'
            message = message + 'Vstupenka pro tohoto zákazníka nebyla nalezena.'
            message = message + '</div>'
      
        return render(request, 'validateTicket.html', {'message':message})
    return render(request, 'validateTicket.html', {'message':''})

def validateTicketForm(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ValidateTicketForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            try:
                ticket = Ticket.objects.get(username=form.cleaned_data["username"])
                message = '<div class="alert alert-success" role="alert">'
                message = message +'Vstupenka pro tohoto zákazníka existuje! Kategorie: ' + ticket.category
                message = message + '</div>'
                return render(request, 'validateTicketForm.html', {'form': form, 'message':message})
            except:                
                message = '<div class="alert alert-danger" role="alert">'
                message = message + 'Vstupenka pro tohoto zákazníka nebyla nalezena.'
                message = message + '</div>'
                return render(request, 'validateTicketForm.html', {'form': form, 'message':message})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ValidateTicketForm()

    return render(request, 'validateTicketForm.html', {'form': form})

def ticketList(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticketList.html', {'tickets':tickets})


def ticketListForm(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TicketListForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            tickets = Ticket.objects.filter(category=form.cleaned_data["category"])
            return render(request, 'ticketListForm.html', {'form': form, 'tickets':tickets})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TicketListForm()

    tickets = Ticket.objects.all()
    return render(request, 'ticketListForm.html', {'form': form, 'tickets':tickets})