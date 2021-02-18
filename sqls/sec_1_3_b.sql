select constituent , data_value , data_time from MIS_WAREHOUSE.SO_FAR_HIGHEST_MONTHLY
where metric_name = 'Requirement (MW) ' AND 
report_month = 'month_name' 
GROUP BY constituent