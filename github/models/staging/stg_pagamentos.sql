with source as (
    select * from {{ source('dbt_financeiro', 'raw_pagamentos') }}
),

renamed as (
    select
        pagamento_id,
        fatura_id,
        CAST(data_pagamento as DATE) as data_pagamento,
        valor_pago,
        juros_multa
    from source
)

select * from renamed