select entity_tag, sum(data_value) as metric_value from mis_warehouse.state_files_daily_data where metric_name = 'Consumption(MU)'
and time_stamp between '01-12-2020' and '31-12-2020' GROUP BY entity_tag