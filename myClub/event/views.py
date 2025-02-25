from django.shortcuts import render, redirect
from calendar import HTMLCalendar
import calendar
import datetime
from .models import Event, Vanue
from .forms import VanueForm, EventForm, EventFormAdmin
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.contrib.auth.models import User
from django.contrib import messages
import csv

import io
# from reportlab.pdfgen import canvas # type: ignore
# from reportlab.lib.pagesizes import letter # type: ignore
# import paginator for pagination
from django.core.paginator import Paginator


    
# Create your views here.
def show_event(request, event_id):
    events = Event.objects.get(pk=event_id)
    return render(request, 'events/show_event.html',{'event':events})


def vanue_events(request, vanue_id):
    #grab the vanue
    vanu = Vanue.objects.get(id=vanue_id)
    # grab the events from that vanue
    
#If the Event model has a ForeignKey or OneToOneField pointing to the Vanu model, Django automatically creates a reverse relation using the lowercase name of the related model followed by _set (e.g., event_set).
#If you have specified a custom related_name in the ForeignKey or OneToOneField, you should use that instead of event_set. For example, if you defined the ForeignKey like this:
#class Event(models.Model):
 #   vanu = models.ForeignKey(Vanu, related_name='events', on_delete=models.CASCADE)
#Then you should use:
    events = vanu.event.all()

    if events:
        return render(request, 'events/vanue_events.html', {'events':events})
    else:
        messages.success(request, "This vanue has no events this time...")
        return redirect('admin')



def admin(request):
    users = User.objects.all().count()
    Events = Event.objects.all().count()
    vanues = Vanue.objects.all().count()
    vanue = Vanue.objects.all()


    events = Event.objects.all().order_by('-date')
    if request.user.is_superuser:
        if request.method == 'POST':
         messages.success(request, "The event aproval has been updated!")
         list_id = request.POST.getlist('boxes')
         events.update(aproved=False)
         for x in list_id:
             Event.objects.filter(pk=int(x)).update(aproved=True)
         return redirect('events')

        else:
            return render(request, 'events/admin.html', {"event":events, "users":users, "Events":Events, "vanues":vanues, 'vanue':vanue})
    else:
        messages.success(request, "You aren't authorized to view this page.")
        return redirect('index')

# Generate PDF files
def vanue_pdf(request):
    vanues = Vanue.objects.all()
    # create a response object with content type pdf

    buffer = io.BytesIO() # create a buffer object to hold the pdf data 
    # create a canvas object that will generate the pdf file in the buffer object 
    p = canvas.Canvas(buffer, pagesize=letter)
    y = 750     # set the y coordinate for the first line of text
    for van in vanues: # loop through the vanues and write the data to the pdf file
        p.drawString(100, y, f"Vanue Name: {van.name}") # write the vanue name to the pdf file
        p.drawString(100, y-20, f"Vanue Address: {van.address}") # write the vanue address to the pdf file
        p.drawString(100, y-40, f"Phone: {van.phone}") # write the vanue phone number to the pdf file
        p.drawString(100, y-60, f"Map Reference: {van.map_reference}") # write the vanue map reference to the pdf file
        y -= 100 # move the y coordinate down by 100 pixels
    p.showPage() # create a new page in the pdf file
    p.save() # save the pdf file
    buffer.seek(0) # move the buffer object back to the beginning of the file
    return FileResponse(buffer, as_attachment=True, filename='vanues.pdf') # return the pdf file as a response object with the filename vanues.pdf

# Generate CSV files
def vanue_csv(request):
    vanues = Vanue.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vanues.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Address', 'Phone', 'Map Reference'])
    for van in vanues:
        writer.writerow([van.name, van.address, van.phone, van.map_reference])
    return response

