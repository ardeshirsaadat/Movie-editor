# Capstone Movie Manager 
## Getting Started

### Installing Dependencies

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight postgres database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
database consists of two simple tables Movie and Actor
# Run app in Dev mode
```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
## Roles
Roles:
###Casting Assistant
- Can view actors and movies
### Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- 3Modify actors or movies
###Executive Producer
- All permissions a Casting Director has and…
- Add or delete a movie from the database

 ### Permissions:
 - delete:movie 		
 - delete:actor 
 - patch:movie 
 - patch:actor
 - post:movie 
 - post:actor 
 - get:actors
 - get:movies
## Endpoints
 ##### GET '/' 
  - redirects to Auth0 login page
 ##### GET '/actos'
 - Required Permission.
 - Fetches all actors 
- Request Arguments: None
- Returns: jsonify({'success': True, 'actors': formated_actors})

##### Get '/movies'
 - Requires permission
 - Request Argument:None
 - Returns jsonify({'success': True, 'movies': formated_movies})

##### Post '/actors
- Requires permission	
- Request Arguments:name,age,gender
- Return jsonify({'success': True})
##### Post '/movies
- Requires permission	
- Request Arguments:movie,release_date
- Return jsonify({'success': True})

##### Delete "/actors/id"
- Requires permission	
- Request Argumenet:id
- Return jsonify({'success': True})
##### Delete "/movies/id"
- Requires permission	
- Request Argumenet:id
- Return jsonify({'success': True})
- Return: new author id

##### PATCH  "/actors/id"
- Requires permission	
- Request Argumenet:any attribute of Actor table
- Return jsonify({
                'success': True,
                'actor': Actor.query.get(id).format()

 ##### PATCH  "/actors/id"
- Requires permission	
- Request Argumenet:any attribute of Movie table
- Return jsonify({
                'success': True,
                'actor': Movie.query.get(id).format()


### Error Handling
Errors are returned as JSON objects in the following format:
  
  {
    "success": False, 
    "error": 404,
    "message": "unprocessable"
      
  }
- 404 – bad request 
- 422 – unprocessable 
- AuthError - authentication errors
## Testing
To run the tests, run

    dropdb library_test
    createdb library_test
    psql library_test < library.psql
    python3 test_flask.py
## Heroku :


## Token :
self.exec = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlV3eWF3RFVGd0pOMFNXSVBlX2J2YiJ9.eyJpc3MiOiJodHRwczovL21vdmllLW1hbmFnZXItYXJkZXNoaXIudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNGRiZDZmYTI2MGY0MDA2YTc4NDZlNyIsImF1ZCI6Im1vdmllIiwiaWF0IjoxNjE1NzQ4MjAxLCJleHAiOjE2MTU3NTU0MDEsImF6cCI6IkwwZEIyRTJGRHJtMnR0TUdqZ3FnVEZxNTY2NEhkcXI0Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.hY5vSszAoqMn9JtuTowtxfybkOyYEFwFFRb2LBqv3st-xZdVpO06Cf1y8OrEBAniGLYKDAC1UWeBdn70vBs-7GPm_z9EwWU0SybqYU9Jj5sitRn-ebpxZYyRw6Y-IIIrSWRubMBmXBOuNqQpRbyxonmMudBPXRsYg0bi7MBYoB4ewi2Mhrw_Bhhct73mTe97GCkzhy85Xnqfx_2mppnFJDJbHOWmCBst9dw52g8ECiwQued7eSk53HHdZ3drLOzRnx0A60Q5_aFSoWysxaUMgtjiAHndSH8XcxH2rUGesTNvyeOoXPECtTgeEwIEKPpNrhgD3A7JJDiZ0Tll2Rx2bw'