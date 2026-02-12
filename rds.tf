data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# segurança de grupo para o RDS
resource "aws_security_group" "rds_sg" {
  name        = "rds-postgres-sg"
  description = "Postgre acesso ao lambda"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "PostgreSQL para VPC"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.default.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# DB subnet group
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = data.aws_subnets.default.ids

  tags = {
    Name = "rds-subnet-group"
  }
}


# Aurora PostgreSQL Serverless v2 Cluster
# Preciso criptografar a nova senha
resource "aws_rds_cluster" "postgres" {
  cluster_identifier      = "tasks-cluster"
  engine                  = "aurora-postgresql"
  engine_version          = "15.3"
  database_name           = "tasksdb"
  master_username         = "caseTodo"
  master_password         = "caseTodo" 
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]
  storage_encrypted       = true
  skip_final_snapshot     = true

  serverlessv2_scaling_configuration {
    min_capacity = 0.5
    max_capacity = 2
  }
}

# Instância Serverless v2

resource "aws_rds_cluster_instance" "postgres_instance" {
  cluster_identifier = aws_rds_cluster.postgres.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.postgres.engine
  engine_version     = aws_rds_cluster.postgres.engine_version
}

# Outputs dos endpoints
output "rds_endpoint" {
  value = aws_rds_cluster.postgres.endpoint
}

output "rds_database_name" {
  value = aws_rds_cluster.postgres.database_name
}