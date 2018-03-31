debug:
	FLASK_DEBUG=1 python simple_vbb.py

deploy:
	python /home/knub/Repositories/simple-vbb/simple_vbb.py > /home/knub/Repositories/simple-vbb/log.txt 2>&1 > /home/knub/Repositories/simple-vbb/log.txt &

run:
	python simple_vbb.py
