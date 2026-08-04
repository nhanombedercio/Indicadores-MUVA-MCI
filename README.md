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

## Início Rápido

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Edite `.env` com a sua configuração (SECRET_KEY, GESTAO_PASSWORD, DATABASE_URL).

### 3. Executar a aplicação

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`.

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
