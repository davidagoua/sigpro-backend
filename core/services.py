import json
from pathlib import Path

from django.core.exceptions import MultipleObjectsReturned
from django.conf import global_settings
from planification.models import *


def decoder_texte(texte_encode):
    encodages = ['utf-8', 'latin-1', 'windows-1252', 'iso-8859-1']
    for encodage in encodages:
        try:
            texte_decode = texte_encode.encode('latin-1').decode(encodage)
            return texte_decode
        except UnicodeDecodeError:
            pass
        except UnicodeEncodeError:
            pass

    return texte_encode


def upload_ptba():
    file = Path(Path(__file__).parent / "./ptba.json")
    ptba = json.load(file.open('r'))


    for composant in ptba['data']['cs']:
        c = ComposantProjet.objects.create(label=composant['name'], ptba=PTBAProjet.objects.first())

        for sous_composant in composant['scs']:
            sc = SousComposantProjet.objects.create(label=decoder_texte(sous_composant['name']), composant=c)

            for indicateur in sous_composant['ilds']:
                ind = Indicateur.objects.create(
                    type = 'ILD' if indicateur['type'] == 'Ild' else 'HORS_ILD',
                    label = decoder_texte(indicateur['name']),
                    sous_composant=sc,
                )

                for tache in indicateur['activities']:
                    try:
                        t = Tache.objects.create(
                            label = decoder_texte(tache['name']),
                            unite= TypeUnite.objects.get_or_create(label=tache['unity'] if tache['unity'] is not None else '')[0],
                            categorie= CategorieDepense.objects.get_or_create(label=tache['category'] if tache['category'] is not None else '')[0],
                            indicateur=ind,
                            montant_engage=  tache['investmentProgram']['amountCommitted'] if tache['investmentProgram']['amountCommitted'] is not None else 0 ,
                            ugp=TypeUGP.objects.get_or_create(label=tache['monitoring'] if tache['monitoring'] is not None else '')[0],
                            responsable=tache['responsible'],
                            departement=Departement.objects.get_or_create(name=tache.get('responsible', 'ras')  if tache['responsible'] is not None else '')[0]
                        )

                        for invp in tache['investmentProgram']:
                            if isinstance(invp, dict) :
                                dc = Decaissement.objects.create(
                                    montant=invp['amountCommitted'] - invp['remainderPay'],
                                    tache=t
                                )

                        for i, inv in enumerate(tache['investmentProgram']['investments']):
                            p = PlanificationCout(
                                tache=t,
                                quantite=inv.get('quantity', 1) ,
                                cout=inv.get('price', inv['total']),
                                departement=Departement.objects.first(),
                                frequence=inv.get('frequency', 1) ,
                                exercice=Exercice.objects.filter(label__contains=inv['year'])[0]
                            )
                    except MultipleObjectsReturned  as e:
                        pass

    return ptba

if __name__ == "__main__":
    upload_ptba()