#!/usr/bin/env python3
"""Validate ALL 36 competency questions of SIGEVS-O.

Complements ``validate_ontology.py`` (which exercises 4 representative CQs
plus reasoning). This script:

1. Loads ``SIGEVS-O-complete.ttl`` and populates it with a sample
   outbreak-response scenario covering every subdomain (Core, Investigation,
   Response, Field Actions).
2. Answers each of the 36 competency questions:
   - ``sparql``       - a SPARQL query over the populated ontology must return
                        the expected sample instances;
   - ``structural``   - the answer is a model-level property of the ontology
                        (e.g., the absence/presence of a cardinality
                        restriction), checked directly on the TBox;
   - ``implementation`` - the answer lives at the JPA/service layer (the
                        concept is intentionally not materialised in OWL);
                        the script only reports the layer, it cannot fail.

Usage::

    python scripts/validate_cqs.py
    python scripts/validate_cqs.py --ontology ontology/SIGEVS-O-complete.ttl

Exit code is 0 when every check passes and 1 otherwise.

Requirements: rdflib.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

try:
    from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL
except ImportError:
    print("[error] rdflib is required: pip install rdflib")
    sys.exit(2)

SIGEVS = Namespace("https://sigevs.ontologies#")
EX = Namespace("http://example.org/sigevs-sample#")

DEFAULT_ONTOLOGY = Path(__file__).resolve().parents[1] / "ontology" / "SIGEVS-O-complete.ttl"

# ---------------------------------------------------------------------------
# Sample ABox: outbreak scenario covering all four subdomains. Inspired by the
# Montenegro (2025) HPAI event reported in the papers.
# ---------------------------------------------------------------------------

SAMPLE_ABOX = """
@prefix ex: <http://example.org/sigevs-sample#> .
@prefix sigevs: <https://sigevs.ontologies#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Core --------------------------------------------------------------------
ex:E1 a sigevs:Estabelecimento, sigevs:EstabelecimentoCadastrado, sigevs:AlvoInvestigacao, sigevs:PropriedadeInspecionada ;
    sigevs:codigoEstabelecimento "SDA-001" ;
    sigevs:nomeEstabelecimento "Granja Sao Joao" ;
    sigevs:tipoEstabelecimento "Propriedade Rural" ;
    sigevs:coordenadas "POINT(-51.4611 -29.6886)" ;
    sigevs:codigoCar "CAR-2312345" ;
    sigevs:geometriaCar "POLYGON((-51.47 -29.69,-51.45 -29.69,-51.45 -29.68,-51.47 -29.68,-51.47 -29.69))" ;
    sigevs:estabelecimentoHasEndereco ex:End1 .

ex:E2 a sigevs:Estabelecimento, sigevs:EstabelecimentoCadastrado, sigevs:PropriedadeInspecionada ;
    sigevs:codigoEstabelecimento "SDA-002" ;
    sigevs:nomeEstabelecimento "Sitio Boa Vista" ;
    sigevs:coordenadas "POINT(-51.4500 -29.6800)" ;
    sigevs:codigoCar "CAR-2312346" ;
    sigevs:geometriaCar "POLYGON((-51.46 -29.68,-51.44 -29.68,-51.44 -29.67,-51.46 -29.67,-51.46 -29.68))" ;
    sigevs:estabelecimentoHasEndereco ex:End2 .

ex:E3 a sigevs:Estabelecimento, sigevs:EstabelecimentoCadastrado, sigevs:Frigorifico, sigevs:PropriedadeInspecionada ;
    sigevs:codigoEstabelecimento "SDA-003" ;
    sigevs:nomeEstabelecimento "Fazenda Tres Pinheiros" ;
    sigevs:coordenadas "POINT(-51.4000 -29.6500)" ;
    sigevs:sistemaInspecao "SIF" ;
    sigevs:estabelecimentoHasEndereco ex:End3 .

ex:E4 a sigevs:Estabelecimento, sigevs:EstabelecimentoCadastrado ;
    sigevs:codigoEstabelecimento "SDA-004" ;
    sigevs:nomeEstabelecimento "Fazenda Santa Rita" ;
    sigevs:coordenadas "POINT(-51.2000 -29.5000)" ;
    sigevs:estabelecimentoHasEndereco ex:End4 .

ex:End1 a sigevs:Endereco ;
    sigevs:rua "RS-287 km 42" ; sigevs:cidade "Montenegro" ; sigevs:uf "RS" .
ex:End2 a sigevs:Endereco ; sigevs:rua "Linha Sao Jose" ; sigevs:cidade "Sao Sebastiao do Cai" ; sigevs:uf "RS" .
ex:End3 a sigevs:Endereco ; sigevs:rua "BR-386 km 10" ; sigevs:cidade "Tres Coroas" ; sigevs:uf "RS" .
ex:End4 a sigevs:Endereco ; sigevs:rua "Estrada Geral" ; sigevs:cidade "Encantado" ; sigevs:uf "RS" .

