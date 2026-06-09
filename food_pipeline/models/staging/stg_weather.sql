-- raw_weather を整形した staging モデル
select
    cast(date as date)        as weather_date,
    temp_mean_c,
    precipitation_mm
from raw_weather
where date is not null
