# Importações necessárias para a aplicação funcionar corretamente
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import Usuario, Disciplina, ReservaAmbiente, Sala
from .serializers import UsuarioSerializer, DisciplinaSerializer, ReservaAmbienteSerializer, LoginSerializer, SalaSerializer
from .permissions import IsGestor, IsProfessor, IsDonoOuGestor
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.http import Http404
from rest_framework.response import Response



# Create your views here.
# View utilizada para listar os usuários cadastrados no banco de dados e para cadastrar um novo usuário
class UsuarioListCreate(ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsGestor] #Permite que apenas usuários cadastrados como gestor tenham acesso a essa funcionalidade

# View utilizada para atualizar parcialmente ou completamente ou deletar um usuário do banco de dados
class UsuarioRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsGestor] #Permite que apenas usuários cadastrados como gestor tenham acesso a essa funcionalidade
    lookup_field = 'pk'

    # Mostra uma mensagem quando um usuário for deletado do banco de dados
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"Usuário excluído do banco de dados"})

# Tratativa de erro para quando a sala passada como parâmetro passada pelo usuário não estiver cadastrada no banco de dados
    def get_object(self):
        try:
            return super().get_object()
        except Exception:
        # Mostra uma mensagem de erro para o usuário
            raise Http404({'Erro': 'Usuário não encontrado no banco de dados'})

# View utilizada para listar as salas cadastrados no banco de dados e para cadastrar uma nova sala
class SalaListCreate(ListCreateAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [IsGestor] #Permite que apenas usuários cadastrados como gestor tenham acesso a essa funcionalidade

    # Verificação para que duas reservas não sejam feitas no mesmo ambiente e no mesmo intervalo de tempo
    def perform_create(self, serializer):
        # Pega todos os dados passados pelo usuário
        nome = serializer.validated_data.get('nome')
        capacidade_alunos = serializer.validated_data.get('capacidade_alunos')
      
        # Verifica se uma sala com esses dados já existe no banco de dados
        sala = Sala.objects.filter(
            nome = nome, 
            capacidade_alunos = capacidade_alunos, 
        ).exists()

        # Se uma sala com os dados fornecidos já existir, reserva uma mensagem de erro avisando o usuário 
        if sala:
            raise ValidationError("Uma sala com esses dados já existe no banco de dados")

        # Caso não exista uma sala com os mesmos dados, ela é salva no banco de dados
        serializer.save()

# View utilizada para atualizar parcialmente ou completamente ou deletar uma sala do banco de dados
class SalaRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer
    permission_classes = [IsGestor] #Permite que apenas usuários cadastrados como gestor tenham acesso a essa funcionalidade
    lookup_field = 'pk'

    # Mostra uma mensagem quando uma sala for deletado do banco de dados
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"Sala excluída do banco de dados"})

# Tratativa de erro para quando a sala passada como parâmetro passada pelo usuário não estiver cadastrada no banco de dados
    def get_object(self):
        try:
            return super().get_object()
        except Exception:
        # Mostra uma mensagem de erro para o usuário
            raise Http404({'Erro': 'Sala não encontrada no banco de dados'})

# View utilizada para listar as disciplinas cadastrados no banco de dados e para cadastrar uma nova disciplina
class DisciplinaListCreate(ListCreateAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer

    # Verificação para que duas reservas não sejam feitas no mesmo ambiente e no mesmo intervalo de tempo
    def perform_create(self, serializer):
        # Pega todos os dados passados pelo usuário
        nome = serializer.validated_data.get('nome')
        curso = serializer.validated_data.get('curso')
        carga_horaria = serializer.validated_data.get('carga_horaria')
        professor = serializer.validated_data.get('professor')
      
        # Verifica se uma disciplina com esses dados já existe no banco de dados
        cadastro = Disciplina.objects.filter(
            nome = nome, 
            curso= curso, 
            carga_horaria=carga_horaria, 
            professor= professor
        ).exists()

        # Se uma disciplina com os dados fornecidos já existir, reserva uma mensagem de erro avisando o usuário 
        if cadastro:
            raise ValidationError("Uma disciplina com esses dados já existe no banco de dados")

        # Caso não exista uma disciplina com os mesmos dados, ela é salva no banco de dados
        serializer.save()

    def get_permissions(self):
        if self.request.method == 'GET':
            return[IsAuthenticated()]
        return [IsGestor()]

# View utilizada para atualizar parcialmente ou completamente ou deletar uma disciplina do banco de dados  
class DisciplinaRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    permission_classes = [IsGestor] #Permite que apenas usuários cadastrados como gestor no banco de dados tenham acesso a essa funcionalidade
    lookup_field = 'pk'

    # Mostra uma mensagem quando uma disciplina for deletado do banco de dados
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"Disciplina excluída do banco de dados"})

