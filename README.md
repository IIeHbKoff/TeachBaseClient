# Teachbase Client

## Running pipeline
1) Create *.env* file with environment variables.
2) Run *docker-compose build*
3) Run *docker-compose up*. You can add *-d* flag for run and detach from commandline interface

## Environment variables
- SECRET_KEY - your django secret key    
- CLIENT_ID - client token    
- CLIENT_SECRET - client secret    
- REDIS_HOST - redis ip addr or dnsname. By default - redis (resolved by docker dns)    
- REDIS_PORT - redis port. By default - 6379    
- REDIS_USERNAME - redis user. By default - None    
- REDIS_PASSWORD - redis password. By default - None     
- POSTGRES_HOST - postgresql ip addr or dnsname. By default - database (resolved by docker dns)    
- POSTGRES_PORT - postgresql port. By default - 5432    
- POSTGRES_DB - postgresql database name. By default - postgres    
- POSTGRES_USER - postgresql user. By default postgres    
- POSTGRES_PASSWORD - postgresql user password. By default - None    
- PGDATA - postgresql pass to database in a filesystem. By default /var/lib/postgresql/data/pgdata    
