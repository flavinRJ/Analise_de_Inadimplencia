with source as (
    select * from {{ source('dbt_financeiro', 'raw_clientes') }}
)

select
    cliente_id,
    nome_empresa,
    segmento,
    limite_credito,
    CAST(data_cadastro as DATE) as data_cadastro
from source