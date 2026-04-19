# AGENTS.md

Este arquivo orienta agentes de código que forem trabalhar neste repositório.

## Objetivo do projeto

O projeto implementa um marketplace sustentável chamado `Cashback Verde`, desenvolvido em Django, com foco em:

- cadastro/autenticação de usuários
- diferenciação entre compradores e vendedores
- catálogo de produtos
- pedidos
- cashback verde

## Estrutura real do repositório

O código principal não está na raiz. O app Django fica em `cashback_verde/`.

Principais áreas:

- `cashback_verde/manage.py`: ponto de entrada dos comandos Django
- `cashback_verde/cashback_verde/`: configuração do projeto (`settings.py`, `urls.py`)
- `cashback_verde/accounts/`: usuário customizado, cadastro e login
- `cashback_verde/products/`: catálogo e detalhe de produtos
- `cashback_verde/orders/`: modelos de pedido
- `cashback_verde/cashback/`: modelo e serviço de cashback
- `cashback_verde/core/`: home e rotas centrais
- `cashback_verde/templates/`: templates compartilhados e de páginas
- `cashback_verde/media/`: uploads locais

## Stack e dependências

- Python
- Django `5.2.13`
- PostgreSQL via `psycopg2-binary`
- `python-decouple` para variáveis de ambiente
- Pillow para imagens
- Bootstrap via CDN nos templates

Dependências declaradas em `cashback_verde/requirements.txt`.

## Como rodar localmente

Assuma que o diretório de trabalho operacional é `cashback_verde/`.

Comandos comuns:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Teste básico:

```bash
python manage.py test
python manage.py check
```

## Variáveis de ambiente esperadas

O projeto usa `python-decouple` e espera valores como:

- `SECRET_KEY`
- `DEBUG`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

Existe um arquivo `cashback_verde/.env` no workspace, mas agentes não devem copiar segredos para respostas nem reescrevê-los sem necessidade explícita.

## Observações importantes antes de editar

### 1. Há trabalho local em andamento

O worktree já possui alterações não commitadas e arquivos novos. Antes de editar, rode `git status --short` e preserve qualquer mudança existente que não faça parte da sua tarefa.

### 2. O settings atual tem efeito colateral no import

`cashback_verde/cashback_verde/settings.py` faz `print(config('DB_NAME'))` durante o import. Isso significa que comandos Django podem vazar esse valor no terminal. Se sua tarefa tocar configuração, trate isso como débito técnico relevante.

### 3. Banco configurado para PostgreSQL

Embora exista `cashback_verde/db.sqlite3`, o `settings.py` atual usa PostgreSQL, não SQLite. Não assuma que o SQLite é o banco ativo.

### 4. Testes ainda são mínimos

Os arquivos `tests.py` dos apps estão praticamente vazios. Ao implementar funcionalidade nova, prefira adicionar testes do comportamento alterado em vez de confiar apenas em inspeção manual.

## Convenções de código observadas

- idioma misto: nomes de apps e código em inglês, textos de interface em português
- views baseadas em função
- templates renderizados no servidor
- usuário customizado em `accounts.User`
- papel do usuário controlado por `role` com valores `buyer` e `seller`

Ao contribuir:

- mantenha consistência com o padrão Django já usado
- preserve nomes de rotas existentes
- evite introduzir camadas desnecessárias para mudanças simples
- centralize regras de domínio reutilizáveis em serviços quando fizer sentido, como já ocorre em `cashback/services.py`

## Fluxo recomendado para agentes

1. Ler `git status --short` para detectar mudanças locais.
2. Entrar em `cashback_verde/`.
3. Ler os arquivos diretamente relacionados à tarefa antes de propor mudanças.
4. Verificar impacto em templates, urls, models, views e migrations.
5. Se alterar models, criar/ajustar migrations.
6. Rodar a menor validação útil possível (`check`, testes do app afetado, ou `test` completo).
7. Informar com clareza o que foi alterado e o que não pôde ser validado.

## Áreas com maior chance de impacto cruzado

- alterações em `accounts.User` afetam autenticação, permissões e relações com `Product`, `Order` e `Cashback`
- alterações em `products.models.Product` afetam listagem, detalhe, admin e possíveis pedidos
- mudanças em `cashback/services.py` afetam saldo do usuário e geração de registros financeiros
- mudanças em `cashback_verde/urls.py` e `templates/base.html` afetam navegação global

## Checklist para tarefas comuns

### Nova funcionalidade em produto

- ajustar model/view/template/url conforme necessário
- validar acesso de vendedor vs comprador
- verificar upload de imagem se houver alteração no campo `image`

### Autenticação e cadastro

- revisar `accounts/forms.py`, `accounts/views.py`, `accounts/urls.py`
- garantir integração com `django.contrib.auth.urls`
- validar redirecionamentos após login/cadastro

### Cashback e pedidos

- revisar tipos numéricos e consistência de saldo
- evitar lógica financeira duplicada em views
- considerar atomicidade se a tarefa envolver gravações múltiplas

## O que evitar

- não sobrescrever mudanças locais do usuário
- não assumir que README documenta o projeto; o `README.md` atual praticamente não contém conteúdo
- não assumir cobertura de testes existente
- não expor valores de `.env` em logs, commits ou respostas
- não trocar para SQLite sem solicitação explícita

## Estado atual verificado nesta análise

- a estrutura Django está presente e coerente
- `python manage.py check` não pôde ser executado no ambiente atual porque o Python ativo não possui Django instalado
- há arquivos e edições locais ainda não commitados

## Saída esperada de futuros agentes

Ao finalizar uma tarefa neste projeto:

- descreva o que mudou
- cite arquivos principais afetados
- informe como validou
- deixe explícito qualquer bloqueio de ambiente, banco ou dependência
