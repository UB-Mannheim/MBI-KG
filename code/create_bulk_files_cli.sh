docker-compose exec -it mbi_wikibase_1 bash
php ./extensions/Wikibase/repo/maintenance/dumpJson.php --entity-type='item' --entity-type='property' --output=./MBI_KG_bulk_cli_v1.0.json
php ./extensions/Wikibase/repo/maintenance/dumpRdf.php --format=ttl --entity-type='item' --entity-type='property' --output=./MBI_KG_bulk_cli_v1.0.ttl
exit
docker cp mbi_wikibase_1:/var/www/html/MBI_KG_bulk_cli_v1.0.json ./MBI_KG_bulk_cli_v1.0.json
docker cp mbi_wikibase_1:/var/www/html/MBI_KG_bulk_cli_v1.0.ttl ./MBI_KG_bulk_cli_v1.0.ttl
