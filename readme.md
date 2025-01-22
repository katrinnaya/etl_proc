   
Запуск контейнера

'''
docker run --name nifi \
  -p 8443:8443 \
  -v ~/etl_proc/hw_2:/opt/nifi/nifi-current/data \
  -d \
  -e SINGLE_USER_CREDENTIALS_USERNAME=admin \
  -e SINGLE_USER_CREDENTIALS_PASSWORD=ctsBtRBKHRAx69EqUghvvgEvjnaLjFEB \
  apache/nifi:latest
'''
