
# Case JOTA

## Acessos

```json
ADM:
  {
    "email": "adm@example.com",
    "password": "senhaADM"
  }

Editor:
  {
    "email": "editor@example.com",
    "password": "senhaEditor"
  }

Leitor:
  {
    "email": "leitor@example.com",
    "password": "senhaLeitor"
  }
```

## COMECE por aqui

- Criar ambiente virtual:
  ```bash
  python -m venv venv
  ```

- Ativar ambiente:
  ```bash
  source venv/bin/activate
  ```

- Instalar dependências:
  ```bash
  make setup
  ```

- Iniciar banco de dados:
  ```bash
  make start-db
  ```

- Executar migrações:
  ```bash
  make migrate
  ```

- Iniciar servidor:
  ```bash
  make start-server
  ```

## Style Guide

Para este projeto, decidi seguir o [**HackSoftware/Django-Styleguide**](https://github.com/HackSoftware/Django-Styleguide). Esse guia é usado como referência por muitas equipes que trabalham com Django, e ajuda a manter uma estrutura limpa, coerente e fácil de escalar.

A principal vantagem de usá-lo é que ele deixa cada parte do sistema no seu devido lugar. A lógica de negócio fica separada das views, os dados são manipulados por actions e selectors bem definidos, e tudo fica mais fácil de entender, tanto para quem desenvolve quanto para quem vai dar manutenção depois.

Além disso, o style guide conversa muito bem com os princípios do Domain-Driven Design (DDD), permitindo que o projeto seja orientado pelas regras do domínio da aplicação, e não pela estrutura técnica do framework.


## [Diagrama do Banco de Dados](https://dbdiagram.io/e/67d58a3175d75cc84431913b/682b500d1227bdcb4effee9b)

## Escopo

Desenvolver uma API RESTful para gestão de notícias, contemplando autenticação e diferentes perfis de usuário.

## Decisões Técnicas

### Gestão de Perfis

Optamos por usar o sistema de grupos nativo do Django (`django.contrib.auth.models.Group`) para representar os perfis de usuário (Admin, Editor, Leitor), em vez de criar um campo `role`. Essa escolha oferece:

- Flexibilidade e Extensibilidade
- Separação de Responsabilidades
- Compatibilidade com middleware e autenticação padrão
- Facilidade para controlar permissões finas via painel admin ou código

### Modelagem (VERTICAIS x PLANOS x USUÁRIO x NOTÍCIA)

Tanto os planos quanto as verticais foram modelados como entidades independentes com suporte a CRUD, em vez de enums fixos. Essa abordagem oferece maior flexibilidade e permite:

- Alterações dinâmicas via painel administrativo, sem necessidade de alterações no código
- Relacionamento N:1 entre o usuário e seu respectivo plano de acesso
- Relacionamento N:N entre planos e verticais, possibilitando que um plano ofereça acesso a múltiplas verticais e que uma vertical esteja presente em diferentes planos
- As notícias se vinculam diretamente a uma vertical (e não ao usuário), e o acesso é controlado com base no plano do usuário, mantendo o usuário desacoplado da lógica da notícia
- Além disso, foi adotada uma **dupla camada de validação de acesso**: uma baseada na vertical da notícia (associada ao plano do usuário) e outra através de um campo booleano `access_pro`. Essa camada adicional permite que determinadas notícias — mesmo pertencentes a verticais públicas — sejam marcadas como exclusivas para assinantes PRO.

Essa modelagem proporciona escalabilidade e flexibilidade para evoluir a plataforma sem travas técnicas.
