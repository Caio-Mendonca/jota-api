# Case JOTA


# COMECE por aqui:
 ## Create venv
 ```
 python -m venv venv
 ```

 ## Init venv
 ```
 source venv/bin/activate
 ```
 ## Install requirements
 ```
 make setup
 ```
 ## Init DataBase
  ```
 make start-db
 ```


# Style Guide
Para o desenvolvimento desse projeto escolhi o style guide 

# Modelo do banco de dados: 

<iframe width="560" height="315" src='https://dbdiagram.io/e/67d58a3175d75cc84431913b/682b500d1227bdcb4effee9b'> </iframe>

# Escopo
Desenvolver uma API RESTful para gestão de notícias, contemplando autenticação e diferentes perfis de usuário.

## Checklist de Entregáveis
- [ ] Autenticação JWT implementada
- [ ] Perfis de usuário (Admin, Editor, Leitor) configurados como grupos
- [ ] CRUD de notícias (título, subtítulo, conteúdo, imagem, autor, data de publicação, status)
- [ ] Upload de imagens funcionando
- [ ] Agendamento de publicações implementado
- [ ] Categorias de notícias por verticais configuradas
- [ ] Controle de acesso baseado em plano e vertical
- [ ] Modelo de planos e verticais com CRUD
- [ ] Processamento assíncrono com filas/eventos para notificações
- [X] Banco de dados PostgreSQL configurado
- [ ] Testes unitários e de integração criados
- [ ] Pipeline CI/CD configurado (GitHub Actions)
- [ ] Documentação da API com Swagger/OpenAPI
- [ ] Docker e docker-compose configurados para deploy

## Decisões técnicas
- Gestão de perfis:
    -  Optei por utilizar o sistema de grupos nativo do Django (django.contrib.auth.models.Group) para o gerenciamento dos perfis de usuário (Admin, Editor, Leitor) ao invés de criar um campo role diretamente no modelo ou usar enums personalizados, por várias razões técnicas e arquiteturais importantes:
        - Flexibilidade e Extensibilidade
        - Separação de Responsabilidades
        - Compatibilidade com Middleware e Autenticação
        - Facilidade para Controle Fino de Permissões

- Modelagem (VERTICAIS x PLANOS x USUÁRIO x NOTÍCIA):
    - Para a definição das verticais, considerei duas opções: criar um ENUM fixo ou modelar as verticais como uma entidade independente, permitindo customização via CRUD. A mesma dúvida ocorreu em relação aos planos de assinatura disponíveis na plataforma. Como o usuário terá uma relação de N:1 com o plano e o plano terá uma relação de 1:N com as verticais, optei por modelar tanto o Plano quanto a Vertical como tabelas separadas, possibilitando alterações via CRUD para maior flexibilidade.
    
    - Quanto à validação do acesso do usuário às notícias, decidi que essa lógica será determinada diretamente pela notícia, que terá relacionamento com o plano (e por consequência, com as verticais), mantendo o modelo do usuário independente dessa relação.

    Nessa abordagem procurei uma maior escalabilidade e facilidade na manutenção do sistema, permitindo que planos e verticais sejam gerenciados dinamicamente sem impactar diretamente os usuários.

- 
