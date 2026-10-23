with faturas as (
    select * from {{ ref('stg_faturas') }}
),

pagamentos as (
    select * from {{ ref('stg_pagamentos') }}
),

clientes as (
    select * from {{ ref('stg_clientes') }}
),

calculo_atraso as (
    select
        f.fatura_id,
        f.cliente_id,
        c.nome_empresa,
        c.segmento,
        f.data_emissao,
        f.data_vencimento,
        f.valor_fatura,
        p.data_pagamento,
        p.valor_pago,
        p.juros_multa,
        
        -- Calcula dias de atraso se pago ou em relação à data limite se em aberto
        CASE 
            WHEN p.data_pagamento is not null then CAST(p.data_pagamento - f.data_vencimento AS INTEGER)
            ELSE CAST('2026-10-01'::DATE - f.data_vencimento AS INTEGER)
        END as dias_atraso_ou_aberto

    from faturas f
    left join pagamentos p on f.fatura_id = p.fatura_id
    left join clientes c on f.cliente_id = c.cliente_id
),

classificacao as (
    select
        *,
        CASE
            WHEN data_pagamento is not null and dias_atraso_ou_aberto <= 0 then 'Pago em Dia'
            WHEN data_pagamento is not null and dias_atraso_ou_aberto > 0 then 'Pago com Atraso'
            WHEN data_pagamento is null and dias_atraso_ou_aberto <= 0 then 'Em Aberto (A Vencer)'
            WHEN data_pagamento is null and dias_atraso_ou_aberto > 0 then 'Inadimplente (Vencido)'
        end as status_fatura
    from calculo_atraso
)

select * from classificacao