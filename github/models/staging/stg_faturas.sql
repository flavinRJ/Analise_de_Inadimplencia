with source as (
    select * from {{ source('dbt_financeiro', 'raw_faturas') }}
),

renamed as (
    select
        fatura_id,
        cliente_id,
        CAST(data_emissao as DATE) as data_emissao,
        CAST(data_vencimento as DATE) as data_vencimento,
        valor_fatura
    from source
)

select * from renamed