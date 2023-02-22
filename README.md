# Oscar


This project is part of [DIH^2](http://www.dih-squared.eu/). For more information check the RAMP Catalogue entry for the
[components](https://github.com/xxx).

| :books: [Documentation](docs/usermanual.md) | :whale: [Docker Hub](https://hub.docker.com/r/phm14/oscar) |
| --------------------------------------------- | ------------------------------------------------------------- |



## Contents

-   [Background](#background)
-   [Requirements](#requirements)
-   [Instructions](#instructions)
-   [Usage](#usage)
-   [License](#license)

## Background
Oscar is an IoT application for enabling communication between an interactive Graphical User Interface (GUI)
and a robotic arm assisting the operator during the assembly process.

### Main modules
1. CSV Parser: component in charge of loading the data of the components and processing steps on Fiware.
2. ROS Services for Fiware-UI-Robot: component enabling communication from UI to the robotic arm
3. ROS Services for Kinect-Fiware: component enabling communication from the camera to Fiware
4. HoloLens UI application: interactive Graphical User Interface
## Requirements
### CSV Data Format ###
Files containing data must be in csv format, using the **comma** ```,``` delimiter.
As for now csv data is split among the following files:
```
Component.csv
Step.csv
Macrostep.csv
UseCase.csv
```
where the entity ```UseCase``` contains one or more entities ```Macrostep```, which, in turn contain one or more
entities ```Step```.

* The first row of the csv tables contains the attribute name (**first letter in lowercase**) and in the case of relationship
  attributes their name convention must follow the rule:
  ```name_of_attribute = 'ref' + name_of_external_entity```.
  So if, for example, an entity ```Step``` has an attribute linking to the ```Component``` entity the name of the
  attribute must be ```refComponent```.

* The second row must contain the type of the attribute, the type of the first column containing the ```id``` must
  be of type ```None```, while the relationship attributes must be of type ```Relationship```

## Instructions ##
Only the first time execute the command:
```
docker network create fiware_default
```
then run the containers for mongo and orion:
```
docker run -d --name=mongo-db --network=fiware_default   --expose=27017 mongo:4.2 --bind_ip_all
docker run -d --name fiware-orion -h orion --network=fiware_default   -p 1026:1026  fiware/orion -dbhost mongo-db
```


To run the container execute the command
```
docker run --ipc=host  -it  phm14/oscar
```
Make sure that in the file ```config.yaml``` inside the folder ```src/oscar_core``` the entities address field ```entities_address: http://IP_ADDRESS:PORT_NUMBER/v2/entities/``` is correct:
```
nano src/oscar_core/config.yml
```
and change accordingly ```entities_address: http://IP_ADDRESS:PORT_NUMBER/v2/entities/```

Inside the container run the following:
```
source install/setup.bash
ros2 launch bring_up bring_up_launch.py
```
### Load data ###
To load data on Fiware execute the command:
```
python parser_to_fiware.py
```
the script file must be on the same folder of config.yml file to work


## Usage

Information about how to use Oscar-GUI can be found in [User & Programmers Manual](docs/usermanual.md).


## License

[Apache2.0](LICENSE) © 2022
