# Преобразование данных в датасете
* вычисление 5 самых жарких и самых холодных дней;
*	фильтрация out/in = in;
*	перевед поле noted_date в формат ‘yyyy-MM-dd’ с типом данных date;

## 1. Запуск контейнера

```
docker run --name nifi \
  -p 8443:8443 \
  -v ~/etl_proc/hw_3:/opt/nifi/nifi-current/data \
  -d \
  -e SINGLE_USER_CREDENTIALS_USERNAME=admin \
  -e SINGLE_USER_CREDENTIALS_PASSWORD=ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB \
  apache/nifi:latest
```
## 2. Работа с NIFI
UI: https://localhost:8443
