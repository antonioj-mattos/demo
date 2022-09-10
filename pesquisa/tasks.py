from django.db import transaction

from django_fsm import can_proceed

from config.celery_app import app
from pesquisa.models import PropostaEditalFomento


@app.task(bind=True)
def interromper_avaliacao_proposta(self, proposta_id: int) -> None:
    with transaction.atomic():
        proposta = PropostaEditalFomento.objects.select_for_update().get(pk=proposta_id)

        if can_proceed(proposta.interromper_avaliacao):
            proposta.interromper_avaliacao()
            proposta.save()

            transaction.on_commit(
                lambda: print(f"Avaliação da proposta [{proposta.id}] interrompida - tempo excedido.")
            )
