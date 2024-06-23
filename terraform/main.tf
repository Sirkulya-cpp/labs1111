locals {
  project_name        = "Terraform_Laba_2"
  security_group_name = "LabES2-security-group"
  instance_name       = "LabES2"
  ubuntu_ami          = "ami-0faab6bdbac9486fb"
  region              = "eu-north-1"
  key_pair_name       = "KeysForLAb"
  author              = "Sirkulya"
}

provider "aws" {
  region = "local.region"  
}
 
resource "aws_instance" "LabES2" {
  ami             = local.ubuntu_ami
  instance_type   = "t2.micro"
  key_name        = aws_key_pair.KeysForLAb_keys.key_name
  security_groups = [aws_security_group.LabES2-sg.name]
  user_data       = file("./init.sh")
  tags = {
    Name    = local.instance_name,
    Project = local.project_name,
    Author  = local.author
  }

}

resource "aws_security_group" "LabES2" {
  name = local.security_group_name

  ingress{
    from_port   = 80
    to_port     = 80
    protocol    ="tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    ="-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = local.security_group_name,
    Project = local.project_name,
    Author  = local.author
  }
}

resource "aws_key_pair" "KeysForLAb" {
  key_name = local.aws_key_pair_name
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCLgqq0rj1FHSNeT7wOrPgd27V0HCjnLGSec999n1qTg4M/7KPvNnF/KwXOGMLMeE/clHSs2j7eltwlHLnbIrtS7SHpjf16A6u4VlNbGwTpzQDRVlUZpNy2jCRPiEOVmKa5J238hTG6a5Bh6Rya4GfwxInq3e/Vxpb4KexG/7yzhqz9i90W9OY+cWDyBRKRtxwYaqd5TL6BqRkBKsmXNgkNgr1uOaVmvtTdTAwEZl2FjE4PTzcarJ/Tp85PDSbgvr9wpcNigHYBWGAZfeU32p7qaMAmhYqIA6mT9TwRL9tRS7d1RmhTHzqEYV0NdBOD56t1IYpEjcZkhv8+CBmtPqXl"
  tags = {
    Name    = local.key_pair_name,
    Project = local.project_name,
    Author =  local.author
  }
}

output "ec2-public-dns" {
  value = aws_instance.LabES2.public_dns
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  cloud {
    organization = "laba_2"

    workspaces {
      name = "laba2"
    }
  }

  required_version = ">= 1.2.0"
}