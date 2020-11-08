### Data Factory pipeline and Durable Functions copying data from Azure Storage to AWS S3

![Architecture](https://github.com/rebremer/copy-azurestorage-awss3/blob/master/pictures/architecture_overview.png)

7GB file took 12 minutes, VNET integration and Azure Function MI are used to authenticate to Azure Storage, AWS key id/credentials to AWS S3. See also Azure Data Factory pipeline below.

![Architecture](https://github.com/rebremer/copy-azurestorage-awss3/blob/master/pictures/data_factory_overview.png)