# Generate Text files
def vanue_text(request):
    vanues = Vanue.objects.all()
    # create a response object with content type text/plain 
    response = HttpResponse(content_type='text/plain')
    # set the content disposition to attachment and the file name to vanues.txt
    # this will tell the browser to download the file instead of displaying it
    # how to display instead of download it?
    response['Content-Disposition'] = 'inline;' #'attachment; filename="vanues.txt"' #inline will display the file in the browser instead of downloading it and the filename is vanues.txt atttachment will download the file
    
    line = []
    for van in vanues:
        line.append(f"{van.name}\n{van.address}\n{van.phone}\n{van.map_reference}\n\n")
        response.writelines(line)
    return response

def delete_event(request, id):
    event = Event.objects.get(pk=id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, "Event Deleted!!")
        return HttpResponseRedirect('/events')
    else:
        messages.success(request, "You aren't authorized to delete..!!")
        return HttpResponseRedirect('/events')

def delete_vanue(request, id):
    van = Vanue.objects.get(pk=id)
    van.delete()
    return HttpResponseRedirect('/vanue')

def update_event(request, id):
    van = Event.objects.get(pk=id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=van)
    else:  
        form = EventForm(request.POST or None, instance=van)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/events')
    return render(request, "events/update_event.html", {"form": form, "van": van})


def add_event(request):
    submitted = False
    if request.method == 'POST':
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
         
              form = EventForm(request.POST)
              if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
            # Just Going to page not submitting anything
            if request.user.is_superuser:  
                form = EventFormAdmin()
            else:  
                form = EventForm()
            if 'submitted' in request.GET:  
                submitted = True
    return render(request, "events/add_event.html", {  "form": form, 'submitted':submitted })

        

def update_vanue(request, id):
    van = Vanue.objects.get(pk=id)
    form = VanueForm(request.POST or None, request.FILES or None,  instance=van)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/vanue')
    return render(request, "events/update_vanue.html", {"form": form, "van": van})


def search(request):
    if request.method == 'POST':
        searched = request.POST['search_text']
        vanues = Vanue.objects.filter(name__contains=searched) #name__contains=searched. 
        return render(request, "events/search.html", {"searched": searched, "vanues": vanues})

def search_event(request):
    if request.method == 'POST':
        searched = request.POST['search_text']
        events = Event.objects.filter(title__contains=searched) #name__contains=searched. 
        return render(request, "events/search_event.html", {"searched": searched, "events": events})
   
    return render(request, "events/search_event.html", {})

def show_vanue(request, id):
    van = Vanue.objects.get(pk=id)
    owner = User.objects.get(pk=van.owner)
    events = van.event.all()
    return render(request, "events/show_vanue.html", {"vanues": van, 'owner':owner, 'events':events})

def vanue(request):
    # van = Vanue.objects.all().order_by('name') #.order_by('name') or something and '?' for randomize
    p = Paginator(Vanue.objects.all(), 2)
    page = request.GET.get('page')
    van = p.get_page(page)
    return render(request, "events/vanue.html", {"vanues": van})

def add_vanue(request):
    submitted = False
    if request.method == 'POST':
        form = VanueForm(request.POST, request.FILES)
        if form.is_valid():
            vanue = form.save(commit=False)
            vanue.owner = request.user.id
            vanue.save()
            return HttpResponseRedirect('/add_vanue?submitted=True')
    else:
        form = VanueForm()
        if 'submitted' in request.GET:  
            submitted = True
    return render(request, "events/add_vanue.html", {  "form": form, 'submitted':submitted })

def all_events(request):
    all_events = Event.objects.all().order_by('title') #.order_by('name') or something and ? for randomize
    return render(request, "events/all_events.html", {  "all_events": all_events })


def index(request, year=datetime.datetime.now().year, month=datetime.datetime.now().strftime("%B")):

    month = month.capitalize() 
    month_number = list(calendar.month_name).index(month)
    now = datetime.datetime.now()
    cal = HTMLCalendar().formatmonth(year, month_number)
    time = now.strftime("%I:%M %p")
    events = Event.objects.filter(date__year=year, date__month=month_number)
    event = Event.objects.all()
    return render(request, "events/index.html", {
        "name": "Django Event Calendar",
        "year": year,
        "month": month, 
        "month_number": month_number,
        "time": time, 
        "cal": cal,
        "events": events,
        'eve':event,

    })