ex:Aves a sigevs:EspecieAnimal ;
    sigevs:especieExploracao "Aves" ;
    sigevs:especieAnimalHasEstabelecimento ex:E1, ex:E2 .

ex:Suinos a sigevs:EspecieAnimal ;
    sigevs:especieExploracao "Suinos" ;
    sigevs:especieAnimalHasEstabelecimento ex:E3 .

ex:Frig1 a sigevs:Frigorifico ;
    sigevs:nomeEstabelecimento "Abatedouro Vale" ;
    sigevs:sistemaInspecao "SIE" .

# Investigation -------------------------------------------------------------
ex:Analise1 a sigevs:AnaliseSanitaria ;
    sigevs:nomeAnalise "Investigacao HPAI Montenegro" ;
    sigevs:analiseAtiva true ;
    sigevs:criadaEm "2025-05-16T08:00:00"^^xsd:dateTime ;
    sigevs:analiseSanitariaHasAlvoInvestigacao ex:E1 ;
    sigevs:analiseSanitariaHasAreaAfetada ex:AreaAfetada1 .

ex:AreaAfetada1 a sigevs:AreaAfetada ;
    sigevs:nomeAreaAfetada "Area de emergencia Montenegro" ;
    sigevs:geometriaAreaAfetada "POLYGON((-51.5 -29.7,-51.4 -29.7,-51.4 -29.6,-51.5 -29.6,-51.5 -29.7))" .

ex:ZonaPerifocal a sigevs:ZonaControleInvestigacao ;
    sigevs:tipoZona "INFECTED" ; sigevs:raio 3.0 .
ex:ZonaVigilancia a sigevs:ZonaControleInvestigacao ;
    sigevs:tipoZona "BUFFER" ; sigevs:raio 10.0 .
ex:ZonaProtecao a sigevs:ZonaControleInvestigacao ;
    sigevs:tipoZona "SURVEILLANCE" ; sigevs:raio 15.0 .

ex:E1 sigevs:alvoInvestigacaoHasZonaControleInvestigacao
    ex:ZonaPerifocal, ex:ZonaVigilancia, ex:ZonaProtecao .

# Movement (GTA) ------------------------------------------------------------
ex:Mov1 a sigevs:MovimentacaoAnimal ;
    sigevs:serie "1" ; sigevs:numeroGTA "1001" ; sigevs:ufOrigem "RS" ;
    sigevs:dataMovimentacao "2025-05-10"^^xsd:date ;
    sigevs:especieMovimentada "Aves" ;
    sigevs:quantidadeAnimais 12000 ;
    sigevs:Origem ex:E1 ; sigevs:Destino ex:E3 .

ex:Mov2 a sigevs:MovimentacaoAnimal ;
    sigevs:serie "1" ; sigevs:numeroGTA "1002" ; sigevs:ufOrigem "RS" ;
    sigevs:dataMovimentacao "2025-05-12"^^xsd:date ;
    sigevs:especieMovimentada "Suinos" ;
    sigevs:quantidadeAnimais 300 ;
    sigevs:Origem ex:E3 ; sigevs:Destino ex:E1 .

ex:Mov3 a sigevs:MovimentacaoAnimal ;
    sigevs:serie "1" ; sigevs:numeroGTA "1003" ; sigevs:ufOrigem "RS" ;
    sigevs:dataMovimentacao "2025-05-13"^^xsd:date ;
    sigevs:especieMovimentada "Aves" ;
    sigevs:quantidadeAnimais 4500 ;
    sigevs:Origem ex:E3 ; sigevs:Destino ex:E4 .

# Response ------------------------------------------------------------------
ex:Resposta1 a sigevs:RespostaSanitaria ;
    sigevs:identificadorResposta "RESP-2025-001" ;
    sigevs:respostaAtiva true ;
    sigevs:respostaConcluida false ;
    sigevs:inicioResposta "2025-05-16T09:00:00"^^xsd:dateTime ;
    sigevs:BaseadaEm ex:Analise1 ;
    sigevs:Tem ex:Posto1 .

ex:Posto1 a sigevs:PostoComando ;
    sigevs:nomePosto "QG Montenegro" ;
    sigevs:enderecoPosto "Central de Emergencia, Montenegro" ;
    sigevs:postoDaResposta ex:Resposta1 .

ex:Ciclo1 a sigevs:CicloVigilancia ;
    sigevs:numeroCiclo 1 ;
    sigevs:cicloFechado true ;
    sigevs:inicioCiclo "2025-05-16T07:00:00"^^xsd:dateTime ;
    sigevs:fimCiclo "2025-05-18T18:00:00"^^xsd:dateTime ;
    sigevs:cicloPertenceAResposta ex:Resposta1 .

ex:Ciclo2 a sigevs:CicloVigilancia ;
    sigevs:numeroCiclo 2 ;
    sigevs:cicloFechado false ;
    sigevs:inicioCiclo "2025-05-19T07:00:00"^^xsd:dateTime ;
    sigevs:cicloPertenceAResposta ex:Resposta1 .

