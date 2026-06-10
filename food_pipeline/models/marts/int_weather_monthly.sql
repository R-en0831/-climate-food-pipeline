-- 日次の気象を月次に集計する中間モデル
select
    strftime(weather_date, '%Y-%m')   as price_month,   -- 日付を '2024-01' 形式の文字列に
    avg(temp_mean_c)                  as avg_temp_c,     -- その月の平均気温
    sum(precipitation_mm)             as total_precip_mm -- その月の合計降水量
from {{ ref('stg_weather') }}
group by strftime(weather_date, '%Y-%m')
