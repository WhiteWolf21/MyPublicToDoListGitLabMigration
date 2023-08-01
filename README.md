# My Public To Do List (New Migrated Version with README.md for Software Testing)

### Isolation Test and Explicit Wait

#### Isolation Test Process
LiveServerTestCase is a class which launches a live Django server in the background on setup and shut the server down on teardown. This class allows us to automate test using Selenium client to execute a series of functional test.

LiveServerTestCase launches a live django server on `localhost:8081` by default. We can access the url by calling `live_server_url`.

#### Refactoring time.sleep
On the previous exercise, we explicitly write on our functional test `time.sleep(1)` every time we hit new to-do item. The question is how do we assure that 1s is accurate enough to wait until our todo-item appears on the page? 

So, on this exercise we refactor the way we wait to-do item until it appears. Instead giving particular number of second, we approach setting the maximum number of second we tolerate, in this case 10s. The selenium would re-read the page if the new to-do item didn't appear and if the waiting time reach 10s, the program will raise another kind of error message.

The waiting step now takes place on `check_for_row_in_list_table` function. Thus, we can remove `time.sleep(1)` every time we hit to-do item.

##### References
- [LiveServerTestCase Docs](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#liveservertestcase)
- [ObeyTheTestingGoat](https://www.obeythetestinggoat.com/book/chapter_explicit_waits_1.html)

### Prettification

This exercise guides us to add styling to our to-do list application. First, we add functional test that checks our css. Since, I want to add font-styling to the app and special font title h1, I write 2 tests that checks whether h1 and body's font family return correct font, also I check the font weight on title. I add two CSS file, the `index.less` would pass the functional test and `wrong.less` would fail.

In this exercise, I also explore myself to use Less, dynamic preprocessor style sheet language. I love using Less since I could beautify my CSS with indentation, and reuse code (in this exercise, I don't do this). 

Little note: One thing confuses me is the anomaly of Selenium. I still can't figure out why every time the functional test runs, it could outcome different output, at some time it returns OK but in another time it returns an error.

### Input Validation and Test Organization

#### Between Refactoring Practices and Clean Code
On TDD Practice, we aware there are 3 stages; RED indicate we write our test first and it fails; GREEN indicate we write some implementation codes to pass the test; and REFACTOR self explanatory. Often times, we pass through the refactor stage as the implementation pass the test within mind. This is not violating any rule or best practices as if the implementation codes as clean as possible. But, often times the process of writing the implementation codes prone to merely passing the test without considering any code smells. The refactor stage thus encourage developer to rewrite the implementation code without violating the test.

#### Test Organization
Test organization we've did on this exercise provide us easiness to re-read what our test is doing. Functional tests file organized by separating user story into a file, while the unit test file organized by separating between view test and model test in a directory containing those files. Besides the cleaner and modularized test in one file, we also able to run specific test file which reduces running time for testing and omit unnecessary test we're not working on.


### Spiking, De Spiking

**Spiking** is a technique to let us code without implementing Test Driven Development (TDD) approach. It allows us to explore new technology (or something we are not good at) at very first time without write tests so we could be focus to learn. But, it doesn't mean we violate the 'culture' to implement TDD approach because Spiking must be conducted in another branch. And we should go back to the master (or development) branch to re-write our codes from scratch and also by implementing TDD approach. And this is called **De-spiking**.

This technique makes common sense since we can't force people to write a test when they don't even know how to program it.

### Testing Database Migrations

##### Why is data migration required?
In a real application, at some point we want to add/change some constraints on our database like one from this story, we want to add a unique constraint on our existing column; without removing existing data. In order to do it, we have to be very careful because we need to be mindful of how long our migrations are going to take. Hence, we need to test it in our local. But, beware of the fact that our production database would probably have more data than our local. So, make sure the way we test it represents how the migrations would behave on the production one.

Also, always run all the functionality test after doing data migrations to ensure everything as we're expected.

##### Populating data
I use data migration approach to dump 100 data. I create a function to generate randomly data. Here is the code.

```python
def dump_data(apps, schema_editor):
    List = apps.get_model("lists", "List")
    Item = apps.get_model("lists", "Item")
    for i in range(10):
        _list = List.objects.create()
        for j in range(10):
            data = Item.objects.create(text='dump-data-' + str(j), list=_list)
```

In my experiment when populating these data, I haven't found any delayed time. I guess it is because both local and production data this application has not that much.