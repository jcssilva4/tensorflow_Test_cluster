O primeiro passo é acessar a VPN do CIN. Mesmo fazendo a conexão utilizando a rede interna do CIn, é necessário usar a VPN do CIn. Para maiores informações sobre o uso 
da VPN do CIn, consultar a documentação disponível na página do HelpDesk para VPN do CIn (https://helpdesk.cin.ufpe.br/redes/vpn). O canal para tirar dúvidas sobre 
conexão com a VPN é através do HelpDesk (helpdesk@cin.ufpe.br). Após se conectar no nó de login (slurm-client1), pode-se executar comandos do slurm:
- sinfo # verificar status dos nós
- squeue # verificar fila de jobs
- srun hostname # envia um job que executa o comando 'hostname' em um nó do cluster
