-- raw_food_prices を整形した staging モデル
select
    month                     as price_month,
    food_price_index,
    meat,
    dairy,
    cereals,
    oils,
    sugar
from raw_food_prices
where month is not null
