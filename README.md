# 📊 Analytics Engineering: Análise de Inadimplência e Gestão de Contas a Receber

Este projeto implementa uma pipeline end-to-end de **Analytics Engineering** para análise de risco financeiro, focada em métricas de **Contas a Receber, Inadimplência e Aging List (Faixas de Atraso)**. 

A solução transforma dados brutos de faturas e pagamentos numa estrutura dimensional pronta para consumo executivo via **Power BI**, utilizando boas práticas de modelagem modular (Medallion Architecture) com **dbt** e **DuckDB**.

---

## 🎯 Problema de Negócio

Acompanhar a inadimplência e o fluxo de caixa é crítico para a saúde financeira de qualquer empresa. Este projeto visa responder às seguintes questões estratégicas:
- Qual o volume financeiro total retido em faturas vencidas?
- Como o risco de inadimplência está distribuído nas faixas de atraso (*Aging Buckets*: 1-30 dias, 31-60 dias, 61-90 dias e >90 dias)?
- Quais segmentos de clientes concentram a maior taxa de inadimplência?
- Qual a média de dias de atraso nas cobranças?

---

## 🏗️ Arquitetura e Fluxo de Dados

O projeto segue a arquitetura de modelagem em camadas (**Staging ➔ Intermediate ➔ Marts**):

1. **Camada Staging (`staging/`)**: Limpeza inicial, padronização de tipos de dados, nomes de colunas e casting de campos vindos das fontes puras (*raw*).
2. **Camada Intermediate (`intermediate/`)**: Aplicação de regras de negócio, cálculo de status das faturas (`Em Aberto`, `Pago em Dia`, `Inadimplente (Vencido)`, etc.), juros/multas e cálculo automático dos dias de atraso.
3. **Camada Marts (`marts/`)**: Construção da tabela fato final (`fct_contas_receber`) agregando informações de clientes e criando a segmentação por **Aging Buckets** para análise de risco.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Python**: Geração de massa de dados sintéticos realistas de faturas, clientes e pagamentos.
* **DuckDB**: Banco de dados analítico (OLAP) de alto desempenho e armazenamento local.
* **dbt (data build tool)**: Transformação de dados, controle de versão dos modelos SQL, lineage e testes de dados.
* **Power BI**: Construção de dashboard interativo focado em KPIs financeiros e análise de risco.
* **Git & GitHub**: Versionamento de código e documentação técnica.

---

## 📐 Métricas e KPIs Construídos (DAX / SQL)

- **Total Faturado**: Volume total financeiro em faturas emitidas.
- **Total Inadimplente**: Soma do valor de faturas vencidas e não pagas.
- **Taxa de Inadimplência (%)**: `Total Inadimplente / Total Faturado`.
- **Aging List (Faixas de Atraso)**: Classificação categórica para análise da qualidade da carteira de crédito (`1–30 dias`, `31–60 dias`, `61–90 dias`, `>90 dias (Crítico)`).
- **Média de Dias de Atraso**: Indicador de eficiência operacional de cobrança.