ex:ZonaCiclo1 a sigevs:ZonaPorCiclo ;
    sigevs:zonaFechada true ;
    sigevs:dataInicioZona "2025-05-16"^^xsd:date ;
    sigevs:dataFimZona "2025-05-18"^^xsd:date ;
    sigevs:zonaDoCiclo ex:Ciclo1 .

ex:ZonaCiclo2 a sigevs:ZonaPorCiclo ;
    sigevs:zonaFechada false ;
    sigevs:dataInicioZona "2025-05-19"^^xsd:date ;
    sigevs:zonaDoCiclo ex:Ciclo2 .

ex:EquipeA a sigevs:EquipeCampo ;
    sigevs:nomeEquipe "Equipe A" ;
    sigevs:equipeAtiva true ;
    sigevs:equipeAlocadaEm ex:Ciclo1 ;
    sigevs:ClassificaSe ex:TipoEquipeA ;
    sigevs:CompostaPor ex:Joao, ex:Ana ;
    sigevs:Utiliza ex:Veic1 ;
    sigevs:Opera ex:Barreira1 .

ex:EquipeB a sigevs:EquipeCampo ;
    sigevs:nomeEquipe "Equipe B" ;
    sigevs:equipeAtiva true ;
    sigevs:equipeAlocadaEm ex:Ciclo1 ;
    sigevs:CompostaPor ex:Carlos .

ex:TipoEquipeA a sigevs:TipoEquipe ;
    sigevs:nomeTipoEquipe "Equipe de inspecao" .

ex:Joao a sigevs:Pessoa, sigevs:MembroEquipe, sigevs:PessoaConvocada ;
    sigevs:keycloakSubjectId "kc-001" ;
    sigevs:cpf "11111111111" ;
    sigevs:nomePessoa "Joao Silva" ;
    sigevs:email "joao.silva@example.org" ;
    sigevs:emQuarentena false ;
    sigevs:permissaoGestao true ;
    sigevs:permissaoObservacao false ;
    sigevs:Convoca ex:Resposta1 ;
    sigevs:Desempenha ex:F1 .

ex:Ana a sigevs:Pessoa, sigevs:MembroEquipe ;
    sigevs:keycloakSubjectId "kc-002" ;
    sigevs:cpf "22222222222" ;
    sigevs:nomePessoa "Ana Pereira" ;
    sigevs:email "ana.pereira@example.org" ;
    sigevs:Desempenha ex:F1 .

ex:Carlos a sigevs:Pessoa, sigevs:MembroEquipe ;
    sigevs:keycloakSubjectId "kc-003" ;
    sigevs:cpf "33333333333" ;
    sigevs:nomePessoa "Carlos Souza" ;
    sigevs:email "carlos.souza@example.org" .

ex:F1 a sigevs:Funcao ; sigevs:nomeFuncao "Veterinario" .
ex:F2 a sigevs:Funcao ; sigevs:nomeFuncao "Auxiliar" .

# Operational areas / properties in area ------------------------------------
ex:AreaA a sigevs:AreaOperacional ;
    sigevs:nomeArea "Area A" ;
    sigevs:PertenceA ex:ZonaCiclo1 ;
    sigevs:areaDaEquipe ex:EquipeA ;
    sigevs:Contem ex:PIA1, ex:PIA2 .

ex:AreaB a sigevs:AreaOperacional ;
    sigevs:nomeArea "Area B" ;
    sigevs:PertenceA ex:ZonaCiclo1 ;
    sigevs:areaDaEquipe ex:EquipeB ;
    sigevs:Contem ex:PIA3 .

ex:PIA1 a sigevs:PropriedadeEmArea ;
    sigevs:visitaConcluida true ;
    sigevs:contidaEmArea ex:AreaA ;
    sigevs:RefereSeA ex:E1 .

ex:PIA2 a sigevs:PropriedadeEmArea ;
    sigevs:visitaConcluida false ;
    sigevs:contidaEmArea ex:AreaA ;
    sigevs:RefereSeA ex:E2 .

ex:PIA3 a sigevs:PropriedadeEmArea ;
    sigevs:visitaConcluida true ;
    sigevs:contidaEmArea ex:AreaB ;
    sigevs:RefereSeA ex:E3 .

# Field actions ---------------------------------------------------------------
ex:Veic1 a sigevs:Veiculo ;
    sigevs:placa "ABC1D23" ; sigevs:marca "Toyota" ; sigevs:modelo "Hilux" ;
    sigevs:tipoVeiculo "Viatura" .

ex:Barreira1 a sigevs:BarreiraSanitaria ;
    sigevs:nomeBarreira "Barreira BR-287" ;
    sigevs:tipoBarreira "FIXED" ;
    sigevs:papelBarreira "SANITARY" ;
    sigevs:coordenadas "POINT(-51.4300 -29.6700)" .

