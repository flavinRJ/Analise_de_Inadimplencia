with int_faturas as (
    select * from {{ ref('int_faturas_status') }}
),

aging_buckets as (
    select
        fatura_id,
        cliente_id,
        nome_empresa,
        segmento,
        data_emissao,
        data_vencimento,
        valor_fatura,
        data_pagamento,
        valor_pago,
        juros_multa,
        dias_atraso_ou_aberto,
        status_fatura,

        -- Criação das faixas de atraso (Aging Buckets) para análise de risco
        case
            when status_fatura = 'Inadimplente (Vencido)' and dias_atraso_ou_aberto between 1 and 30 then '1. De 1 a 30 dias'
            when status_fatura = 'Inadimplente (Vencido)' and dias_atraso_ou_aberto between 31 and 60 then '2. De 31 a 60 dias'
            when status_fatura = 'Inadimplente (Vencido)' and dias_atraso_ou_aberto between 61 and 90 then '3. De 61 a 90 dias'
            when status_fatura = 'Inadimplente (Vencido)' and dias_atraso_ou_aberto > 90 then '4. Acima de 90 dias (Crítico)'
            else 'Em Dia / A Vencer'
        end as faixa_aging

    from int_faturas
)

select * from aging_buckets