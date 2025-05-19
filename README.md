# Case JOTA

# Style Guide
Para o desenvolvimento desse projeto escolhi o style guide 

# Gestão do projeto
Utilizei a plataforma github criando um projeto para controle das tarefas mapeadas e criação de historias

# Escopo
Desenvolver uma API RESTful para gestão de notícias, contemplando autenticação e diferentes perfis de usuário. A solução deve ser escalável e eficiente, utilizando filas ou eventos para processamento assíncrono, além de seguir padrões modernos de desenvolvimento backend.

## Requisitos

## Decisões tecnicas
- (VERTICAIS x PLANOS X USUARIO X NOTÍCIA) Para definição das verticais fiquei entre cria-las como ENUM ou criar um dominio de entidade que fosse capaz de ser customizado via CRUD, a mesma dúvida se deu em relação aos planos de assinatura disponiveis na plataforma. Uma vez que um usuario terá uma relação de N:1 com o plano e N:N com as verticais.
Para essa decisão considerei que a validação de quais noticiais o usuario terá acesso se dará diretamente na noticia, sendo ela que terá o relacionamento com o plano e essa relação ficando alheia ao usuario e as verticais.

Sendo assim temos o seguinte diagrama:

# Diagrama da Modelagem
