from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Alumno
from django import forms
from django.http import FileResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.mail import EmailMessage
import requests
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ["nombre", "edad", "carrera"]

import json

@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            return redirect("dashboard")
    else:
        form = AlumnoForm()

    # 👉 preparar datos para Chart.js
    nombres = [a.nombre for a in alumnos]
    edades = [a.edad for a in alumnos]

    return render(
        request,
        "alumnos/dashboard.html",
        {
            "alumnos": alumnos,
            "form": form,
            "nombres_json": json.dumps(nombres),
            "edades_json": json.dumps(edades),
        },
    )




@login_required
def alumno_pdf(request, id):
    alumno = Alumno.objects.get(id=id, usuario=request.user)

    # Generar PDF en memoria
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Alumno: {alumno.nombre}")
    p.drawString(100, 780, f"Edad: {alumno.edad}")
    p.drawString(100, 760, f"Carrera: {alumno.carrera}")
    p.showPage()
    p.save()
    buffer.seek(0)

    # Enviar PDF por correo
    email = EmailMessage(
        subject="Datos del alumno",
        body=f"Adjunto PDF con los datos de {alumno.nombre}",
        from_email="tu_correo_configurado@gmail.com",
        to=[request.user.email],  # o al docente
    )
    email.attach(f"{alumno.nombre}.pdf", buffer.getvalue(), "application/pdf")
    email.send()

    # Descargar PDF directamente
    return FileResponse(buffer, as_attachment=True, filename=f"{alumno.nombre}.pdf")


@login_required
def scraping_view(request):
    url = "https://news.ycombinator.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    titulos = [a.get_text() for a in soup.select(".titleline a")[:10]]
    return render(request, "alumnos/scraping.html", {"titulos": titulos})

