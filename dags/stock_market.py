from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.sensors.base import PokeReturnValue
from airflow.operators.python import PythonOperator
from include.stock_market.tasks import _get_stock_prices, _store_prices
from datetime import datetime

SYMBOL = 'NVDA'

@dag(
    start_date=datetime(2023, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['stock_market']
)

def stock_market():

    @task.sensor(poke_interval=30, #every 30sec sensor will check if api is available
                 timeout=300, mode='poke')
    
    def is_api_available() -> PokeReturnValue:
        import requests

        api = BaseHook.get_connection('stock_api')
        url = f"{api.host}{api.extra_dejson['endpoint']}"
        print(url)
        response = requests.get(url, headers=api.extra_dejson['headers'])
        condition = response.json()['finance']['result'] is None
        return PokeReturnValue(is_done=condition, xcom_value=url)
    
    get_stock_prices = PythonOperator(
        task_id='get_stock_prices',
        python_callable=_get_stock_prices,
        op_kwargs={'url': '{{ ti.xcom_pull(task_ids="is_api_available") }}', 'symbol': SYMBOL}
    )

    store_prices = PythonOperator(
        task_id='store_prices',
        python_callable=_store_prices,
        op_kwargs={'stock': '{{ ti.xcom_pull(task_ids="get_stock_prices") }}'}
    )

    is_api_available() >> get_stock_prices >> store_prices


stock_market()

#step 1: lets check if yahoo finance api is available using sensor
#step 2: fetch stock prices
#step 3: store prices in minio (is like AWS S3)