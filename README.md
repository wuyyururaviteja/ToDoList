# ToDoList

I wanted to have a good To Do list to mark my tasks faster than remembering all my tasks and brainstormimg myself.
So i tried and checked various online todo lists few are good but are too complicated and few are longer and tedious ones. Few tools are simpler but due to free account and login many of the capabilities are out of reach.

Then struck a thought in my mind. AI has developed a lot recently so may be i can ask chatgpt in writing code rather than typing tedious closing and opening html braces. So I have started to take help from my coding buddy and design a tool in a way i feel will be useful.

# UseCase
My usecase is too simple I need to have a website format of todolist which remembers the tasks even after I restart my system and always running. I need implementations like add a task, add a category, delete a category and filter the tasks.

# D&D ( Designing and Developing )
Note : This just describes my analysis and reworking to make the design a step better. Long content that can be skippable.

My first case was i need it in a web format so while exploring i have come across a flask server kind of implementation. As I have a good knowledge in Python I have decided to use Flask Server for my kind of mini automation. I have asked ChatGPT to design a todolist app with Flask implementation code. Ding.... It has given me 2 files one was my app file and another was my HTML file to render. Ok now the task addition is good.

Here comes the next part, I wanted my tasks in a way that it shows me the time taken for a task also. So I have added a logic to add the time created and time completed and upon completion i have started sending the time taken param. 

Next step was to add a filter so I can view what tasks are completed and what are pending etc. So next query to my partner to add a filtering logic. As expected it has added the filter criteria in request and sent the request so it worked fine. 

Then a notification struck asking me to look into something on priority, then I realised a todo list is never done with no priorities. So I took a step forward and asked GPT to add a priority and category filter too. Hushhh... filter is added but what about the categories, I asked chatGPT to finish that also. Now when i checked the code it added a static list like Work,Personal,Analysis. But I dont want to restrict my self to these limited categories. So as usual added them too. 

Here comes the next part of my usecase where i want my tasks to be available after restart. So I explored this and found may be a database would be a better addition. Butttt can all devices have a database ? May be yes or no so I thought of going old school and a file writing model. Which updated everything in a file and after restart it just fetches from file and shows. May be i can do the same for categories also. So i have added a 2 new files for storing the details. 

Hurray the project is done. But i thought may be I need to tweek UI a bit and started changing the HTML, CSS, JS. Finally i changed the implementation and my project is ready to use. This is my version 1 of TodoList.

<img width="1512" alt="Screenshot 2025-01-10 at 16 24 32" src="https://github.com/user-attachments/assets/a762d7f0-0ec8-4a30-86b1-8f55203db8ec" />
