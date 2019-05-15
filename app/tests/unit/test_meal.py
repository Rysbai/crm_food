import mock
import unittest
from app.models.meal import Department, MealsCategory, Meal


class MealsModelTest(unittest.TestCase):

    def test_should_return_just_department_name(self):
        department_name = "Bar"

        mock_instance = mock.Mock(spec=Department)
        mock_instance.name = department_name
        self.assertEqual(Department.__str__(mock_instance), department_name)

    def test_should_return_just_meals_category_name(self):
        department_name = "Bar"
        meals_category_name = "Example Category #"

        mock_department = mock.Mock(spec=Department)
        mock_department.name = department_name

        mock_instance = mock.Mock(spec=MealsCategory)
        mock_instance.department = mock_department
        mock_instance.name = meals_category_name

        self.assertEqual(MealsCategory.__str__(mock_instance), meals_category_name)

    def test_should_return_just_meal_name(self):
        department_name = "Bar"
        meals_category_name = "Example Category #"
        meal_name = "Plov"

        mock_department = mock.Mock(spec=Department)
        mock_department.name = department_name

        mock_meals_category = mock.Mock(spec=MealsCategory)
        mock_meals_category.department = mock_department
        mock_meals_category.name = meals_category_name

        mock_instance = mock.Mock(spec=Meal)
        mock_instance.category = mock_meals_category
        mock_instance.name = meal_name

        self.assertEqual(Meal.__str__(mock_instance), meal_name)
