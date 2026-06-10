-- 月次の気象と食料価格を結合した分析用マート
select
    fp.price_month,
    fp.food_price_index,
    fp.cereals,
    fp.meat,
    fp.dairy,
    w.avg_temp_c,
    w.total_precip_mm
from {{ ref('stg_food_prices') }}     as fp
left join {{ ref('int_weather_monthly') }} as w
    on fp.price_month = w.price_month
order by fp.price_month