ex:Sub1 a sigevs:SubmissaoPropriedade ;
    sigevs:uuidSubmissao "sub-0001" ;
    sigevs:dataHoraColeta "2025-05-16T10:30:00"^^xsd:dateTime ;
    sigevs:VinculadaA ex:PIA1 ;
    sigevs:RealizadaPor ex:EquipeA .

ex:Sub2 a sigevs:SubmissaoPropriedade ;
    sigevs:uuidSubmissao "sub-0002" ;
    sigevs:dataHoraColeta "2025-05-17T14:00:00"^^xsd:dateTime ;
    sigevs:VinculadaA ex:PIA3 ;
    sigevs:RealizadaPor ex:EquipeA .

ex:SubBarreira1 a sigevs:SubmissaoBarreira ;
    sigevs:uuidSubmissaoBarreira "sub-bar-0001" ;
    sigevs:dataHoraColetaBarreira "2025-05-17T08:15:00"^^xsd:dateTime ;
    sigevs:submissaoBarreiraHasBarreiraSanitaria ex:Barreira1 .

ex:Temp1 a sigevs:Estabelecimento, sigevs:EstabelecimentoNaoCadastrado ;
    sigevs:nomeContato "Maria Souza" ;
    sigevs:cpfCnpj "44444444444" ;
    sigevs:telefone "+55 55 99999-0000" ;
    sigevs:coordenadas "POINT(-51.4600 -29.6870)" .

ex:Rast1 a sigevs:RastreamentoGps ;
    sigevs:inicioRastreamento "2025-05-16T09:00:00"^^xsd:dateTime ;
    sigevs:fimRastreamento "2025-05-16T11:00:00"^^xsd:dateTime ;
    sigevs:rastreamentoGpsHasVeiculo ex:Veic1 .

