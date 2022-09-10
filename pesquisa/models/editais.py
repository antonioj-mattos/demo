from django.contrib.postgres import fields
from django.db import models

from django_fsm import FSMIntegerField, transition


class EstadoProposta:
    Aberta = 1
    Submetida = 2
    Recepcionada = 3
    Autorizada = 4
    Cancelada = 5


class PropostaEditalFomento(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()

    periodo_inscricao = fields.DateRangeField()
    periodo_selecao = fields.DateRangeField()

    estado = FSMIntegerField(default=EstadoProposta.Aberta, protected=True)

    aberta_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    @transition(
        field=estado,
        source=EstadoProposta.Aberta,
        target=EstadoProposta.Submetida,
    )
    def submeter(self):
        """O autor pode submeter a proposta para avaliação."""

    @transition(
        field=estado,
        source=EstadoProposta.Submetida,
        target=EstadoProposta.Aberta,
    )
    def editar(self):
        "O autor pode editar a proposta submetida mas não recepcionada para avaliação."

    @transition(
        field=estado,
        source=EstadoProposta.Aberta,
        target=EstadoProposta.Cancelada,
    )
    def cancelar(self):
        "O autor pode cancelar a proposta enquanto aberta."

    @transition(
        field=estado,
        source=EstadoProposta.Submetida,
        target=EstadoProposta.Recepcionada,
    )
    def avaliar(self):
        "O avaliador pode recepicionar a proposta para avaliação."

    @transition(
        field=estado,
        source=EstadoProposta.Recepcionada,
        target=EstadoProposta.Aberta,
    )
    def devolver(self):
        "O avaliador pode devolver a proposta após a avaliação."

    @transition(
        field=estado,
        source=EstadoProposta.Recepcionada,
        target=EstadoProposta.Submetida,
    )
    def interromper_avaliacao(self):
        "O avaliador pode interromper a avaliação."

    @transition(
        field=estado,
        source=EstadoProposta.Recepcionada,
        target=EstadoProposta.Autorizada,
    )
    def autorizar(self):
        "O avaliador pode autorizar a proposta."
