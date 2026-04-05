init_user_pool:
	python -m app.scripts.initialize_user_pool --email ${ADMIN_EMAIL} --password ${ADMIN_PASSWORD}
.PHONY: init_user_pool

STAGE?=local
create_tables:
	python -m app.scripts.create_tables --stage ${STAGE}
.PHONY: create_tables

purge_tables:
	python -m app.scripts.purge_tables
.PHONY: purge_tables

purge_user_pools:
	python -m app.scripts.purge_user_pools
.PHONY: purge_user_pools