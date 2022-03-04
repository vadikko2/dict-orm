# my-first-orm
This is super simple dict ORM.  This GIST shows how to use property for describe data models.

Example:

```python
from orm_controllers import DictBaseController
from orm_models import BaseModel
from orm_objects import DictBaseObject
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


class EmployeeModel(BaseModel):
    __table_name__ = "employees"

    name = Str(name='name')
    lastname = Str(name='lastname')
    age = Age(name='age')
    position = Str(name='position')


class EmployeeObject(DictBaseObject):
    """Object class for EmployeeModel"""
    __model__ = EmployeeModel


if __name__ == '__main__':

    DictBaseController.connect(db=db)

    em = EmployeeObject(name='TestName', lastname='TestLastName', age=42, position='TestPosition')
    print(em)
    print('\n')

    # Result: <EmployeeObject: (position='TestPosition', age=42, lastname='TestLastName', name='TestName')>

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

    # Result:
    # <EmployeeObject: (position='C++/Qt Programmer', name='Alex', lastname='Alyinic', age=32)>
    # <EmployeeObject: (position='C/C++ Programmer', name='Alexei', lastname='Vasiliev', age=40)>

```
