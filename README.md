# ML-Project | Sensor-Fault-Detection

-  Data source | Air Pressure Data that is taken from MongoDB, was picked from the https://www.scania.com/ website.
-  Goal | We need to identify whether the engine failure of a heavy duty vehicles are due to air pressure system or not. 


The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.
## Tech Stack Used
1. Python 
2. FastAPI 
3. Machine learning algorithms
4. Docker
5. MongoDB

## Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions

## How to run?
Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need AWS account to access the service like S3, ECR and EC2 instances.

## Data Collections
![image](https://user-images.githubusercontent.com/57321948/193536736-5ccff349-d1fb-486e-b920-02ad7974d089.png)


## Project Archietecture
![image](https://user-images.githubusercontent.com/57321948/193536768-ae704adc-32d9-4c6c-b234-79c152f756c5.png)


## Deployment Archietecture
![image](https://user-images.githubusercontent.com/57321948/193536973-4530fe7d-5509-4609-bfd2-cd702fc82423.png)




### RESOURCES



Mongo DB URL: 

```
"mongodb+srv://dbUser:<Password>@cluster0.z9ypkxp.mongodb.net/test"
```