terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = "us-west-2" # Change this to your desired region
}

resource "aws_opensearchserverless_collection" "aoss_example" {
  name        = "aoss-example"
  description = "Vector search demo"
  type        = "VECTORSEARCH"

  depends_on = [aws_opensearchserverless_security_policy.encryption_policy]
}

resource "aws_opensearchserverless_access_policy" "data_access_policy" {
  name        = "aoss-example-access-policy"
  type        = "data"
  description = "Access policy for aoss-example collection"
  policy = jsonencode([
    {
      Description = "Access for SSO user"
      Rules = [
        {
          ResourceType = "index"
          Resource     = ["index/*/*"]
          Permission   = ["aoss:*"]
        },
        {
          ResourceType = "collection"
          Resource     = ["collection/aoss-example"]
          Permission   = ["aoss:*"]
        }
      ]
      Principal = ["arn:aws:sts::123456789012:assumed-role/AWSReservedSSO_AWSAdministratorAccess_abcdefg12345/clayton@claytondavis.dev"]
    }
  ])
}

resource "aws_opensearchserverless_security_policy" "network_policy" {
  name        = "aoss-example-network-policy"
  type        = "network"
  description = "Network policy for aoss-example collection"
  policy = jsonencode([
    {
      Rules = [
        {
          ResourceType = "collection"
          Resource     = ["collection/aoss-example"]
        },
        {
          ResourceType = "dashboard"
          Resource     = ["collection/aoss-example"]
        }
      ]
      AllowFromPublic = true
    }
  ])
}

resource "aws_opensearchserverless_security_policy" "encryption_policy" {
  name        = "aoss-example-security-policy"
  type        = "encryption"
  description = "Encryption policy for aoss-example collection"
  policy = jsonencode({
    Rules = [
      {
        ResourceType = "collection"
        Resource     = ["collection/aoss-example"]
      }
    ]
    AWSOwnedKey = true
  })
}