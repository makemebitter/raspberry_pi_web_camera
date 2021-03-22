from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import subprocess
# Create your views here.

def index(request):
    """View function for home page of site."""
    
    process = subprocess.Popen(['/bin/systemctl', 'status', 'stream_camera'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    camera_status = 'UP' if 'Active: active' in str(out) else "DOWN"
    context = {
        'camera_status': camera_status
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'pigwatch/index.html', context=context)

def start_cam(request):
    """View function for home page of site."""
    subprocess.call(['sudo', '/bin/systemctl', 'start', 'stream_camera'])


    # Render the HTML template index.html with the data in the context variable
    return HttpResponseRedirect('/')

def stop_cam(request):
    """View function for home page of site."""
    subprocess.call(['sudo', '/bin/systemctl', 'stop', 'stream_camera'])
    # Render the HTML template index.html with the data in the context variable
    return HttpResponseRedirect('/')

