# EleNA: Elevation Based Navigation

## What is EleNA?
The Elevation based navigation is a program that determines a route between two locations based on the desired optimization of elevation gain. It allows users to minimize or maximize elevation gain while also limiting the total distance to a specified percentage of the shortest path. This is particularly useful for hikers and bikers who want to plan their routes based on their desired level of intensity and elevation gain. The system considers the topography of the area and calculates a route that meets the specified optimization criteria.

## Environment requirement:
node.js

python=3.9

## Install dependecies

First, install both the front-end dependencies and the server dependencies using the following two commands:

 `npm install`
 
`pip install -r requirements.txt`

## Run:

Our client runs on port 3000, and our server runs on port 8080. Make sure those two ports are avaiable before running. 

In the project's root directory, run the Flask server using the following command:

`python src/server/server.py`

In the project's root directory, run the React client using the following command:

`npm start`

The homepage will automatically shows up, it might takes longer when you first start the client. If the homepage does not show up, visit:

`localhost:3000`

## Test

In the project's root directory, run the following command:

 `pytest`

