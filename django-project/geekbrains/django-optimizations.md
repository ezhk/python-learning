
# Debug toolbar SQL optimizations
## Начальные значение
| URL | SQL queries | Duplicate Queries |
|-----|-------------|-------------------|
| /products/category/0 | 12 | 5 |
| /cart/ | 5 | 0 |
| /order/ | 6 | 0 |
| /order/read/2 | 7 | 0 |
| /order/update/2 | 28 | 22 |

## После оптимизации 
| URL | SQL queries | Duplicate Queries | Actions |
|-----|-------------|-------------------|---------|
| /products/category/0 | 8 | 0 | template: discount_products &#124; is_discount:product.pk -> product in discount_products |
| /order/update/2 | 12 | 5 | orderapp:forms -> get_initial_for_field, init self.products |
| /order/update/2 | 11 | 4 | calculate init summary cost and quantity in JS or OrderUpdate: set init summary values |

# Django extensions
$ pip install django-extensions  
$ ./manage.py show_urls

    /	mainapp.views.main	index
    /__debug__/render_panel/	debug_toolbar.views.render_panel	djdt:render_panel
    /__debug__/sql_explain/	debug_toolbar.panels.sql.views.sql_explain	djdt:sql_explain
    /__debug__/sql_profile/	debug_toolbar.panels.sql.views.sql_profile	djdt:sql_profile
    /__debug__/sql_select/	debug_toolbar.panels.sql.views.sql_select	djdt:sql_select
    /__debug__/template_source/	debug_toolbar.panels.templates.views.template_source	djdt:template_source
    /admin/	adminapp.views.IndexList	admin:index
    /admin/categories	adminapp.views.ProductCategoriesList	admin:categories
    /admin/categories/create	adminapp.views.ProductCategoryCreate	admin:category_create
    /admin/categories/delete/<int:pk>	adminapp.views.ProductCategoryDelete	admin:category_delete
    /admin/categories/update/<int:pk>	adminapp.views.ProductCategoryUpdate	admin:category_update
    /admin/order/update/<int:pk>	adminapp.views.OrderStatus	admin:order_update
    /admin/products	adminapp.views.ProductsList	admin:products
    /admin/products/create	adminapp.views.ProductCreate	admin:product_create
    /admin/products/delete/<int:pk>	adminapp.views.ProductDelete	admin:product_delete
    /admin/products/update/<int:pk>	adminapp.views.ProductUpdate	admin:product_update
    /admin/users	adminapp.views.UsersList	admin:users
    /admin/users/create	adminapp.views.UserCreate	admin:user_create
    /admin/users/delete/<int:pk>	adminapp.views.UserDelete	admin:user_delete
    /admin/users/update/<int:pk>	adminapp.views.UserUpdate	admin:user_update
    /auth/	authapp.views.login	auth:login
    /auth/create	authapp.views.CreateShopUser	auth:create
    /auth/edit	authapp.views.edit	auth:edit
    /auth/logout	authapp.views.logout	auth:logout
    /auth/verify/<str:email>/<slug:activation_key>	authapp.views.verify	auth:verify
    /cart/	cartapp.views.show	cart:index
    /cart/add/<int:pk>	cartapp.views.add	cart:add
    /cart/delete/<int:pk>	cartapp.views.delete	cart:delete
    /cart/update/<int:pk>/quantity/<int:value>	cartapp.views.update	cart:update
    /contacts/	mainapp.views.contacts	contacts
    /media\/<path>	django.views.static.serve	
    /order/	orderapp.views.OrderList	order:index
    /order/create	orderapp.views.OrderCreate	order:create
    /order/delete/<int:pk>	orderapp.views.OrderDelete	order:delete
    /order/read/<int:pk>	orderapp.views.OrderRead	order:read
    /order/update/<int:pk>	orderapp.views.OrderUpdate	order:update
    /order/update/<int:pk>/status/<slug:status>	orderapp.views.change_order_status	order:update_status
    /products/	mainapp.views.products	products:index
    /products/category/<int:pk>	mainapp.views.products	products:category
    /products/detail/<int:pk>	mainapp.views.products_details	products:detail
    /social/complete/<backend>/	social_django.views.complete	social:complete
    /social/disconnect/<backend>/	social_django.views.disconnect	social:disconnect
    /social/disconnect/<backend>/<association_id>/	social_django.views.disconnect	social:disconnect_individual
    /social/login/<backend>/	social_django.views.auth	social:begin

# Связи таблиц базы данных
$ sudo apt-get install python3-graphviz  
$ manage.py graph_models -a -g -o geekshop_visualized.png

