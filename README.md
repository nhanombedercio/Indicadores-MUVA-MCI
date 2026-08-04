# MCI Indicadores — Sistema de Gestão de Indicadores MUVA

Sistema web para gestão de indicadores MCI com dois perfis: painel da equipa técnica e página de revisão para director.

## Stack Tecnológico

- **Backend:** Flask (Python)
- **Base de dados:** SQLite via SQLAlchemy
- **Frontend:** HTML + Bootstrap 5 + Chart.js
- **Export:** openpyxl (Excel)

## Estrutura

```
mci_indicadores/
├── app.py                 # Aplicação Flask
├── models.py              # Modelos SQLAlchemy
├── data.py                # Dicionário de indicadores
├── routes/
│   ├── revisao.py         # Rotas de revisão do director
│   └── gestao.py          # Rotas do painel da equipa
├── templates/
│   ├── base.html
│   ├── revisao/           # Templates de revisão
│   └── gestao/            # Templates do painel
├── static/
│   └── style.css
├── requirements.txt
├── .env
└── README.md
```

## Desenvolvimento Local

### 1. Instalar dependências

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Crie um ficheiro `.env` (copie `.env` existente):

```env
FLASK_DEBUG=true
SECRET_KEY=chave-secreta-para-desenvolvimento
GESTAO_PASSWORD=muva2026
DATABASE_URL=sqlite:///mci_indicadores.db
```

### 3. Inicializar base de dados

```bash
python init_db.py
```

### 4. Executar em desenvolvimento

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`.

## Produção — Digital Ocean

### Pré-requisitos

- Droplet Digital Ocean Ubuntu 24.04 LTS (1GB RAM suficiente)
- Acesso SSH ao servidor
- Domínio apontado para o servidor

### 1. Setup Inicial do Servidor

```bash
# Como root
ssh root@IP_DO_SERVIDOR

apt update && apt upgrade -y
apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx git ufw

# Criar utilizador de aplicação
adduser muva
usermod -aG sudo muva
rsync --archive --chown=muva:muva ~/.ssh /home/muva

# Firewall
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
```

### 2. Clonar e Instalar

```bash
# Como utilizador muva
su - muva

mkdir -p /var/www/mci_indicadores
cd /var/www/mci_indicadores

# Clonar repositório
git clone https://github.com/seu-user/Indicadores-MUVA-MCI.git .

# Ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Produção

```bash
# Gerar SECRET_KEY segura
python -c "import secrets; print(secrets.token_hex(32))"

# Copiar exemplo e editar
cp .env.production.example .env

# Editar .env com valores reais
nano .env
```

Conteúdo recomendado para `.env`:

```env
SECRET_KEY=<SAÍDA_DO_COMANDO_ACIMA>
GESTAO_PASSWORD=USAR-PASSWORD-FORTE
DATABASE_URL=sqlite:////var/www/mci_indicadores/instance/mci_indicadores.db
FLASK_DEBUG=false
```

### 4. Criar Base de Dados

```bash
mkdir -p /var/www/mci_indicadores/instance
source venv/bin/activate
python init_db.py
```

### 5. Configurar Gunicorn como Serviço

```bash
# Como root
sudo nano /etc/systemd/system/mci_indicadores.service
```

Conteúdo:

```ini
[Unit]
Description=Gunicorn — MCI Indicadores MUVA
After=network.target

[Service]
User=muva
Group=www-data
WorkingDirectory=/var/www/mci_indicadores
Environment="PATH=/var/www/mci_indicadores/venv/bin"
EnvironmentFile=/var/www/mci_indicadores/.env
ExecStart=/var/www/mci_indicadores/venv/bin/gunicorn \
    --workers 2 \
    --bind unix:/run/mci_indicadores.sock \
    --access-logfile /var/log/mci_indicadores_access.log \
    --error-logfile /var/log/mci_indicadores_error.log \
    wsgi:app

Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mci_indicadores
sudo systemctl start mci_indicadores
sudo systemctl status mci_indicadores
```

