convert:
	find . -maxdepth 1 -type d | tail -n +2 | { while read folder; do ls -1 $$folder/.oq/ | { while read line; do convert $$folder/.oq/$$line -geometry 300x300 -quality 30 $$folder/$$line; done }; done }
