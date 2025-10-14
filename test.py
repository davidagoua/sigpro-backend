import json
from cProfile import label

import pandas as pd
from pathlib import  Path

from core.models import Departement
from planification.models import Indicateur, Exercice
from programme.models import ComposantesProgram, Action, Activite, Quarter, ActiviteMonth, \
    TacheProgram, PlanificationCoutProgram, IndicateurProgram


def main():
    fichier = Path('./data/ptba_programme_remake.xlsx')

    gros_json = {
        'composantes': []
    }

    df = pd.read_excel(fichier, skiprows=20, sheet_name='1. ASN-Prg')

    for row in df.itertuples():
        if 'Composante' in str(row[1]):
            gros_json['composantes'].append({
                "name": row[1],
                "description": row[2],
                "actions": []
            })

        if 'Action' in str(row[1]) :
            gros_json['composantes'][-1]['actions'].append({
                "ddr": row[1],
                "name": row[2],
                "activites": []
            })

        if 'Activit' in str(row[1]):
            gros_json['composantes'][-1]['actions'][-1]['activites'].append({
                "name": row[1],
                "description": row[2],
                "responsable": row[6],
                "localisation": row[7],
                "type_activite": row[9],
                "2025":{
                    "Q1": {
                        "janv": row[10],
                        "fevr": row[11],
                        "mars": row[12],
                    },
                    "Q2": {
                        "avril": row[14],
                        "mai": row[15],
                        "juin": row[16],
                    },
                    "Q3": {
                        "juil": row[18],
                        "Aout": row[19],
                        "Sept": row[20],
                    },
                    "Q4": {
                        "Oct": row[22],
                        "Nov": row[23],
                        "Dec": row[24],
                    }
                },

                "taches": []
            })
        if 'Tache' in str(row[1]) or 'Tâche' in str(row[1]):
            gros_json['composantes'][-1]['actions'][-1]['activites'][-1]['taches'].append({
                "name": row[1],
                "description": row[2],
                "responsable": row[6],
                "localisation": row[7],
                "partenaire": row[8],
                "2025": {
                    "Q1": {}
                },
                "type_activite": row[9],

                "ild": row[25],
                "source": row[26],
                "unite": row[27],
                "quantity": row[28],
                "duree": row[29],
                "frecuence": row[30],
                "cout_unitaire": row[31],
                "cout_total": row[32],
                "ref_ddp": row[33],
                "ref_ddp_natures": row[34],
                "ref_ddp_actions": row[35],
                "ref_ddp_activites": row[36],
                "nature_economique": row[37],
                "ref_ddp_ligne_budgetaire": row[38],
                "ppm": row[39],
            })



    open(fichier.parent / 'test.json', 'w').write(json.dumps(gros_json))


def get_status(data) -> int:
    #row[10] if not pd.isna(row[10]) else 0
    if pd.isna(data):
        return 0
    elif len(data) == 0:
        return 0
    return 1

