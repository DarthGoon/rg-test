run:
	@docker-compose up
test:
	@docker-compose --file docker-compose.test.yml run sut
