# Back-End Developer Skills Test

## Goals

The purpose of these tasks is to simulate routine data problems we deal with at the Growth Lab on a daily basis. We understand that it can be challenging to demonstrate back-end skills through a portfolio of work as it is often proprietary, so we use these exercises to create a more level playing field for candidates.

We are looking to get better insight into your skills with data manipulation, data analysis, and web frameworks; as well as getting a look into how you approach problems and your overall process.

Some questions we'll be looking to assess are:
- Can you write code to solve a problem?
- Can you look up and learn how to do something that you might not necessarily know yet?
- Are you aware of the basic concepts, tools, and techniques in the problem area?
- Are you aware of general best practices when writing software?

Some criteria we'll be using along the way:
- Does it work? Is it complete? Are there mistakes or problems in the result, and if so, how major?
- Is this a reasonable and expedient way to solve this problem? Are there better tools or methods that could be used? Does it generally follow good engineering principles?
- Can you explain how it works and why you chose to do things the way you did? Additionally, does the code demonstrate an understanding of the problem and competency in the tools being used?
- Is the code reasonably well-formatted and readable?
- Is the logic easy to follow?

## Logistics

Once you complete these exercises, send us your code and any output that is generated along the way. You can email us a compressed directory of files, create a [GitHub Gist](https://gist.github.com/), or use whatever method you think is the best way to share with us.

We then schedule some time to sit down with you and debrief on the process. We're interested in the approaches you took, the code you wrote, the choices you made, what you think you would improve upon in the future and how, and anything else that comes up.

## Stack
On our team, we use Python for back-end codebases and have a strong preference for candidates who can demonstrate Python skills. Beyond that, you can use whatever packages or frameworks you are comfortable with and think are appropriate for completing these tasks.

For reference, we often use the following on the team:
- Pandas
- Flask
- SQLAlchemy
- NumPy
- Graphene

We also use PostgreSQL databases on the team, but you are by no means required to host any sort of database or server to complete these exercises. All tasks can be completed on your local machine.

## Guidelines
- We expect these tasks should take approximately a combined 1-2 hours, depending on experience. There is no penalty for going over (we aren't timing you!), but we also don't want to take up too much of your free time.
- Please complete these exercises on your own without collaboration from or sharing with anyone else. However, you are free to look up documentation or search for resources online that may help you complete the tasks.
    - Yes, Stack Overflow is allowed.
    - We're interested in your process, so if you find something that you this is useful, stick the URL in a comment to show us how you approached it!
- There are no trick questions and no "correct" approach to solve any of these tasks.
- If you don't know how to do something, **don't panic**. Start with a general plan of what you'd like to do, and complete as much as you can. Part of this work involves researching, learning, and attempting new problems to the best of your abilities. Not everyone knows how to do everything, so show us as much as you can do!
- Keeping notes on what you did throughout the process isn't necessary, but can be helpful when we discuss these exercises once you finish. This is especially true for parts where you ran into trouble!

## Exercises

### The Data
Within this directory is an extract of data we have compiled and cleaned in the course of our work that we obtained from the [US Census Bureau](https://www.census.gov). This dataset describes state populations and state-to-state migration flows from the decade between 2010 and 2019. We recommend using the "Download ZIP" functionality from GitHub to easily download all the necessary datasets in this directory.

The [Census Bureau classifies](https://www2.census.gov/geo/pdfs/maps-data/maps/reference/us_regdiv.pdf) states into 9 geographical divisions, which are in turn classified into 4 regions. The file `census_classification.csv` describes these relationships. Each row represents one entity that has a `level` of one of `(state, division, region)` with a unique `id`. Each state and division row also has a `parent_id` which corresponds to the `id` of its parent one level up. These relationships can be used to traverse the resulting hierarchical tree.

Each row of data found in `census_migration_data.csv` describes the `estimate` of the amount of people who moved from one state (`previous_state`) to anothere state (`current_state`) in a given `year` between 2010 and 2019. This is also informed by a `margin_of_error` describing the range of what the true value of the `estimate` may be.

Finally, `state_populations.csv` gives the population of each state for each year within the observation period.

### Task 1: Aggregate Data
Let's say once we have obtained this dataset, we are interested in first examining high-level trends of migration flows within the US. We need you to produce an aggregated dataset showing the summed estimates of people moving from a previous Census `division` to their current Census `region` for each year. You can drop `margin_of_error` for this task.

The output for this task should be a CSV named `aggregated_migration.csv` with each row being a division-to-region pair for a given year. As you are aggregating fields from the `state` level, feel free to rename columns to something more accurate and descriptive as necessary.

### Task 2: Analyze Data
While a lot of the work of the Growth Lab happens in partnership with national governments, we also occassionally work with state and local governments internationally. Let's say for this task we are working on a hypothetical project with the state of North Carolina (NC).

Looking solely at rows in the raw data where the `current_state` is North Carolina, we need you to generate a CSV called `nc_migration.csv` where each row corresponds to a `year` and has additional columns answering the following questions:
- Which state had the largest number of people move to North Carolina that year?
- Which state had the largest proportion of its own population move to North Carolina that year?
- How many states had at least 10,000 people move to North Carolina that year?
- What percentage of people who migrated to North Carolina that year came from outside of the South Atlantic division?

In the output file, it is fine to use state abbreviations when applicable instead of full names if more convenient. Name columns something descriptive but concise. You can also use the `estimate` field for all questions and do not need to incorporate `margin_of_error` in this task.

### Task 3: Build a Web API
Now that we have completed some initial data manipulation, we want to build an API that exposes Census Bureau migration data to users. To keep it simple, let's stick with our preivous scenario where we're working on a project in collaboration with the state of North Carolina and thus only interested in rows where the `current_state` is NC.

Write the code to run a web server (locally is fine) where a user can call a specific URL to perform a query. You are encouraged to use an existing framework (Flask, Django, Graphene, etc.) to simplify this.

In addition to provided fields, we also want to generate lower- and upper-bounds for the estimates using the `margin_of_error`. These can be calculated by adding or subtracting `margin_of_error` from the `estimate` (with a floor at 0).

Each row should return the following fields:
- `previous_state`: 2-character state abbreviation
- `year`
- `estimate`
- `estimate_lb`: `estimate - margin_of_error`
- `estimate_ub`: `estimate + margin_of_error`

The types of endpoints we want to build are as follows:
```
/previous_state/<id>/
/previous_state/<id>/<year>/
/previous_division/<id>/
/previous_division/<id>/<year>/
```
As a general approach, we suggest you tackle this with the following steps:

0. Make sure you have created a subset of data limited to North Carolina as the `current_state` to work with.
1. Write a function that takes a required `id` for the previous state and an optional `year` and returns the rows of data associated with only that combination of variables.
2. Write a function that takes a required `id` for the previous Census division and an optional `year` and returns the row of data associated with only that combination of variables.
3. Write some additional code that wraps those functions into individual routes in a web API and returns rows of JSON data.

Note: We write an maintain both REST (using Flask) and GraphQL (using Flask + Graphene) APIs on our team depending on the tool. Your API can use either of these architectures and you can make modifications to the instructions as necessary to query, especially if you choose to use GraphQL. Just let us know what routes or queries we need to use to access data when reviewing your code if different from above.