### 6. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/mci_indicadores
```

Conteúdo:

```nginx
server {
    listen 80;
    server_name mci.seu-dominio.mz;

    location /static/ {
        alias /var/www/mci_indicadores/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/mci_indicadores.sock;
        proxy_read_timeout 120s;
        client_max_body_size 5M;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/mci_indicadores /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 7. HTTPS com Let's Encrypt

```bash
sudo certbot --nginx -d mci.seu-dominio.mz
sudo certbot renew --dry-run
```

### Manutenção

```bash
# Ver logs
sudo journalctl -u mci_indicadores -f

# Reiniciar após atualizar código
cd /var/www/mci_indicadores
git pull
sudo systemctl restart mci_indicadores

# Backup da base de dados
cp /var/www/mci_indicadores/instance/mci_indicadores.db \
   /home/muva/backups/mci_$(date +%Y%m%d).db
```

## Acesso

- **Painel da Equipa:** `http://localhost:5000/gestao` (password: muva2026)
- **Dashboard:** `http://localhost:5000/gestao/dashboard`
- **Revisão do Director:** Link único gerado pelo sistema e enviado ao director

## Fluxo de Trabalho

1. **Equipa** cria um novo ciclo de revisão no painel
2. **Equipa** preenche os dados de cada indicador (resultado, projectos, notas)
3. **Sistema** gera um link único de revisão
4. **Equipa** copia e envia o link ao director
5. **Director** abre o link, revê os dados, confirma ou edita
6. **Director** submete a revisão
7. **Sistema** guarda as alterações e marca o ciclo como revisto
8. **Equipa** visualiza a revisão no detalhe do ciclo, exporta para Excel ou consulta o dashboard

## Funcionalidades Principais

### Painel da Equipa (`/gestao`)

- ✅ Login com password
- ✅ Criar novos ciclos de revisão
- ✅ Preencher dados de indicadores
- ✅ Editar dados antes de enviar ao director
- ✅ Gerar link único de revisão
- ✅ Ver detalhe do ciclo com comparação lado-a-lado (antes vs. depois)
- ✅ Exportar ciclo individual para Excel
- ✅ Exportar todos os ciclos para Excel (consolidado)
- ✅ Dashboard com gráficos e métricas

### Página de Revisão do Director

- ✅ Acesso público via link único (token)
- ✅ Visualização de todos os dados preenchidos pela equipa
- ✅ Modo leitura por defeito
- ✅ Edição inline de campos específicos (nome, meta, notas)
- ✅ Proposta de eliminação com justificação obrigatória
- ✅ Confirmação de indicadores
- ✅ Inserção de nome e observações gerais
- ✅ Progresso visual de confirmação
- ✅ Validação completa antes de submissão
- ✅ Página de confirmação após submissão

### Dashboard

- ✅ Resumo de ciclos (total, revistos, pendentes)
- ✅ Resumo de indicadores (confirmados, editados, eliminação)
- ✅ Gráficos (tipo de indicador, confirmação por grupo)
- ✅ Tabelas de propostas de eliminação
- ✅ Tabelas de edições do director
- ✅ Tabelas de resultados registados

## Exportação Excel

### Um Ciclo
- Folha "Resumo" com metadados do ciclo
- Folha "Indicadores" com tabela completa (código, nome, meta, resultado, notas, decisões)
- Formatação com cores: verde para confirmados, amarelo para editados, vermelho para eliminação

### Todos os Ciclos
- Uma folha por ciclo
- Folha "Consolidado" com todos os indicadores empilhados
- Mesma formatação de cores

## Configuração de Produção

Para deploy em Digital Ocean (ou outro servidor):

1. Clonar o repositório no servidor
2. Criar ambiente virtual Python
3. Instalar dependências: `pip install -r requirements.txt`
4. Configurar variáveis em `.env`
5. Usar Gunicorn como servidor WSGI
6. Configurar Nginx como proxy reverso
7. Configurar HTTPS com Let's Encrypt

Ver secção "Deploy — Digital Ocean" na especificação técnica para instruções detalhadas.

## Notas Importantes

- **Base de dados:** SQLite local (ficheiro `mci_indicadores.db`). Para produção, considere fazer backups regulares.
- **Autenticação:** Password simples no painel da equipa. Para produção, considere implementar autenticação multi-utilizador.
- **Sessões:** Flask usa cookies de sessão (SECRET_KEY no .env).
- **Links de revisão:** Tokens UUID gerados automaticamente — únicos e intransferível.

## Licença

© 2026 MUVA / MCI — Sistema de Gestão de Indicadores
