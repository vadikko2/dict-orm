# My First Dict ORM
This is super simple dict ORM.  This GIST shows how to use property for describe data models.

### Use example

1. Import BaseModel and declare dict database
```python
from typing import Type

from orm_controllers import DictBaseController
from orm_models import BaseModel
from orm_objects import BaseObject
from orm_types import Str, Age

db = {
    'employees': [
        {
            'name': 'Vadim',
            'lastname': 'Kozyrevskii',
            'position': 'Python Programmer',
            'age': 26
        },
        {
            'name': 'Alex',
            'lastname': 'Alyinic',
            'position': 'C++/Qt Programmer',
            'age': 32
        },
        {
            'name': 'Alexei',
            'lastname': 'Vasiliev',
            'position': 'C/C++ Programmer',
            'age': 40
        }
    ]
}
```

2. Declare Employee model
```python
class EmployeeModel(BaseModel):
    __table_name__ = "employees"

    name = Str(name='name')
    lastname = Str(name='lastname')
    age = Age(name='age')
    position = Str(name='position')
```

4. Connect to database and create ObjectClass
```python
if __name__ == '__main__':
    # Connect to db
    DictBaseController.connect(db=db)
    # Create Object class
    EmployeeObject = EmployeeModel.get_object(controller=DictBaseController)  # type: Type[BaseObject]

```

5. Do some tests
```python
    # ------------------ SELECT FRO DB ------------------

    ems = EmployeeObject.objects.select(
        attrs=(
            EmployeeModel.name, EmployeeModel.lastname,
            EmployeeModel.age, EmployeeModel.position
        ),
        filters=[
            (EmployeeModel.age, lambda x: x > 30),
            (EmployeeModel.position, lambda x: 'C++' in x)
        ]
    )

    for em in ems:
        print(em)

    print('\n')

    # Result:
    # <EmployeeObject: (position='C++/Qt Programmer', name='Alex', lastname='Alyinic', age=32)>
    # <EmployeeObject: (position='C/C++ Programmer', name='Alexei', lastname='Vasiliev', age=40)>

    # ------------------ CREATE NEW EMPLOYEE ------------------

    test_em = EmployeeObject(
        name='TestName', lastname='TestLastName', age=42,
        position='TestPosition'
    )  # type: BaseObject

    print(test_em.as_dict())
    print('\n')

    # Result: {'name': 'TestName', 'position': 'TestPosition', 'lastname': 'TestLastName', 'age': 42}

    # ------------------ INSERT AND AFTER THAT SELECT NEW EMPLOYEE FROM DB ------------------

    EmployeeObject.objects.insert(row=test_em)

    test_ems = EmployeeObject.objects.select(
        attrs=(
            EmployeeModel.name, EmployeeModel.lastname,
            EmployeeModel.age, EmployeeModel.position
        ),
        filters=[
            (EmployeeModel.name, lambda x: x == test_em.name.value)
        ]
    )

    for em in test_ems:
        print(em)
    print('\n')

    # Result: <BaseObject: (position='TestPosition', age=42, lastname='TestLastName', name='TestName')>

    # ------------------ BULK INSERT AND AFTER THAT SELECT NEW EMPLOYEES FROM DB ------------------

    bi_test_ems = [
        EmployeeObject(
            name='TestName%s' % i, lastname='TestLastName%s' % i,
            age=42 + i, position='TestPosition%s' % i)
        for i in range(10)
    ]

    EmployeeObject.objects.bulk_insert(rows=bi_test_ems)

    gotten_test_ems = EmployeeObject.objects.select(
        attrs=(
            EmployeeModel.name, EmployeeModel.lastname,
            EmployeeModel.age, EmployeeModel.position
        ),
        filters=[
            (EmployeeModel.name, lambda x: x.startswith('TestName'))
        ]
    )

    for em in gotten_test_ems:
        print(em)
    print('\n')

    # Result:
    # <BaseObject: (position='TestPosition', name='TestName', lastname='TestLastName', age=42)>
    # <BaseObject: (position='TestPosition0', name='TestName0', lastname='TestLastName0', age=42)>
    # <BaseObject: (position='TestPosition1', name='TestName1', lastname='TestLastName1', age=43)>
    # <BaseObject: (position='TestPosition2', name='TestName2', lastname='TestLastName2', age=44)>
    # <BaseObject: (position='TestPosition3', name='TestName3', lastname='TestLastName3', age=45)>
    # <BaseObject: (position='TestPosition4', name='TestName4', lastname='TestLastName4', age=46)>
    # <BaseObject: (position='TestPosition5', name='TestName5', lastname='TestLastName5', age=47)>
    # <BaseObject: (position='TestPosition6', name='TestName6', lastname='TestLastName6', age=48)>
    # <BaseObject: (position='TestPosition7', name='TestName7', lastname='TestLastName7', age=49)>
    # <BaseObject: (position='TestPosition8', name='TestName8', lastname='TestLastName8', age=50)>
    # <BaseObject: (position='TestPosition9', name='TestName9', lastname='TestLastName9', age=51)>

    # Disconnect from db
    DictBaseController.disconnect()
```
