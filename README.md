# Case Todo AWS – Automação de Tarefas

Este projeto implementa uma **aplicação de gerenciamento de tarefas (CRUD)** utilizando **AWS Lambda**, **DynamoDB** e **API Gateway**. Seguindo o padrão **clean architecture**, separando camadas de domínio, usecases, infraestrutura e handlers.  

## 🏗️ Estrutura do Projeto
lambda/
└── tarefa_lambda/
├── domain/ # Entidade Task com regras de negócio
│ └── task.py
├── dto/ # DTOs para validação de payload
│ └── create_task_dto.py
├── handlers/ # Funções Lambda para cada operação do CRUD
│ ├── create.py
│ ├── update.py
│ ├── delete.py
│ ├── get_task.py
│ ├── list_tasks.py
│ └── list_all_tasks.py
├── infra/ # Repositório de acesso ao DynamoDB
│ └── task_repository.py
├── usecases/ # Regras de negócio e fluxo de operações
│ └── task_usecase.py
└── main.py # Entry point da Lambda

## 🔹 Tecnologias Utilizadas

- **Python 3.10**
- **AWS Lambda**
- **DynamoDB**
- **API Gateway**
- **Boto3** (AWS SDK para Python)

---

## 📦 Entidades e Camadas

### Domain
- **Task** (`domain/task.py`)
  - Atributos: `id`, `titulo`, `descricao`, `status`, `criado_por`, `data_criacao`, `data_conclusao`
  - Valida `status` com três opções: `"Pendente" | "Em Andamento" | "Concluída"`
  - Métodos:
    - `to_dict()` → converte objeto para persistência no DynamoDB
    - `to_response()` → converte objeto para resposta da API

### DTOs
- `create_task_dto.py` → Valida payload de criação de tarefa

### UseCases
- **TaskUseCase** (`usecases/task_usecase.py`)
  - Contém **regras de negócio**
  - Atualização parcial de tarefas
  - Validação de usuário (`criado_por`) para operações sensíveis
  - Validação de status

### Handlers
- Funções Lambda que processam eventos do API Gateway:
  - `handle_create`, `handle_update`, `handle_delete`
  - `handle_get`, `handle_list`, `handle_all_list`

### Infra
- **TaskRepository** (`infra/task_repository.py`)
  - Responsável por acessar o **DynamoDB**
  - Métodos: `create`, `get_by_id`, `get_all`, `update`, `delete`
  - Usa `ConditionExpression` para garantir que apenas o criador possa alterar/deletar a tarefa

---

## 🔹 API Endpoints

| Método | Endpoint           | Descrição                              | Headers Necessários |
|--------|------------------|----------------------------------------|------------------|
| POST   | `/tasks`          | Criar uma tarefa                        | `criado_por`      |
| GET    | `/tasks`          | Listar tarefas do usuário               | `criado_por`      |
| GET    | `/tasks/all`      | Listar todas as tarefas (admin)        | -                |
| GET    | `/tasks/{id}`     | Buscar tarefa por ID                     | `criado_por`      |
| PUT    | `/tasks/{id}`     | Atualizar tarefa                         | `criado_por`      |
| DELETE | `/tasks/{id}`     | Excluir tarefa                           | `criado_por`      |

> Todos os endpoints exigem o header `criado_por` para validação de autorização, exceto `/tasks/all`.

---

## 🔄 Fluxo de Operação

Exemplo: **Atualizar tarefa**

1. Cliente faz `PUT /tasks/{id}` + JSON body
2. API Gateway dispara a Lambda (`main.py`)
3. Lambda extrai `criado_por` do header e chama `handle_update`
4. Handler chama `TaskUseCase.update_task`
5. UseCase:
   - Busca tarefa existente
   - Valida se `criado_por` bate
   - Valida status
   - Chama `TaskRepository.update`
6. Repository atualiza DynamoDB com **ConditionExpression**
7. Resposta retorna para cliente via API Gateway

---

## ⚙️ Regras de Negócio

- **Usuário** só pode atualizar/deletar suas próprias tarefas
- **Status** permitido: `Pendente | Em Andamento | Concluída`
- **Update parcial:** apenas campos enviados no payload são alterados
- **Data de criação** é setada automaticamente
- **Data de conclusão** é opcional e atualizável

---

## 🔹 Exemplo de Payloads

### Criar tarefa
``json
POST /tasks
Headers:
  criado_por: usuario123

Body:
{
  "titulo": "Estudar AWS",
  "descricao": "Revisar Lambda e DynamoDB",
  "status": "Pendente"
}

### Modelo de resposta API:
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "titulo": "Estudar AWS",
  "descricao": "Adicionar estudo de API Gateway",
  "status": "Em Andamento",
  "criado_por": "usuario123",
  "data_criacao": "2026-02-12T04:00:00",
  "data_conclusao": null
}

# Case Todo AWS – Infraestrutura como Código (Terraform)

Este projeto provisiona a **infraestrutura necessária para a automação de tarefas** no AWS usando **Terraform**. Ele cria:

- **API Gateway** para expor endpoints REST
- **AWS Lambda** para lógica de negócio
- **DynamoDB** para persistência
- **IAM Roles** para permissões

## 📂 Estrutura do Projeto

create_terraform/
├── main.tf # Provider e configuração geral
├── dynamodb.tf # Tabela DynamoDB
├── api_gateway.tf # API Gateway e integração Lambda
├── iam.tf # Roles e políticas IAM
├── tarefa_lambda.zip # Código da Lambda empacotado
├── terraform.tfstate # Estado atual da infraestrutura
├── terraform.tfstate.backup
└── .terraform/ # Plugins e providers do Terraform


## 🚀 Deploy e Execução Local

Esta seção explica como **deployar a infraestrutura AWS** usando Terraform e como **testar a Lambda localmente** antes de subir para a nuvem.

---

### 1️⃣ Pré-requisitos

- Python 3.10+
- pip / virtualenv
- AWS CLI configurado (credenciais e região `sa-east-1`)
- Terraform 1.5+ instalado
- Node.js (opcional se usar SAM ou Serverless no futuro)

---

### 2️⃣ Deploy na AWS com Terraform

1. Navegue para a pasta do Terraform:

``bash
cd create_terraform

2. Inicialize o Terraform (baixar providers):
terraform init

3. Validar os arquivos de configuração:
terraform validate

4. Planejar a criação da infraestrutura:
terraform plan

5.Aplicar a infraestrutura:
terraform apply

Confirme digitando 'yes' quando solicitado.

Isso vai criar:
DynamoDB (Tasks)
Lambda (tarefa_lambda)
API Gateway com todos os endpoints
IAM Roles e Policies

6.Após o deploy, você receberá a URL base da API. Exemplo:
https://0n8tr5v6p9.execute-api.sa-east-1.amazonaws.com

##Testes localmente:
1. Crie um ambiente virtual:
cd lambda/tarefa_lambda
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

2. Simule uma execução local usando um evento de teste:
import json
from main import lambda_handler

# Exemplo de evento para criar tarefa
event = {
    "requestContext": {
        "http": {"method": "POST"}
    },
    "headers": {
        "criado_por": "usuario_teste"
    },
    "body": json.dumps({
        "title": "Test Task",
        "description": "Executando Lambda localmente"
    })
}

response = lambda_handler(event, None, criado_por="usuario_teste")
print(response)


