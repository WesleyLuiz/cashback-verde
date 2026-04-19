# Backlog do Projeto

Baseado no documento `Template para TCC - FULLSTACK (Projeto Prático)-ruVA4Hit.docx`.

## Status atual

### Feito

- estrutura base do projeto Django
- usuário customizado com papéis `buyer` e `seller`
- cadastro de usuário
- login com `django.contrib.auth`
- listagem de produtos
- detalhe do produto
- modelos de pedido, itens de pedido e cashback
- serviço inicial de geração de cashback

### Em andamento

- navegação e fluxo de autenticação
- cadastro de produto por vendedor

### Falta

- carrinho de compras
- finalização de pedido
- geração automática de cashback no fechamento da compra
- painel do usuário
- histórico de pedidos
- histórico de cashback
- testes funcionais principais

## Ordem recomendada

1. Fechar autenticação e navegação global.
2. Finalizar cadastro de produto para vendedor.
3. Implementar carrinho.
4. Implementar checkout e criação de pedidos.
5. Integrar cashback automático após compra concluída.
6. Criar painel do usuário com saldo e histórico.
7. Cobrir fluxos principais com testes.

## Critérios de pronto por etapa

### 1. Autenticação e navegação

- login redireciona para uma rota existente
- logout retorna para a home
- menu mostra links corretos para visitante, comprador e vendedor

### 2. Cadastro de produto

- vendedor acessa a rota de criação
- comprador não consegue cadastrar produto
- formulário salva nome, descrição, preço, imagem e flag sustentável
- após salvar, usuário é redirecionado com mensagem de sucesso

### 3. Carrinho e pedido

- usuário autenticado consegue adicionar item
- carrinho calcula subtotal e total
- checkout cria `Order` e `OrderItem`

### 4. Cashback

- compra concluída gera registro em `Cashback`
- saldo do usuário é atualizado
- histórico fica visível no painel