# Tratativa de erro para quando a disciplina passada como parâmetro passada pelo usuário não estiver cadastrada no banco de dados
    def get_object(self):
        try:
            return super().get_object()
        except Exception:
        # Mostra uma mensagem de erro para o usuário
            raise Http404({'Erro': 'Disciplina não encontrada no banco de dados'})

# View utilizada para listar as disciplinas encarregadas a cada professor cadastrados  no banco de dados 
class DisciplinaProfessorList(ListAPIView):
    serializer_class = DisciplinaSerializer
    permission_classes = [IsProfessor] #Permite que usuários cadastrados como professor tenham acesso a essa funcionalidade

    def get_queryset(self):
        return Disciplina.objects.filter(professor=self.request.user)

# View utilizada para listar as reservas de ambiente cadastrados no banco de dados e para cadastrar uma nova disciplina  
class ReservaAmbienteListCreate(ListCreateAPIView):
    queryset = ReservaAmbiente.objects.all()
    serializer_class = ReservaAmbienteSerializer

# Verificação para que duas reservas não sejam feitas no mesmo ambiente e no mesmo intervalo de tempo
    def perform_create(self, serializer):
        # Pega todos os dados passados pelo usuário
        data_inicio = serializer.validated_data.get('data_inicio')
        data_termino = serializer.validated_data.get('data_termino')
        sala_reservada = serializer.validated_data.get('sala_reservada')
        periodo = serializer.validated_data.get('periodo')
      
        # Verifica se uma reserva com esses dados já existe no banco de dados
        reserva = ReservaAmbiente.objects.filter(
            sala_reservada = sala_reservada, 
            data_inicio__lte= data_termino, 
            data_termino__gte=data_inicio, 
            periodo = periodo
        ).exists()

        # Se uma reserva para aquele ambiente e horário já existir, reserva uma mensagem de erro avisando o usuário de que a reserva já existe no banco de dados
        if reserva:
            raise ValidationError("Uma reserva para este ambiente e período já existe no banco de dados")

        # Caso não exista uma reserva com os mesmos dados, ela é salva no banco de dados
        serializer.save()

    # define as permissões. Caso seja GET, qualquer pessoa logada pode visualizar, caso o método seja outro, é necessário ser gestor para acessar
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsGestor()]
    
    # Define a consulta pelo queryset, usando um filtro de id. caso contrário, retorna todos os dados cadastrados
    def get_queryset(self):
        queryset = super().get_queryset()
        professor_id = self.request.query_params.get('professor', None)
        if professor_id:
            queryset = queryset.filter(professor_id=professor_id)
        return queryset 

# View utilizada para atualizar parcialmente ou completamente ou deletar uma reserva de ambiente no banco de dados 
class ReservaAmbienteRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = ReservaAmbiente.objects.all()
    serializer_class = ReservaAmbienteSerializer
    permission_classes = [IsAuthenticated,IsDonoOuGestor] #Permite que só pessoas que são dono ou gestor tenham acesso a essa funcionalidade
    lookup_field = 'pk'
    # Mostra uma mensagem quando uma reserva for deletada do banco de dados
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"Reserva de ambiente excluída do banco de dados"})
    
    # Tratativa de erro para quando a disciplina passada como parâmetro passada pelo usuário não estiver cadastrada no banco de dados
    def get_object(self):
        try:
            return super().get_object()
        # Mostra uma mensagem de erro para o usuário
        except Exception:
            raise Http404({'Erro': 'Não existe uma reserva desse ambiente no banco de dados'})

# View utilizada para listar as reservas de ambiente que cada professor está encarregado 
class ReservaAmbienteProfessorList(ListAPIView):
    serializer_class = ReservaAmbienteSerializer
    permission_classes = [IsProfessor] #permite que usuários cadastrdos como professor tenham acesso a essa funcionalidade 

    def get_queryset(self):
        return ReservaAmbiente.objects.filter(professor=self.request.user)

# View utilizada para fazer o login do usuário
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
