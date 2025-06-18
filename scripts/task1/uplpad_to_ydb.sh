ydb \
--endpoint grpcs://ydb.serverless.yandexcloud.net:2135 \
--database /ru-central1/b1g9tm1cvjc9r6hl0g83/etn4ciikjn2811hfpjo9 \
--sa-key-file authorized_key.json \
import file csv \
--path transactions_v2 \
--input-format csv \
--format-version full \
--delimiter "," \
--skip-rows 1 \
--null-value "" \
--verbose \
transactions_v2.csv