def ingest(sheet_name: str = "1. ASN-Prg"):
    fichier = Path('./ptba_programme_remake.xlsx')


    gros_json = {
        'composantes': [],
        'actions': [],
        'activites': [],
        'taches': []
    }

    df = pd.read_excel(fichier, skiprows=22, sheet_name=sheet_name)


    for row in df.itertuples():
        try:
            if 'Composante' in str(row[1]):
                ComposantesProgram.objects.create(label=row[1], description=row[2])
                gros_json['composantes'].append(True)

            if 'Action' in str(row[1]):
                Action.objects.create(
                    label=row[1],
                    description=row[2],
                    composante=ComposantesProgram.objects.last()
                )
                gros_json['actions'].append(True)

            if 'Activit' in str(row[1]):
                act = Activite.objects.create(
                    label=row[1],
                    description=row[2],
                    responsable=Departement.objects.filter(name=row[6]).first() if row[6] is not None else None,
                    localisation=row[7],
                    type_activite=row[9],
                    indicateur=IndicateurProgram.objects.filter(order=row[25]).first() if row[25] is not None else None,
                    action_id=Action.objects.last().pk
                )
                ActiviteMonth.objects.create(
                    activite=act,
                    quarter=Quarter.objects.get_or_create(label='Q1', annee=2025)[0],
                    label="Janvier",
                    status=get_status(row[10]),
                )
                ActiviteMonth.objects.create(
                    activite=act,
                    quarter=Quarter.objects.get_or_create(label='Q1', annee=2025)[0],
                    label="Fevrier",
                    status=get_status(row[11]),
                )
                ActiviteMonth.objects.create(
                    quarter=Quarter.objects.get_or_create(label='Q1', annee=2025)[0],
                    label="Mars",
                    status=get_status(row[12]),
                    activite=act,
                )
                ActiviteMonth.objects.create(
                    quarter=Quarter.objects.get_or_create(label='Q2', annee=2025)[0],
                    activite=act,
                    status=get_status(row[14]),
                    label="Avril",
                )
                ActiviteMonth.objects.create(
                    quarter=Quarter.objects.get_or_create(label='Q2', annee=2025)[0],
                    activite=act,
                    status=get_status(row[15]),
                    label="Mai",
                )
                ActiviteMonth.objects.create(
                    quarter=Quarter.objects.get_or_create(label='Q2', annee=2025)[0],
                    activite=act,
                    status=get_status(row[16]),
                    label="Juin",
                )
                ActiviteMonth.objects.create(
                    quarter=Quarter.objects.get_or_create(label='Q3', annee=2025)[0],
                    activite=act,
                    status=get_status(row[18]),
                    label="Juillet",
                )
                ActiviteMonth.objects.create(
                    quarter=Quarter.objects.get_or_create(label='Q3', annee=2025)[0],
                    activite=act,
                    status=get_status(row[19]),
                    label="Aout",
                )
                ActiviteMonth.objects.create(
                    quarter=Quarter.objects.get_or_create(label='Q3', annee=2025)[0],
                    activite=act,
                    status=get_status(row[20]),
                    label="Septembre",
                )
                ActiviteMonth.objects.create(
                    quarter=Quarter.objects.get_or_create(label='Q4', annee=2025)[0],
                    activite=act,
                    status=get_status(row[22]),
                    label="Octobre",
                )
                ActiviteMonth.objects.create(
                    quarter=Quarter.objects.get_or_create(label='Q4', annee=2025)[0],
                    activite=act,
                    status=get_status(row[23]),
                    label="Novembre",
                )
                ActiviteMonth.objects.create(
                    quarter=Quarter.objects.get_or_create(label='Q4', annee=2025)[0],
                    activite=act,
                    status=get_status(row[24]),
                    label="Decembre",

                )
                gros_json['activites'].append(True)

            if 'Tache' in str(row[1]) or 'Tâche' in str(row[1]):
                t = TacheProgram.objects.create(
                    label=row[1],
                    description=row[2],
                    responsable=row[6],
                    location=row[7],
                    partenaire=row[8],
                    activite=Activite.objects.last(),
                    activite_id=Activite.objects.last().pk,
                    indicateur=IndicateurProgram.objects.filter(order=row[25]).first() if row[25] is not None else None,
                    source=row[26],
                    ref_ddp=row[33],
                    ref_ddp_nature=row[34],
                    ref_ddp_action=row[35],
                    ref_ddp_activites=row[36],
                    ref_ddp_ligne=row[38],
                    ppm=row[39],
                    nature_economique=row[37],
                )
                PlanificationCoutProgram.objects.create(
                    exercice=Exercice.objects.filter(label__contains="2025").first(),
                    tache=t,
                    montant=row[31],
                    unite=row[27],
                    quantity=row[28],
                    duree=row[29],
                    frequence=row[30],
                    cout_unitaire=row[31],
                    # cout_total=row[32],

                )
                gros_json['taches'].append(True)
        except Exception as e:
            print(e)
            continue

    return gros_json


if __name__ == '__main__':
    ingest()