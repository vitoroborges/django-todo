from django.shortcuts import render
from .models import Tarefa, Usuario
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def formlogin(request):

    if request.method == "POST":
        usuario = request.POST['login']
        senha = request.POST['senha']        
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/tarefas/listartarefas")
    
    return render(request, "login.html")

def logout_view(request):
    logout(request)

    return HttpResponseRedirect("/tarefas/login")

@login_required(login_url="/tarefas/login")
def listarTarefas(request):

    tarefas = Tarefa.objects.all()

    return render(request, "listarTarefas.html", {"tarefas" : tarefas})

@login_required(login_url="/tarefas/login")
def listarUsuarios(request):

    usuarios = Usuario.objects.all()

    return render(request, "listarUsuarios.html", {"usuarios": usuarios})

@login_required(login_url="/tarefas/login")
def cadastroAtividade(request):

    if(request.method == "POST"):
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')        
        ano = int(request.POST.get('data').split("-")[0])
        mes = int(request.POST.get('data').split("-")[1])
        dia = int(request.POST.get('data').split("-")[2])
        data = datetime(ano, mes, dia)
        usuario = Usuario.objects.get(id=request.POST.get('usuario'))

        nova_atividade = Tarefa(titulo=titulo, 
                                descricao=descricao, 
                                data=data, 
                                usuario=usuario)
        nova_atividade.save()

        return HttpResponseRedirect('/tarefas/listartarefas')

    usuarios = Usuario.objects.all()

    return render(request, "cadastroAtividade.html", {'usuarios':usuarios})

@login_required(login_url="/tarefas/login")
def cadastroUsuario(request):
    return render(request, "cadastroUsuario.html")

@login_required(login_url="/tarefas/login")
def excluirAtividade(request, id):

    tarefa = Tarefa.objects.get(id=id)
    tarefa.delete()

    return HttpResponseRedirect('/tarefas/listartarefas')

@login_required(login_url="/tarefas/login")
def editarUsuario(request, id):
    if(request.method == "POST"):
        nome = request.POST.get('nome')
        email = request.POST.get('email')

        usuario_editado = Usuario.objects.get(id=id)
        usuario_editado.nome = nome
        usuario_editado.email = email
        usuario_editado.save()
        return HttpResponseRedirect('/tarefas/listartarefas')
    else:
        usuario = Usuario.objects.get(id=id)
        return render(request, "editarUsuario.html", {'usuario':usuario})

@login_required(login_url="/tarefas/login")
def atualizarCadastro(request, id):
     atividade = Tarefa.objects.get(id=id)

     if(request.method == "POST"):
        
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')        
        ano = int(request.POST.get('data').split("-")[0])
        mes = int(request.POST.get('data').split("-")[1])
        dia = int(request.POST.get('data').split("-")[2])
        data = datetime(ano, mes, dia)
        usuario = Usuario.objects.get(id=request.POST.get('usuario'))
        
        atividade_editada = Tarefa.objects.get(id=id)
        atividade_editada.titulo = titulo
        atividade_editada.descricao = descricao
        atividade_editada.data = data
        atividade_editada.usuario = usuario
        atividade_editada.save()

        return HttpResponseRedirect('/tarefas/listartarefas')
     else:
        atividade = Tarefa.objects.get(id=id)
        usuarios = Usuario.objects.all()

        return render(request, "editarAtividade.html", {'usuarios':usuarios, 'atividade': atividade})