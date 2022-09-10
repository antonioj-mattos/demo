from django.core.exceptions import PermissionDenied
from django.db import transaction

import pydantic
from django_fsm import can_proceed

from pesquisa.models import PropostaEditalFomento


class Comando(pydantic.BaseModel):
    proposta_id: int


class SubmeterProposta:
    def executar(comando: Comando) -> None:

        with transaction.atomic():
            proposta = PropostaEditalFomento.objects.select_for_update().get(pk=comando.proposta_id)

            if not can_proceed(proposta.submeter):
                raise PermissionDenied()

            proposta.submeter()
            proposta.save()


executar = SubmeterProposta.executar
