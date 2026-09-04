# Schedule Generator
WebSite: <a> https://fabrizzio1235.pythonanywhere.com/ </a> | Available until: Sunday 04 October 2026
#### Description:

This project was created with the principal purpose to help students who want to create their perfect schedule. In my school, the administration gave us an Excel file. In that document, there are a lot of subjects and it is very complicated to find your personal schedule. You spend a lot of time checking every teacher, checking if they don't overlap with each other, etc. Many problems! With my app, you can easily generate schedules in a matter of minutes or even seconds. You only have to submit your schedule in the correct format (specified there), then you select your subjects, and finally your teachers. The app will create the possible schedules. If it is not possible, the app will let you know. To be honest, I don't really know how it works in other countries (selecting your schedule and not being assigned by the administration). But at my university, student have to form your schedule using the Excel file provided by the administration.

### Static Files

* **generator.js**: This file shows the user their schedule with their selections of teachers and subjects. It also lets them switch between other possible schedules generated with those preferences.
* **selectsubjects.js**: This file manages the logic of subject selection and manages the search filter.
* **styles.css**: This is the only CSS file used in the project and obviously handles the project decoration.

### Templates

* **filter.html**: This is the layout of the Subject Selector. It shows all the subjects from the file submitted by the user in the submit.html page. This file is related to selectsubjects.js to manage the logic and interaction with the layout.
* **generator.html**: This file shows 2 things. First, it shows the subjects selected by the user; they have to select one teacher per subject. Once selected, they should press the "Generate" button. If the schedule is possible (there is no overlap), it shows the generated schedule and the quantity of possible schedules. Otherwise, it will show a message to let the user know that the combination of teachers is not possible (they have to select other teachers or change some subjects). This file is related to the generator.js file.
* **index.html**: This file is the simple beginning of the page. It is only the presentation, the first impression for the user of my website.
* **submit.html**: This file shows the user the steps to submit their document of subjects/teachers. It explains in detail the requirements their documents must have to generate the schedules. If there is a problem in the document, the web will let the user know.
* **layout.html**: This file is literally the layout for the other HTML files, just to simplify the code and declare the basic things of every web page.

### Backend and Configuration

* **app.py**: This document is the core of the project. It handles how the web pages connect to each other and how we use the user's input, such as files, types, selections, etc.
* **db.py**: Configuration for the database.
* **requirements.txt**: This file lists the required libraries that this project needs installed to run correctly.
* **schedule.db**: If the user's file is submitted correctly (everything is recognized), it generates schedule.db, a database that contains only the necessary data for the project, like the days of the week, teacher's name, and IDs.

### Design Choices

During the development, I made some important decisions to make sure the app works correctly and gives a good experience to the user:

**1. Using Pandas for Data Management:**
At first, I thought about using the normal `csv` library of Python. But I chose **Pandas** because it works better with Excel files (`.xlsx`), which are very common in schools. Pandas makes it easier to clean the data (like handling empty values) and read the rows, so the system doesn't crash if the user's file has small errors.

**2. Combination Algorithm (Itertools):**
To make the schedules, I used `itertools.product`. This was very important because I needed a fast way to mix all the selected subjects to find combinations. Even if this process is heavy for big data, for a normal schedule (5-8 subjects), it is very fast and guarantees that we don't miss any possible combination.

**3. Database vs. In-Memory:**
I decided to use temporary tables in SQLite (`scheduleCopy1`, `scheduleCopy2`) instead of saving big lists in the Flask session or global variables. This keeps the app organized and saves the user's selection (filtering by subject first, then by teacher) correctly between the different pages.

**4. Block-Based Interface (Divs) vs. Tables:**
Even though it is a schedule, I decided not to use a strict `<table>` structure for the content. Instead, I use `<td>` columns as containers and put independent `div` elements (`.class-block`) inside them. This allowed me to use better styles like rounded borders, shadows, and spaces between subjects—this is hard to do with normal table cells. Also, it lets subjects "stack" naturally if there is more than one on the same day.

**5. Backend Data Validation:**
I used Regex in `app.py` (`validateHour`) to check the time format strictly. I chose to do this in the backend instead of the frontend to be sure the data is correct before saving it to the database. This avoids errors when generating the schedules if a user uploads a file with bad time formats.

**6. Simplification of HTML (Jinja2):**
To avoid writing the same code many times, I used Jinja2 templates (like `layout.html`). This allowed me to create a base structure for all the pages. So, instead of repeating the head, header, and footer in every HTML file, I just extended the layout. This makes the code much simpler and easier to read.


