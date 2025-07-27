#!/bin/bash
az group create --name BillingResourceGroup --location eastus
az cosmosdb create --name BillingCosmosDB --resource-group BillingResourceGroup
az storage account create --name billingstorage --resource-group BillingResourceGroup --sku Standard_RAGRS
az storage container create --account-name billingstorage --name billing-archive