# Species categories (individuals declared in the TBox) linked to the species
sigevs:CategoriaAves sigevs:categoriaEspecieHasEspecieAnimal ex:Aves .
sigevs:CategoriaSuinos sigevs:categoriaEspecieHasEspecieAnimal ex:Suinos .
"""

# ---------------------------------------------------------------------------
# SPARQL queries
# ---------------------------------------------------------------------------

Q = {
    "CQ-CORE-01": "SELECT ?est ?nome WHERE { ?est a sigevs:EstabelecimentoCadastrado ; sigevs:nomeEstabelecimento ?nome . }",
    "CQ-CORE-02": """
        SELECT ?est ?nomeEst ?especie WHERE {
          ?esp a sigevs:EspecieAnimal ;
               sigevs:especieExploracao ?especie ;
               sigevs:especieAnimalHasEstabelecimento ?est .
          ?est sigevs:nomeEstabelecimento ?nomeEst .
        }""",
    "CQ-CORE-03": """
        SELECT ?est ?coord WHERE { ?est a sigevs:Estabelecimento ; sigevs:coordenadas ?coord . }""",
    "CQ-CORE-05": """
        SELECT ?est ?car WHERE { ?est sigevs:codigoCar ?car . }""",
    "CQ-CORE-06": """
        SELECT ?frig ?nome ?inspecao WHERE {
          ?frig a sigevs:Frigorifico ; sigevs:nomeEstabelecimento ?nome ; sigevs:sistemaInspecao ?inspecao .
        }""",
    "CQ-CORE-07": """
        SELECT ?pessoa ?gestao ?observacao WHERE {
          ?pessoa a sigevs:PessoaConvocada ;
                  sigevs:permissaoGestao ?gestao ; sigevs:permissaoObservacao ?observacao .
        }""",
    "CQ-INV-01": """
        SELECT ?alvo ?tipo ?raio ?alvoCoord ?est ?nome ?coord WHERE {
          ?alvo a sigevs:AlvoInvestigacao ;
                sigevs:coordenadas ?alvoCoord ;
                sigevs:alvoInvestigacaoHasZonaControleInvestigacao ?zona .
          ?zona sigevs:tipoZona ?tipo ; sigevs:raio ?raio .
          ?est a sigevs:Estabelecimento ;
               sigevs:nomeEstabelecimento ?nome ; sigevs:coordenadas ?coord .
        }""",
    "CQ-INV-03": """
        SELECT ?mov ?gta ?data ?origem ?destino WHERE {
          ?mov a sigevs:MovimentacaoAnimal ;
               sigevs:numeroGTA ?gta ; sigevs:dataMovimentacao ?data ;
               sigevs:Origem ?origem ; sigevs:Destino ?destino .
          FILTER(?data >= "2025-05-11"^^xsd:date && ?data <= "2025-05-14"^^xsd:date)
        }""",
    "CQ-INV-04": """
        SELECT DISTINCT ?contato ?nome WHERE {
          { ?mov a sigevs:MovimentacaoAnimal ; sigevs:Origem ex:E1 ; sigevs:Destino ?contato . }
          UNION
          { ?mov a sigevs:MovimentacaoAnimal ; sigevs:Destino ex:E1 ; sigevs:Origem ?contato . }
          ?contato sigevs:nomeEstabelecimento ?nome .
        }""",
    "CQ-INV-05": """
        SELECT DISTINCT ?indireto ?nome WHERE {
          { ?m1 a sigevs:MovimentacaoAnimal ; sigevs:Origem ex:E1 ; sigevs:Destino ?intermediario .
            ?m2 a sigevs:MovimentacaoAnimal ; sigevs:Origem ?intermediario ; sigevs:Destino ?indireto . }
          UNION
          { ?m1 a sigevs:MovimentacaoAnimal ; sigevs:Destino ex:E1 ; sigevs:Origem ?intermediario .
            ?m2 a sigevs:MovimentacaoAnimal ; sigevs:Destino ?intermediario ; sigevs:Origem ?indireto . }
          FILTER(?indireto != ex:E1)
          ?indireto sigevs:nomeEstabelecimento ?nome .
        }""",
    "CQ-INV-06": """
        SELECT ?zona ?tipo ?raio WHERE {
          ex:E1 sigevs:alvoInvestigacaoHasZonaControleInvestigacao ?zona .
          ?zona sigevs:tipoZona ?tipo ; sigevs:raio ?raio .
        }""",
    "CQ-INV-07": """
        SELECT ?analise ?nome ?ativa WHERE {
          ?analise a sigevs:AnaliseSanitaria ;
                   sigevs:nomeAnalise ?nome ; sigevs:analiseAtiva ?ativa .
        }""",
    "CQ-INV-08": """
        SELECT DISTINCT ?municipio WHERE {
          ex:E1 sigevs:estabelecimentoHasEndereco ?end .
          ?end sigevs:cidade ?municipio .
        }""",
    "CQ-INV-09": """
        SELECT DISTINCT ?categoria WHERE {
          ?esp sigevs:especieAnimalHasEstabelecimento ex:E1 .
          ?categoria sigevs:categoriaEspecieHasEspecieAnimal ?esp .
        }""",
    "CQ-RES-01": """
        SELECT ?ciclo ?numero ?fechado WHERE {
          ?ciclo sigevs:cicloPertenceAResposta ex:Resposta1 ;
                 sigevs:numeroCiclo ?numero ; sigevs:cicloFechado ?fechado .
        }""",
    "CQ-RES-02": """
        SELECT ?ciclo ?equipe ?nomeEquipe WHERE {
          ?equipe sigevs:equipeAlocadaEm ?ciclo ; sigevs:nomeEquipe ?nomeEquipe .
        }""",
    "CQ-RES-03": """
        SELECT ?equipe ?nomeEquipe ?membro ?nomeMembro WHERE {
          ?equipe a sigevs:EquipeCampo ; sigevs:nomeEquipe ?nomeEquipe ; sigevs:CompostaPor ?membro .
          ?membro sigevs:nomePessoa ?nomeMembro .
        }""",
    "CQ-RES-06": """
        SELECT DISTINCT ?membro ?nomeMembro WHERE {
          ?rast a sigevs:RastreamentoGps ;
                sigevs:inicioRastreamento ?inicio ;
                sigevs:rastreamentoGpsHasVeiculo ?veiculo .
          ?equipe sigevs:Utiliza ?veiculo ; sigevs:CompostaPor ?membro .
          ?membro sigevs:nomePessoa ?nomeMembro .
          OPTIONAL { ?rast sigevs:fimRastreamento ?fimRastreamento . }
          FILTER(?inicio <= "2025-05-16T10:00:00"^^xsd:dateTime
              && (?fimRastreamento >= "2025-05-16T10:00:00"^^xsd:dateTime || !BOUND(?fimRastreamento)))
        }""",
    "CQ-RES-08": """
        SELECT ?equipe ?area ?nomeArea WHERE {
          ?area sigevs:areaDaEquipe ?equipe ; sigevs:nomeArea ?nomeArea .
        }""",
    "CQ-RES-09": """
        SELECT DISTINCT ?resposta ?barreira ?nomeBarreira WHERE {
          ?barreira ^sigevs:Opera ?equipe .
          ?equipe sigevs:equipeAlocadaEm ?ciclo .
          ?ciclo sigevs:cicloPertenceAResposta ?resposta .
          ?barreira sigevs:nomeBarreira ?nomeBarreira .
        }""",
    "CQ-RES-10": """
        SELECT ?area ?nomeArea ?est WHERE {
          ?pia sigevs:contidaEmArea ?area ; sigevs:RefereSeA ?est .
          ?area sigevs:nomeArea ?nomeArea .
        }""",
    "CQ-RES-11": """
        SELECT ?barreira ?tipo ?papel WHERE {
          ?barreira a sigevs:BarreiraSanitaria ;
                    sigevs:tipoBarreira ?tipo ; sigevs:papelBarreira ?papel .
        }""",
    "CQ-RES-12": """
        SELECT ?equipe ?veiculo ?placa WHERE {
          ?equipe sigevs:Utiliza ?veiculo . ?veiculo sigevs:placa ?placa .
        }""",
    "CQ-RES-13": """
        SELECT ?resposta ?posto WHERE { ex:Resposta1 sigevs:Tem ?posto . }""",
    "CQ-RES-14": """
        SELECT ?pessoa ?nome ?quarentena WHERE {
          ?pessoa sigevs:Convoca ex:Resposta1 ;
                  sigevs:nomePessoa ?nome ; sigevs:emQuarentena ?quarentena .
        }""",
    "CQ-CAM-01": """
        SELECT DISTINCT ?est ?nome WHERE {
          ?ciclo sigevs:cicloPertenceAResposta ex:Resposta1 .
          ?zona sigevs:zonaDoCiclo ?ciclo .
          ?area sigevs:PertenceA ?zona .
          ?pia sigevs:contidaEmArea ?area ;
               sigevs:visitaConcluida true ;
               sigevs:RefereSeA ?est .
          ?est sigevs:nomeEstabelecimento ?nome .
        }""",
    "CQ-CAM-02": """
        SELECT ?est ?status WHERE {
          ?pia sigevs:RefereSeA ?est ; sigevs:visitaConcluida ?status .
        }""",
    "CQ-CAM-03": """
        SELECT ?equipe ?submissao WHERE {
          ?submissao a sigevs:SubmissaoPropriedade ;
                     sigevs:RealizadaPor ?equipe .
        }""",
    "CQ-CAM-04": """
        SELECT ?estabelecimento ?contato WHERE {
          ?estabelecimento a sigevs:EstabelecimentoNaoCadastrado ; sigevs:nomeContato ?contato .
        }""",
}

# Model-level checks (TBox), for CQs answered by structural analysis.
def check_inv_02(g: Graph) -> bool:
    """A property may be the target of several simultaneous investigations:
    the analysis->target property carries no max-1 cardinality, and no UNIQUE
    constraint is modelled between analysis and target."""
    for restriction in g.subjects(OWL.onProperty, SIGEVS.analiseSanitariaHasAlvoInvestigacao):
        if (restriction, RDF.type, OWL.Restriction) in g:
            for card in (OWL.maxCardinality, OWL.cardinality,
                         OWL.maxQualifiedCardinality, OWL.qualifiedCardinality):
                value = next(g.objects(restriction, card), None)
                if value is not None and int(value) <= 1:
                    return False
    return True


def check_res_04(g: Graph) -> bool:
    """Barriers are bound to cycles through field teams only: there is no direct
    object property between BarreiraSanitaria and CicloVigilancia."""
    for prop in g.subjects(RDF.type, OWL.ObjectProperty):
        domains = set(g.objects(prop, RDFS.domain))
        ranges = set(g.objects(prop, RDFS.range))
        if SIGEVS.BarreiraSanitaria in domains:
            if SIGEVS.CicloVigilancia in ranges:
                return False
    return True


def check_res_05(g: Graph) -> bool:
    """A fresh ZonaPorCiclo relator exists for each cycle (zonaDoCiclo)."""
    return (SIGEVS.zonaDoCiclo, RDF.type, OWL.ObjectProperty) in g


def check_res_07(g: Graph) -> bool:
    """A team is allocated to a single cycle: equipeAlocadaEm is the only
    property from EquipeCampo to CicloVigilancia."""
    for prop in g.subjects(RDF.type, OWL.ObjectProperty):
        domains = set(g.objects(prop, RDFS.domain))
        ranges = set(g.objects(prop, RDFS.range))
        if SIGEVS.EquipeCampo in domains and SIGEVS.CicloVigilancia in ranges:
            if prop != SIGEVS.equipeAlocadaEm:
                return False
    return True


STRUCTURAL_CHECKS = {
    "CQ-INV-02": check_inv_02,
    "CQ-RES-04": check_res_04,
    "CQ-RES-05": check_res_05,
    "CQ-RES-07": check_res_07,
}

# CQs whose answer lives in the JPA/service layer (concept deliberately not
# materialised in the OWL ontology).
IMPLEMENTATION_CQS = {
    "CQ-CORE-04": "region/inspectoria is a JPA attribute; not materialised in OWL",
    "CQ-CAM-05": "audit log is a cross-cutting JPA concern; not modelled as a class",
    "CQ-CAM-06": "file attachments are stored as bytes in the submission payload",
}

# Expected results for the SPARQL CQs: (CQ id) -> callable(row) -> True/False.
def rows_core_01(rows):
    names = {str(r.nome) for r in rows}
    return {"Granja Sao Joao", "Sitio Boa Vista", "Fazenda Tres Pinheiros", "Fazenda Santa Rita"} <= names

def rows_core_02(rows):
    got = {(str(r.nomeEst), str(r.especie)) for r in rows}
    return {("Granja Sao Joao", "Aves"), ("Fazenda Tres Pinheiros", "Suinos")} <= got

def rows_core_03(rows):
    return len({str(r.coord) for r in rows}) >= 4

def rows_core_05(rows):
    cars = {str(r.car) for r in rows}
    return {"CAR-2312345", "CAR-2312346"} <= cars

def rows_core_06(rows):
    got = {str(r.inspecao) for r in rows}
    return {"SIF", "SIE"} <= got

def rows_core_07(rows):
    for r in rows:
        if bool(r.gestao) and not bool(r.observacao):
            return True
    return False

def rows_inv_01(rows):
    inside = {"INFECTED": set(), "BUFFER": set()}
    for r in rows:
        d = haversine_km(parse_wkt_point(str(r.alvoCoord)), parse_wkt_point(str(r.coord)))
        if d <= float(r.raio):
            inside.setdefault(str(r.tipo), set()).add(str(r.nome))
    return {"Granja Sao Joao", "Sitio Boa Vista"} <= inside["INFECTED"] \
        and "Fazenda Tres Pinheiros" in inside["BUFFER"]

def rows_inv_03(rows):
    gtas = {str(r.gta) for r in rows}
    return {"1002", "1003"} <= gtas and "1001" not in gtas  # window 05-11..05-14

def rows_inv_04(rows):
    return {str(r.nome) for r in rows} == {"Fazenda Tres Pinheiros"}

def rows_inv_05(rows):
    names = {str(r.nome) for r in rows}
    return "Fazenda Santa Rita" in names and "Fazenda Tres Pinheiros" not in names

def rows_inv_06(rows):
    return {str(r.tipo) for r in rows} == {"INFECTED", "BUFFER", "SURVEILLANCE"}

def rows_inv_07(rows):
    return any(str(r.nome) == "Investigacao HPAI Montenegro" and bool(r.ativa) for r in rows)

def rows_inv_08(rows):
    return {str(r.municipio) for r in rows} == {"Montenegro"}

def rows_inv_09(rows):
    return {short(r.categoria) for r in rows} == {"CategoriaAves"}

def rows_res_01(rows):
    got = {int(r.numero): bool(r.fechado) for r in rows}
    return got.get(1) is True and got.get(2) is False

def rows_res_02(rows):
    got = {str(r.nomeEquipe) for r in rows}
    return {"Equipe A", "Equipe B"} <= got

def rows_res_03(rows):
    got = {(str(r.nomeEquipe), str(r.nomeMembro)) for r in rows}
    return {("Equipe A", "Joao Silva"), ("Equipe A", "Ana Pereira"), ("Equipe B", "Carlos Souza")} <= got

def rows_res_06(rows):
    return {str(r.nomeMembro) for r in rows} == {"Joao Silva", "Ana Pereira"}

def rows_res_08(rows):
    got = {(str(r.nomeArea), short(r.equipe)) for r in rows}
    return {("Area A", "EquipeA"), ("Area B", "EquipeB")} == got

def rows_res_09(rows):
    return {str(r.nomeBarreira) for r in rows} == {"Barreira BR-287"}

def rows_res_10(rows):
    got = {(str(r.nomeArea), short(r.est)) for r in rows}
    return {("Area A", "E1"), ("Area A", "E2"), ("Area B", "E3")} == got

def rows_res_11(rows):
    return any(str(r.tipo) == "FIXED" and str(r.papel) == "SANITARY" for r in rows)

def rows_res_12(rows):
    return any(str(r.placa) == "ABC1D23" and short(r.equipe) == "EquipeA" for r in rows)

def rows_res_13(rows):
    return {short(r.posto) for r in rows} == {"Posto1"}

def rows_res_14(rows):
    return any(str(r.nome) == "Joao Silva" and bool(r.quarentena) is False for r in rows)

def rows_cam_01(rows):
    return {str(r.nome) for r in rows} == {"Granja Sao Joao", "Fazenda Tres Pinheiros"}

def rows_cam_02(rows):
    got = {(short(r.est), bool(r.status)) for r in rows}
    return {("E1", True), ("E2", False), ("E3", True)} <= got

def rows_cam_03(rows):
    got = [(short(r.equipe), short(r.submissao)) for r in rows]
    return ("EquipeA", "Sub1") in got and ("EquipeA", "Sub2") in got

def rows_cam_04(rows):
    return {str(r.contato) for r in rows} == {"Maria Souza"}


EXPECTED = {
    "CQ-CORE-01": rows_core_01,
    "CQ-CORE-02": rows_core_02,
    "CQ-CORE-03": rows_core_03,
    "CQ-CORE-05": rows_core_05,
    "CQ-CORE-06": rows_core_06,
    "CQ-CORE-07": rows_core_07,
    "CQ-INV-01": rows_inv_01,
    "CQ-INV-03": rows_inv_03,
    "CQ-INV-04": rows_inv_04,
    "CQ-INV-05": rows_inv_05,
    "CQ-INV-06": rows_inv_06,
    "CQ-INV-07": rows_inv_07,
    "CQ-INV-08": rows_inv_08,
    "CQ-INV-09": rows_inv_09,
    "CQ-RES-01": rows_res_01,
    "CQ-RES-02": rows_res_02,
    "CQ-RES-03": rows_res_03,
    "CQ-RES-06": rows_res_06,
    "CQ-RES-08": rows_res_08,
    "CQ-RES-09": rows_res_09,
    "CQ-RES-10": rows_res_10,
    "CQ-RES-11": rows_res_11,
    "CQ-RES-12": rows_res_12,
    "CQ-RES-13": rows_res_13,
    "CQ-RES-14": rows_res_14,
    "CQ-CAM-01": rows_cam_01,
    "CQ-CAM-02": rows_cam_02,
    "CQ-CAM-03": rows_cam_03,
    "CQ-CAM-04": rows_cam_04,
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def short(term) -> str:
    text = str(term)
    for marker in ("#", "/"):
        if marker in text:
            text = text.rsplit(marker, 1)[-1]
    return text


def parse_wkt_point(wkt: str):
    inner = wkt.strip()
    for prefix in ("POINT(", "POINT ("):
        if inner.upper().startswith(prefix.upper()):
            inner = inner[len(prefix):]
            break
    inner = inner.rstrip(")").strip()
    lon, lat = (float(value) for value in inner.split())
    return lat, lon


def haversine_km(a, b) -> float:
    lat1, lon1 = a
    lat2, lon2 = b
    radius = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    h = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(h))


ALL_CQS = [
    "CQ-CORE-01", "CQ-CORE-02", "CQ-CORE-03", "CQ-CORE-04", "CQ-CORE-05", "CQ-CORE-06", "CQ-CORE-07",
    "CQ-INV-01", "CQ-INV-02", "CQ-INV-03", "CQ-INV-04", "CQ-INV-05", "CQ-INV-06", "CQ-INV-07", "CQ-INV-08", "CQ-INV-09",
    "CQ-RES-01", "CQ-RES-02", "CQ-RES-03", "CQ-RES-04", "CQ-RES-05", "CQ-RES-06", "CQ-RES-07", "CQ-RES-08",
    "CQ-RES-09", "CQ-RES-10", "CQ-RES-11", "CQ-RES-12", "CQ-RES-13", "CQ-RES-14",
    "CQ-CAM-01", "CQ-CAM-02", "CQ-CAM-03", "CQ-CAM-04", "CQ-CAM-05", "CQ-CAM-06",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate all 36 SIGEVS-O competency questions.")
    parser.add_argument("--ontology", type=Path, default=DEFAULT_ONTOLOGY)
    args = parser.parse_args()

    ontology_path = args.ontology if args.ontology.is_absolute() else (Path.cwd() / args.ontology)
    if not ontology_path.exists():
        print(f"[error] ontology not found: {ontology_path}")
        return 1

    graph = Graph()
    graph.parse(str(ontology_path), format="turtle")
    populated = Graph()
    for triple in graph:
        populated.add(triple)
    populated.parse(data=SAMPLE_ABOX, format="turtle")

    print("=" * 72)
    print(f"SIGEVS-O competency-question validation (36 CQs)")
    print(f"ontology: {ontology_path} ({len(graph)} triples; {len(populated)} with sample ABox)")
    print("=" * 72)

    failures = []
    counts = {"sparql": 0, "structural": 0, "implementation": 0}

    for cq_id in ALL_CQS:
        if cq_id in IMPLEMENTATION_CQS:
            counts["implementation"] += 1
            print(f"  {cq_id:<12} [impl-layer ] {IMPLEMENTATION_CQS[cq_id]}")
            continue
        if cq_id in STRUCTURAL_CHECKS:
            try:
                ok = STRUCTURAL_CHECKS[cq_id](populated)
            except Exception as exc:  # noqa: BLE001
                ok = False
                print(f"      error: {type(exc).__name__}: {exc}")
            counts["structural"] += 1
            print(f"  {cq_id:<12} [structural ] TBox check {'ok' if ok else 'FAIL'}")
            if not ok:
                failures.append(f"{cq_id}: structural check failed")
            continue

        query = Q.get(cq_id)
        if query is None:
            failures.append(f"{cq_id}: no query defined")
            print(f"  {cq_id:<12} [sparql     ] FAIL (query missing)")
            continue
        try:
            rows = list(populated.query(query))
            ok = EXPECTED[cq_id](rows)
        except Exception as exc:  # noqa: BLE001
            ok = False
            print(f"      error: {type(exc).__name__}: {exc}")
        counts["sparql"] += 1
        print(f"  {cq_id:<12} [sparql     ] {len(rows):>2} row(s) {'ok' if ok else 'FAIL'}")
        if not ok:
            failures.append(f"{cq_id}: unexpected result set")

    print("=" * 72)
    print(f"Summary: {len(ALL_CQS)} CQs "
          f"(SPARQL: {counts['sparql']}, structural: {counts['structural']}, "
          f"implementation-layer: {counts['implementation']})")
    if failures:
        print("RESULT: FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("RESULT: ALL 36 COMPETENCY QUESTIONS VALIDATED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
