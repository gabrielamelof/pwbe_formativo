from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Model para cadastro de usuários no banco de dados. Com os campos de informação necessárias
class Usuario(AbstractUser):
    TIPO_CHOICES = [
        ('G', 'Gestor'), 
        ('P', 'Professor'), 
    ]

    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES, default='P')
    ni = models.IntegerField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField()
    data_contratacao = models.DateField()

    REQUIRED_FIELDS = ['ni', 'data_nascimento', 'data_contratacao']

    def __str__(self):
        return f'{self.username} ({self.get_tipo_display()})'

# Model para cadastro de disciplinas no banco de dados. Com os campos de informação necessárias
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.CharField(max_length=100)
    carga_horaria = models.IntegerField()
    descricao = models.TextField(blank=True, null=True)
    professor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'tipo':'P'})

    def __str__(self):
        return self.nome

# Model para cadastro de salas no banco de dados. Com os campos de informação necessárias
class Sala(models.Model):
    nome = models.CharField(max_length=100)
    capacidade_alunos = models.IntegerField()

    def __str__(self):
        return self.nome

# Model para cadastro de reservas de ambientes no banco de dados. Com os campos de informação necessárias
class ReservaAmbiente(models.Model):
    PERIODO_CHOICES = [
        ('M', 'Manhã'), 
        ('T', 'Tarde'), 
        ('N', 'Noite'), 
    ]

    data_inicio = models.DateField()
    data_termino = models.DateField()
    periodo = models.CharField(max_length=1, choices=PERIODO_CHOICES, default='M')
    sala_reservada = models.ForeignKey(Sala, on_delete=models.CASCADE)
    professor = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'tipo':'P'})
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sala_reservada} - {self.get_periodo_display()} ({self.data_inicio} a {self.data_termino})'

    