# sheng-pytutor-poc

In this repo contains a feature that represents student information as knowledge graphs to track their current knowledge status in the class. You may read more about what these graphs represent in `Graph Idea.pdf` on the `main` branch.

### Set up

1. Run `python ./KG/database_table_generator.py` to generate a table named `concepts` in the database. This will have primary key as UUID and all the rest are attributes. 

### Testing

1. Run `python ./KG/gpt_test.py` to run some tests to see what outputs the LLM model returns back to you.

### Findings:

1. The LLM is good at finding concepts used in student questions but sometimes can include somewhat irrelevant concepts. 

2. The weights are working as expected as can be seen from this tutor response:

2.1 I see that you don't have a specific weight indicating any understanding or confusion about dictionary-related concepts, which probably implies you have encountered this topic for the first time or have neutral familiarity with it. Let's start with the basics and build from there!

2.2 That's a great observation! Yes, lists in Python are mutable, meaning you can change their content after their creation. This includes the ability to add, remove, or update elements.

Let's explore this a bit further. How do you think you would change or update a value inside a list? What kind of operations or methods do you think might be available to achieve this? If you're not sure, we can explore some examples together!

