NAME_CONTAINER += 'video_stream_processig'

DC += docker-compose -f
DC_NAME += 'docker-compose.yml'

all:
	$(DC) $(DC_NAME) up --build
