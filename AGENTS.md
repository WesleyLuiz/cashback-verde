# AGENTS.md

Guia para agentes de codigo que forem trabalhar neste repositorio.

## Objetivo do projeto

`Cashback Verde` e um marketplace sustentavel desenvolvido em Django para um projeto de TCC. O sistema diferencia compradores e vendedores, permite cadastro e gerenciamento de anuncios, compra por carrinho e geracao/uso de cashback verde.

## Estrutura do repositorio

O projeto Django fica dentro de `cashback_verde/`; a raiz contem arquivos de apoio como `BACKLOG.md` e este guia.

Principais caminhos:

- `cashback_verde/manage.py`: ponto de entrada dos comandos Django.
- `cashback_verde/cashback_verde/`: configuracao do projeto (`settings.py`, `urls.py`, ASGI/WSGI e static local).
- `cashback_verde/accounts/`: usuario customizado, cadastro, login customizado e perfil.
- `cashback_verde/products/`: anuncios de produtos/servicos, filtros, CRUD de vendedor e formulario.
- `cashback_verde/orders/`: carrinho em sessao, checkout, pedidos e itens de pedido.
- `cashback_verde/cashback/`: registro e servico de credito de cashback.
- `cashback_verde/core/`: home e rotas centrais.
- `cashback_verde/templates/`: templates globais e paginas renderizadas no servidor.
- `cashback_verde/media/`: uploads locais de imagens.

## Stack

- Python
- Django `5.2.13`
- PostgreSQL via `psycopg2-binary`
- `python-decouple` para variaveis de ambiente
- Pillow para upload/processamento basico de imagens
- Bootstrap `5.3.3` via CDN nos templates

Dependencias declaradas em `cashback_verde/requirements.txt`.

## Como rodar

Use `cashback_verde/` como diretorio operacional para comandos Django.

