---
type: note
topic: data-platform
created: 2026-01-15
tags:
  - datahub
  - dremio
---

# DATAHUB / DREMIO

[https://docs.datahub.com/docs/generated/ingestion/sources/dremio](https://docs.datahub.com/docs/generated/ingestion/sources/dremio)

# PROFILING

[https://docs.datahub.com/docs/metadata-ingestion/docs/dev_guides/sql_profiles](https://docs.datahub.com/docs/metadata-ingestion/docs/dev_guides/sql_profiles)

*CAUTION
Running profiling against many tables or over many rows can run up significant costs. While we've done our best to limit the expensiveness of the queries the profiler runs, you should be prudent about the set of tables profiling is enabled on or the frequency of the profiling runs.*

*Extracts:*

- *Row and column counts for each table*
- *For each column, if applicable:*
    - null counts and proportions
    - distinct counts and proportions
    - minimum, maximum, mean, median, standard deviation, some quantile values
    - histograms or frequencies of unique values
- *Optional SQL Profiling (if enabled):*
    - Table, row, and column statistics can be profiled and ingested via optional SQL queries.
    - Extracts statistics about tables and columns, such as row counts and data distribution, for better insight into the dataset structure.

CONFIG

| ****profiling**ProfileConfig**                                             |                                                                                                                                                                               |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| *profiling.***enabled**boolean                                             | Whether profiling should be done. Default: False                                                                                                                              |
| *profiling.***include_field_distinct_count**boolean                        | Whether to profile for the number of distinct values for each column. Default: True                                                                                           |
| *profiling.***include_field_distinct_value_frequencies**boolean            | Whether to profile for distinct value frequencies. Default: False                                                                                                             |
| *profiling.***include_field_histogram**boolean                             | Whether to profile for the histogram for numeric fields. Default: False                                                                                                       |
| *profiling.***include_field_max_value**boolean                             | Whether to profile for the max value of numeric columns. Default: True                                                                                                        |
| *profiling.***include_field_mean_value**boolean                            | Whether to profile for the mean value of numeric columns. Default: True                                                                                                       |
| *profiling.***include_field_min_value**boolean                             | Whether to profile for the min value of numeric columns. Default: True                                                                                                        |
| *profiling.***include_field_null_count**boolean                            | Whether to profile for the number of nulls for each column. Default: True                                                                                                     |
| *profiling.***include_field_quantiles**boolean                             | Whether to profile for the quantiles of numeric columns. Default: False                                                                                                       |
| *profiling.***include_field_sample_values**boolean                         | Whether to profile for the sample values for all columns. Default: True                                                                                                       |
| *profiling.***include_field_stddev_value**boolean                          | Whether to profile for the standard deviation of numeric columns. Default: True                                                                                               |
| *profiling.***limit**One of integer, null                                  | Max number of documents to profile. By default, profiles all documents. Default: None                                                                                         |
| *profiling.***max_workers**integer                                         | Number of worker threads to use for profiling. Set to 1 to disable. Default: 20                                                                                               |
| *profiling.***offset**One of integer, null                                 | Offset in documents to profile. By default, uses no offset. Default: None                                                                                                     |
| *profiling.***profile_table_level_only**boolean                            | Whether to perform profiling at table-level only, or include column-level profiling as well. Default: False                                                                   |
| *profiling.***query_timeout**integer                                       | Time before cancelling Dremio profiling query Default: 300                                                                                                                    |
| *profiling.***operation_config**OperationConfig                            |                                                                                                                                                                               |
| *profiling.operation_config.***lower_freq_profile_enabled**boolean         | Whether to do profiling at lower freq or not. This does not do any scheduling just adds additional checks to when not to run profiling. Default: False                        |
| *profiling.operation_config.***profile_date_of_month**One of integer, null | Number between 1 to 31 for date of month (both inclusive). If not specified, defaults to Nothing and this field does not take affect. Default: None                           |
| *profiling.operation_config.***profile_day_of_week**One of integer, null   | Number between 0 to 6 for day of week (both inclusive). 0 is Monday and 6 is Sunday. If not specified, defaults to Nothing and this field does not take affect. Default: None |
