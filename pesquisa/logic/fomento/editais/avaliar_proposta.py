from datetime import datetime, timedelta

from django.core.exceptions import PermissionDenied
from django.db import transaction

import pydantic
from django_fsm import can_proceed

from pesquisa import tasks
from pesquisa.models import PropostaEditalFomento


class Comando(pydantic.BaseModel):
    proposta_id: int


class AvaliarProposta:
    def executar(comando: Comando) -> None:

        with transaction.atomic():
            proposta = PropostaEditalFomento.objects.select_for_update().get(pk=comando.proposta_id)

            if not can_proceed(proposta.avaliar):
                raise PermissionDenied()

            proposta.avaliar()
            proposta.save()

            # programa a interrupção automática da avaliação
            # caso ela não seja concluída em até 3 horas.
            transaction.on_commit(
                lambda: tasks.interromper_avaliacao_proposta.apply_async(
                    (proposta.id,), countdown=3 * 3600
                )
            )


executar = AvaliarProposta.executar