```bash
cd cashback_verde
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Validacoes comuns:

```bash
python manage.py check
python manage.py test
```

## Variaveis de ambiente

O projeto usa `python-decouple` e espera, no minimo:

- `SECRET_KEY`
- `DEBUG`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

Existe `.env` local no workspace. Nao exponha segredos em respostas, logs, commits ou documentacao.

## Estado funcional atual

Ja existe:

- usuario customizado `accounts.User` com `role` (`buyer` ou `seller`) e `cashback_balance`;
- cadastro com email unico e escolha de perfil;
- login usando `django.contrib.auth.views.LoginView` com formulario customizado;
- pagina de perfil em `accounts/profile.html`;
- vendedores veem seus proprios anuncios no perfil;
- CRUD de anuncios para vendedores: criar, editar e remover;
- listagem e detalhe de anuncios;
- filtros de anuncios por tipo, categoria e cidade;
- campos de anuncio: nome, descricao, preco, imagem, tipo, categoria, cidade e percentual de cashback;
- carrinho em sessao para compradores;
- adicionar, atualizar quantidade e remover itens do carrinho;
- checkout transacional;
- uso opcional do saldo de cashback no checkout;
- geracao automatica de cashback apos compra concluida.

## Regras de dominio importantes

- Compradores (`buyer`) podem acessar carrinho, adicionar itens e finalizar compras.
- Vendedores (`seller`) podem cadastrar anuncios e editar/remover somente anuncios proprios.
- `Product.seller` e opcional no banco por historico de migracoes, mas novas criacoes pela view atribuem o vendedor autenticado.
- `Product.cashback_percentage` aceita valores de `0` a `100`.
- `Product.cashback_amount` calcula o cashback estimado para uma unidade.
- `Order.total` armazena o total final apos eventual uso de cashback.
- `Order.cashback_used` armazena quanto cashback foi abatido na compra.
- `OrderItem.price` copia o preco do produto no momento da compra.
- `cashback.services.generate_cashback(order)` cria o registro em `Cashback` e soma ao saldo do usuario.

## URLs principais

- `/`: home (`home`)
- `/produtos/`: listagem (`product_list`)
- `/produtos/novo/`: criar anuncio (`product_create`)
- `/produtos/<pk>/`: detalhe (`product_detail`)
- `/produtos/<pk>/editar/`: editar anuncio (`product_update`)
- `/produtos/<pk>/remover/`: remover anuncio (`product_delete`)
- `/carrinho/`: carrinho (`cart_detail`)
- `/carrinho/adicionar/<product_id>/`: adicionar item (`add_to_cart`)
- `/carrinho/atualizar/<product_id>/`: atualizar quantidade (`update_cart_item`)
- `/carrinho/remover/<product_id>/`: remover item (`remove_from_cart`)
- `/carrinho/finalizar/`: checkout (`checkout`)
- `/accounts/register/`: cadastro (`register`)
- `/accounts/login/`: login (`login`)
- `/accounts/perfil/`: perfil (`profile`)

## Pontos de atencao tecnica

- Sempre rode `git status --short` antes de editar. O repositorio pode ter alteracoes locais do usuario.
- O arquivo antigo foi preservado como `bckpAGENTS.md`; este `AGENTS.md` e a referencia atual.
- `settings.py` ainda faz `print(config('DB_NAME'))` durante import. Isso pode vazar o nome do banco no terminal e deve ser tratado como debito tecnico se a tarefa tocar configuracao.
- O banco configurado e PostgreSQL. Mesmo que exista `db.sqlite3`, nao assuma SQLite como banco ativo.
- `STATICFILES_DIRS` aponta para `BASE_DIR / 'cashback_verde' / 'static'`, que hoje corresponde a `cashback_verde/cashback_verde/static`.
- Templates usam Bootstrap via CDN; mudancas visuais devem seguir esse padrao salvo pedido explicito.
- Testes ainda sao minimos nos apps. Para novas regras, adicione testes focados no comportamento alterado.

## Fluxo recomendado para agentes

1. Rode `git status --short`.
2. Entre em `cashback_verde/` para comandos Django.
3. Leia models, views, forms, urls e templates relacionados antes de editar.
4. Se alterar models, crie/ajuste migrations.
5. Preserve alteracoes locais que nao sejam suas.
6. Rode a menor validacao util: `python manage.py check`, teste do app afetado ou suite completa.
7. Informe o que mudou, os arquivos principais e qualquer bloqueio de ambiente.

## Tarefas comuns

### Produtos e servicos

- Verifique `products/models.py`, `products/forms.py`, `products/views.py`, `products/urls.py`.
- Atualize templates em `templates/products/`.
- Preserve permissoes de vendedor e propriedade do anuncio.
- Se mexer em imagem, valide `MEDIA_URL`/`MEDIA_ROOT`.

### Autenticacao e perfil

- Verifique `accounts/models.py`, `accounts/forms.py`, `accounts/views.py`, `accounts/urls.py`.
- Login e logout passam tambem por `django.contrib.auth.urls`.
- Mantenha consistencia entre `role`, menu global e permissoes das views.

### Carrinho e checkout

- Verifique `orders/views.py`, `orders/models.py`, `orders/urls.py` e `templates/orders/cart.html`.
- O carrinho fica na sessao sob a chave `cart`.
- Compradores apenas; vendedores recebem `HttpResponseForbidden`.
- Operacoes de checkout usam `transaction.atomic()` e bloqueiam o usuario com `select_for_update()`.
- Evite duplicar regras financeiras fora dos helpers/servicos existentes.

### Cashback

- Verifique `cashback/models.py` e `cashback/services.py`.
- Mantenha calculos com `Decimal`.
- Considere atomicidade quando alterar saldo ou registros financeiros.
- Se adicionar historico visivel, provavelmente envolvera perfil, templates e consulta de `Cashback`.

## Backlog funcional provavel

Com base no codigo atual, ainda parecem pendentes ou incompletos:

- historico de pedidos para comprador;
- historico de cashback no perfil;
- pagina de confirmacao/detalhe do pedido apos checkout;
- testes funcionais dos fluxos principais;
- melhorias de administracao para `Cashback` e possivelmente pedidos;
- remocao do `print(config('DB_NAME'))` em `settings.py`.

Confirme sempre no codigo antes de assumir que um item do backlog ainda esta aberto.

## O que evitar

- Nao sobrescreva alteracoes locais do usuario.
- Nao exponha conteudo de `.env`.
- Nao troque PostgreSQL por SQLite sem pedido explicito.
- Nao mova o projeto Django para a raiz.
- Nao introduza APIs, frontend SPA ou bibliotecas novas sem necessidade real.
- Nao altere regras de saldo/cashback sem testes ou validacao cuidadosa.

## Ao finalizar uma tarefa

Inclua na resposta:

- resumo objetivo do que mudou;
- arquivos principais afetados;
- validacao executada;
- bloqueios ou riscos restantes, se houver.
