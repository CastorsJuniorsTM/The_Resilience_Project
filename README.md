# README

## Authors  
- FIEVET Thibaud
- HERVE Maxence

## Project Overview  
This project is a simple Community Management System developed for Database course.    
The goal is to design a database and create a small Python application that interacts with it.

The system includes basic management of individuals, communities, skills, services, messages, and locations.

The system is inspired by the Resilience Project, whose objective is to connect individuals and communities in a collaborative network of mutual assistance.
Anyone can add themselves to the database, create communities, and define relationships. Communities and individuals can also declare links to each other, share skills, offer services (free, barter-based, or commercial), and exchange messages.
Members of a community can participate in its management, including voting to exclude a person: if more than half of the members vote against someone, that person is removed from the community.
The system also handles geolocation, generating OpenStreetMap links from stored coordinates.
Finally, the application must provide a few required views, such as community membership, message threads, and proximity between individuals or communities.

## Repository Structure
.
├── UML/
│   Contains the UML class diagram (PlantUML + PNG)
│
├── MLD/
│   Contains the logical data model (MLD)
│
├── SQL/
│   Contains the SQL schema and sample data
│
└── python/

## Main Features
- Individuals and communities management  
- Membership rules (including voting for exclusion)  
- Skills and services management  
- Messaging between users or communities  
- Geolocation of individuals  
- Required views: community view, message thread view, proximity view  

## How to Use
1. Create the database using the SQL files.  
2. Run the Python application found in the `python/` folder.  
3. Test the system with the provided sample data.

## Files Included  
- UML diagram  
- Logical model (MLD)  
- SQL schema
- Python application
- Test data