Результат: screenshots/geekshop_visualized.png

# Siege
$ siege -f siege-urls.txt -d0 -r15 -c250

    ** SIEGE 4.0.4
    ** Preparing 250 concurrent users for battle.
    The server is now under siege...siege aborted due to excessive socket failure; you
    can change the failure threshold in $HOME/.siegerc
    
    Transactions:		        1832 hits
    Availability:		       62.59 %
    Elapsed time:		       30.36 secs
    Data transferred:	       17.42 MB
    Response time:		        2.05 secs
    Transaction rate:	       60.34 trans/sec
    Throughput:		        0.57 MB/sec
    Concurrency:		      123.60
    Successful transactions:        1834
    Failed transactions:	        1095
    Longest transaction:	       24.53
    Shortest transaction:	        0.00

$ sudo sysctl net.core.somaxconn=4096  
$ siege -f siege-urls.txt -d0 -r15 -c250

    Transactions:		       42355 hits
    Availability:		       99.66 %
    Elapsed time:		      209.17 secs
    Data transferred:	      486.08 MB
    Response time:		        1.14 secs
    Transaction rate:	      202.49 trans/sec
    Throughput:		        2.32 MB/sec
    Concurrency:		      230.72
    Successful transactions:       41855
    Failed transactions:	         145
    Longest transaction:	       38.35
    Shortest transaction:	        0.00

## Статистика по URL
| URL                           | Transactions  | Elapsed time  | Concurrency   | Transaction rate | Response time  |
|-------------------------------|---------------|---------------|---------------|------------------|----------------|
| /                             | 48050         | 128.74 secs   | 214.88        | 373.23 trans/sec | 0.58 secs      |
| /admin/                       | 47890         | 159.14 secs   | 231.24        | 300.93 trans/sec | 0.77 secs      |
| /admin/products               | 48638         | 128.23 secs   | 219.64        | 379.30 trans/sec | 0.58 secs      |
| /admin/users                  | 48750         | 115.44 secs   | 213.91        | 422.30 trans/sec | 0.51 secs      |
| /auth/edit                    | 48566         | 153.09 secs   | 238.87        | 317.24 trans/sec | 0.75 secs      |
| /cart/                        | 55471         | 160.23 secs   | 208.61        | 346.20 trans/sec | 0.60 secs      |
| /cart/update/1/quantity/10    | 3750          | 54.64 secs    | 241.54        | 68.63 trans/sec  | 3.52 secs      |
| /contacts/                    | 44159         | 135.84 secs   | 231.64        | 325.08 trans/sec | 0.71 secs      |
| /order/                       | 48750         | 129.04 secs   | 221.40        | 377.79 trans/sec | 0.59 secs      |
| /order/update/1               | 59896         | 221.22 secs   | 231.26        | 270.75 trans/sec | 0.85 secs      |
| /order/update/2               | 59728         | 240.18 secs   | 237.99        | 248.68 trans/sec | 0.96 secs      |
| /order/read/1                 | 51622         | 142.82 secs   | 222.30        | 361.45 trans/sec | 0.62 secs      |
| /products/                    | 52264         | 143.03 secs   | 225.20        | 365.41 trans/sec | 0.62 secs      |
| /products/category/1          | 56250         | 143.31 secs   | 219.49        | 392.51 trans/sec | 0.56 secs      |
| /products/detail/1            | 51492         | 141.85 secs   | 213.58        | 363.00 trans/sec | 0.59 secs      |
| /products/detail/2            | 49394         | 142.27 secs   | 216.70        | 347.18 trans/sec | 0.62 secs      |

/order/update/2 — наиболее медленный URL,  
    только, на самом деле, это не очень правильная метрика, точнее она считается от затраченного  
    вренени на количество запросов, а поскольку мы ещё загружаем статику, то создается ощущение,  
    что это URL работает быстрее /cart/update/1/quantity/10 — что ошибочно.

## Производительность оптимизаций
Переключась между бранчами 2.5 и 2.6 может замерить profit от оптимизаций.

| Branch                        | URL                           | Transactions  | Elapsed time  | Concurrency   | Transaction rate | Response time  |
|-------------------------------|-------------------------------|---------------|---------------|---------------|------------------|----------------|
| django-2.5 — до оптимизации   | /order/update/2               | 59992         | 313.55 secs   | 241.36        | 191.33 trans/sec | 1.26 secs      |
| django-2.6 — после оптимизации| /order/update/2               | 60000         | 213.63 secs   | 238.43        | 280.86 trans/sec | 0.85 secs      |

Также по результатам стрельб видно, что при текущих настройках может обслужить порядка 200 клиентов.