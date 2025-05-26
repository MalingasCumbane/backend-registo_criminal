

import requests
from django.conf import settings
from .models import Cidadao

class BIAPIClient:
    @staticmethod
    def fetch_citizen_data(bi_number):
        try:
            print("passsando o reg")
            response = requests.get(
                f"{settings.BI_API_URL}?bi_number={bi_number}",
                headers={'Authorization': f'Bearer {settings.BI_API_TOKEN}'},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar dados do BI: {str(e)}")
            return None
        
    def create_citizen_if_not_exists(bi_data):
        try:
            if Cidadao.objects.filter(numero_bi_nuit=bi_data['bi']).exists():
                return None
                
            if Cidadao.objects.filter(full_name__iexact=bi_data['nome']).exists():
                return None
                
            # Cria novo registro
            citizen = Cidadao.objects.create(
                numero_bi_nuit=bi_data['bi_number'],
                full_name=bi_data['nome_completo'],
                data_nascimento=bi_data['data_nascimento'],
                naturalidade=bi_data.get('naturalidade'),
                estado_civil=bi_data.get('estado_civil'),
                residencia=bi_data.get('residencia'),
                sexo=bi_data.get('sexo'),
                local_emissao_bi=bi_data.get('emitido_em'),
                data_emissao_bi=bi_data.get('data_emissao'),
                data_validade_bi=bi_data.get('valido_ate'),
                # Outros campos...
            )
            return citizen
        except Exception as e:
            print(f"Erro ao criar cidadão: {str(e)}")
            return None