### Data Factory pipeline and Durable Functions copying data from Azure Storage to AWS S3

![Architecture](https://github.com/rebremer/copy-azurestorage-awss3/blob/master/pictures/architecture_overview.png)

7GB file took 12 minutes, VNET integration and Azure Function MI are used to authenticate to Azure Storage and key vualt. AWS key id/credentials are stored in key vault and used to authenticate to AWS S3. Following steps need to be executed:

1. Create Azure Durable Function, Azure Data Factory, Key vault and Azure Storage. Add container and file (e.g. 5 GB) to container.
2. Assing Managed Identity to your Azure Function and grant RBAC accesss to your storage account and access policy key vault
3. Create AWS S3 account and bucket. Create AWS user with programmatic access to S3 bucket and add credentials to key vault. 
4. Deploy code in folder DurableFunction to your Durable function. Configure Azure Functions params with your variables from step 1 and 2.
5. Add VNET integration to Azure Function and whitelist VNET in firewall of Azure Storage and Key vault. Whitelist Azure IR IP or ADFv2 in managed VNET in firewall Azure Function. Whitelist IP of Azure function in AWS S3.
6. Deploy code in folder adfv2 in your Azure Data Factory to create pipeline and then run pipeline.

Azure Data Factory pipeline is depicted below.

![Architecture](https://github.com/rebremer/copy-azurestorage-awss3/blob/master/pictures/data_factory_overview.png)