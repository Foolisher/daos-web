# API

# 创建应用 app
	curl -X POST 'localhost:5000/api/app' --form app_name='eco'

# 查询应用
	curl  'localhost:8090/api/app' --cookie 'app_name=ecp;'

# 删除应用
	curl -X DELETE 'localhost:8090/api/app' --form app_name='端点电商'


# 用户登陆
	curl -X POST 'localhost:8090/api/login' --form name='admin' --form password='123456'


# 获取所有job
	curl --form app_name='ecp' 'localhost:8090/api/jobs'


# 新增job
	curl -X POST 'localhost:8090/api/job' \
		--form app_name='端点电商' \
		--form job_id='交易统计' \
		--form sql='select sum(fee) from ecp_order_items' \
		--form hour=1


# 删除 job
	curl -X DELETE 'localhost:8090/api/job' --form app_name='端点电商' --form job_id='交易统计'


# 执行 job
	curl -X POST 'localhost:8090/api/job/start' --form app_name='端点电商' --form job_id='交易统计'

# 停止 job
	curl -X POST 'localhost:8090/api/job/stop' --form app_name='端点电商' --form job_id='交易统计'

# 查询结果
	curl -X GET 'localhost:8090/api/job/result' --form app_name='端点电商' --form job_id='交易统计'


# 创建菜单
	curl -X POST 'localhost:8090/api/menu' \
		--form app_name='端点电商' \
		--form body='{"something": "nothing"}'

# 删除菜单
	curl -X DELETE 'localhost:8090/api/menu' --form app_name='端点电商'


# 查询所有菜单   /api/menus/full?app_name=  /api/menus/simple?app_name=
	curl -X GET 'localhost:8090/api/menus/full' --form app_name='端点电商'





## 实例   创建任务 ==> 执行任务 ==> 查看结果

	curl -X DELETE 'localhost:8090/api/job' --cookie 'app_name=ecp' --form job_id='前一小时交易订单量'

	curl -X POST 'localhost:8090/api/job' \
		--form job_id='前一小时交易订单量' \
		--cookie 'app_name=ecp' \
		--form sql='
		   select  count(DISTINCT(`order_id`)) order_count, hour(-1) order_key
		    from `ecp.ecp_order_items`
		    where hour(-1) = substr(created_at, 0,13)
		' \
		--form hour=1


	curl -X POST 'localhost:8090/api/job/start' --cookie 'app_name=ecp' --form job_id='前一小时交易订单量'


	curl -X GET 'localhost:8090/api/job/result' --cookie 'app_name=ecp' --form job_id='前一小时交易订单量'





