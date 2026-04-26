# Cashback Verde

Marketplace sustentável desenvolvido em Django para um projeto de TCC. A aplicação conecta compradores e vendedores de produtos e serviços com proposta sustentável, permitindo cadastro de anúncios, compras por carrinho e geração de cashback verde.

## Sobre o projeto

O Cashback Verde tem como objetivo incentivar escolhas de consumo mais sustentáveis por meio de um marketplace com benefício financeiro. Compradores podem navegar por anúncios, filtrar produtos e serviços, montar um carrinho e finalizar compras. A cada compra concluída, o sistema calcula um percentual de cashback configurado no anúncio e credita esse valor no saldo do comprador.

Vendedores podem criar, editar e remover seus próprios anúncios, informando preço, imagem, cidade, categoria, tipo de item e percentual de cashback.

## Funcionalidades

- Cadastro de usuários com perfil de comprador ou vendedor.
- Login e logout usando o sistema de autenticação do Django.
- Perfil do usuário com informações da conta.
- Listagem de anúncios com filtros por tipo, categoria e cidade.
- Detalhe de produto ou serviço com cashback estimado.
- Cadastro, edição e remoção de anúncios por vendedores.
- Carrinho de compras para compradores autenticados.
- Atualização e remoção de itens do carrinho.
- Checkout com criação de pedido e itens de pedido.
- Uso opcional de saldo de cashback no checkout.
- Geração automática de cashback após a compra.
- Área administrativa do Django para gerenciamento dos dados.

## Tecnologias utilizadas

- Python
- Django 5.2.13
- PostgreSQL
- psycopg2-binary
- python-decouple
- Pillow
- Bootstrap 5.3.3 via CDN

## Estrutura principal

```text
cashback_verde/
├── accounts/          # usuário customizado, cadastro, login e perfil
├── cashback/          # modelo e serviço de cashback
├── cashback_verde/    # configurações do projeto Django
├── core/              # home e rotas centrais
├── orders/            # carrinho, checkout, pedidos e itens
├── products/          # anúncios, filtros, formulários e CRUD
├── templates/         # templates HTML compartilhados e por app
├── media/             # uploads locais
├── manage.py
└── requirements.txt
```

## Pré-requisitos

- Python 3 instalado.
- PostgreSQL instalado e em execução.
- Um banco de dados PostgreSQL criado para o projeto.
- Ambiente virtual Python recomendado.

## Configuração do ambiente

Clone o repositório e entre na pasta do projeto Django:

```bash
cd cashback_verde
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` dentro da pasta `cashback_verde/` com as variáveis necessárias:

```env
SECRET_KEY=sua-chave-secreta
DEBUG=True
DB_NAME=nome_do_banco
DB_USER=usuario_do_banco
DB_PASSWORD=senha_do_banco
DB_HOST=localhost
DB_PORT=5432
```

Execute as migrações:

```bash
python manage.py migrate
```

Opcionalmente, crie um superusuário para acessar o admin:

```bash
python manage.py createsuperuser
```

Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:8000/
```

## Rotas principais

- `/`: página inicial.
- `/produtos/`: listagem de anúncios.
- `/produtos/novo/`: cadastro de anúncio por vendedor.
- `/produtos/<id>/`: detalhe de anúncio.
- `/produtos/<id>/editar/`: edição de anúncio pelo vendedor dono.
- `/produtos/<id>/remover/`: remoção de anúncio pelo vendedor dono.
- `/carrinho/`: carrinho do comprador.
- `/carrinho/finalizar/`: checkout.
- `/accounts/register/`: cadastro de usuário.
- `/accounts/login/`: login.
- `/accounts/perfil/`: perfil do usuário.
- `/admin/`: painel administrativo do Django.

## Perfis de usuário

### Comprador

O comprador pode visualizar anúncios, adicionar itens ao carrinho, finalizar compras, usar cashback disponível e receber novo cashback após uma compra concluída.

### Vendedor

O vendedor pode cadastrar produtos ou serviços, editar anúncios próprios, remover anúncios próprios e acompanhar seus anúncios na página de perfil.

## Regras de cashback

- Cada anúncio possui um percentual de cashback entre 0% e 100%.
- O cashback estimado é calculado com base no preço do item e no percentual do anúncio.
- No checkout, o comprador pode usar o saldo de cashback disponível como desconto.
- Após a compra, o sistema gera um registro de cashback e atualiza o saldo do comprador.
- Os cálculos financeiros usam `Decimal` para evitar problemas de precisão.

## Executando testes

Com o ambiente virtual ativado, execute:

```bash
python manage.py test
```

Para validar a configuração geral do projeto:

```bash
python manage.py check
```

## Status atual

Implementado:

- autenticação e cadastro;
- perfis de comprador e vendedor;
- CRUD de anúncios para vendedores;
- filtros de produtos e serviços;
- carrinho de compras;
- checkout;
- uso e geração automática de cashback;
- testes automatizados para fluxos principais.

Pendências e melhorias possíveis:

- histórico de pedidos para compradores;
- histórico de cashback no perfil;
- página de confirmação ou detalhe do pedido;
- melhorias no painel administrativo;
- refinamento visual das telas;
- remoção de logs temporários em configurações, caso existam.

## Observações para desenvolvimento

- O projeto está configurado para PostgreSQL.
- Não exponha valores reais do `.env` em commits ou documentação.
- Os templates usam Bootstrap via CDN.
- O app Django está dentro da pasta `cashback_verde/`, não na raiz do repositório.
- Alterações em modelos devem ser acompanhadas de migrações.

## Licença

Projeto acadêmico desenvolvido para fins de estudo.
