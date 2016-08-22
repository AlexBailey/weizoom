etcdctl set /service/weapp/service1 "127.0.0.1:8000"
etcdctl set /extra/weapp/location1 "location /static { root /home/weizoom/microservice/launcher/Weapp/weapp/; }"
etcdctl set /extra/weapp/location2 "location /custom_static { root /home/weizoom/microservice/launcher/Weapp/weapp/templates/custom/; }"
etcdctl set /extra/weapp/location3 "location /standard_static/ { alias /home/weizoom/microservice/launcher/Weapp/weapp/static/; }"
etcdctl set /extra/weapp/location4 "location /landing_static/ { alias /home/weizoom/microservice/launcher/Weapp/weapp/static/landing/; }"
etcdctl set /extra/weapp/location5 "location /termite_static/upload/ { alias /home/weizoom/microservice/launcher/Weapp/weapp/static/upload/; }"
etcdctl set /extra/weapp/location6 "location /termite_static/head_images/ { alias /home/weizoom/microservice/launcher/Weapp/weapp/static/head_images/; }"
etcdctl set /extra/weapp/location7 "location /termite_static/ { alias /home/weizoom/microservice/launcher/Weapp/weapp/termite/static/; }"
etcdctl set /extra/weapp/location8 "location /markettools_static/ { alias /home/weizoom/microservice/launcher/Weapp/weapp/market_tools/tools/; }"
etcdctl set /extra/weapp/location9 "location /webapp_static/ { alias /home/weizoom/microservice/launcher/Weapp/weapp/modules/static/; }"
etcdctl set /extra/weapp/location10 "location /workbench/ { rewrite ^(.*)$ /termite$1; }"