# Full Stack API Final Project

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others. 

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Api Documentation
`https://documenter.getpostman.com/view/5081938/SzS1TonS`

Click [here](https://documenter.getpostman.com/view/5081938/SzS1TonS)


## Api Endpoints
Currently,
<table>
  <tr>
    <td>HTTP VERB</td>
    <td>ENDPOINT</td>
    <td>TASK</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>api/categories/</td>
    <td>Create A Question category</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>api/categories/</td>
    <td>Return ArrayList of Question Categories</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>api/questions/</td>
    <td>Create A Question</td>
  </tr>
  
  <tr>
    <td>GET</td>
    <td>api/questions?page=1</td>
    <td>Return an array list of questions with pages</td>
  </tr>
  
  <tr>
    <td>DELETE</td>
    <td>api/questions/{question_id}</td>
    <td>Delete question with the stated ID</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>api/questions/{question_id}</td>
    <td>Get a specific question details base on ID</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>api/categories/{category_id}/questions</td>
    <td>Get set of question in a category base on Category ID</td>
  </tr>
  
   <tr>
    <td>POST</td>
    <td>api/questions/search</td>
    <td>Get set of questions base on search term</td>
  </tr>
  
   <tr>
    <td>POST</td>
    <td>api/play_quizzes</td>
    <td>Return Specific question at Random base on category and previous question</td>
  </tr>
  </table>
  
  
  GET `'/api/categories'`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: `None`
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```



POST `'/api/categories'`
- Create new categories for questions to be added.
- Request Arguments: ```{
	"type":"Biochemistrys"
}```
- Response: An object of categories updated 
```
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 23,
      "type": "Biochemistrys"
    }
  ],
  "category created": "Biochemistrys",
  "created": 23,
  "success": true,
  "total_categories": 23
}

```


POST `/api/questions`

- Add questions to already created category.
- Request Arguments: 
```
{
	"question": "Who discovered penicillin?",
	"answer":"Alexander Fleming",
	"difficulty":3,
	"category":1,
	"id":8
}
```
- Response: Returns objects of existing questions with created id.
```angular2html
{
  "created": 33,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
    ],
  "success": true,
  "total_questions": 22
}
```

POST `'api/questions/search'`

- Search questions database base on text argument supplied
- Request Arguments:
```
{
	"search":"title"
}
```
- Response: Return objects of questions matching the search parameters.
```
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

POST `'/api/play_quizzes'`

- Generate random questions base category and previous question.
- Request Arguments:
```
{
	"quiz_category":{
		"id":1
	},
	"previous_questions":[1,2]
}
```
- Response: Returns an object containing questions, answers and category_id
```
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```




## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)