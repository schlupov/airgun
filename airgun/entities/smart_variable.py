from navmazing import NavigateToSibling
from airgun.entities.base import BaseEntity
from widgetastic.widget import Table


from airgun.navigation import (
    NavigateStep,
    navigator
)

from airgun.views.smart_variable import (
    SmartVariableView,
    PuppetClassesView,
    SmartVariableCreateView,
    EditPuppetClassView,
    ChangedEnvironmentsView,
)


class SmartVariableEntity(BaseEntity):

    def create(self, values):
        view = self.navigate_to(self, 'New')
        view.expander.click()
        view.fill(values)
        view.submit.click()

    def search(self, value):
        view = self.navigate_to(self, 'All')
        return view.search(value)

    def edit(self, name, values):
        view = self.navigate_to(self, 'Edit', entity_name=name)
        view.fill(values)
        view.submit.click()

    def read(self, entity_name):
        view = self.navigate_to(self, 'Edit', entity_name=entity_name)
        return view.read()

    def delete(self, entity_name):
        view = self.navigate_to(self, 'All')
        view.search(entity_name)
        view.table.row(variable=entity_name)['Actions'].widget.click()
        self.browser.handle_alert()

    def create_puppet_class(self, entity_name, values):
        view = self.navigate_to(self, 'NewVariable', entity_name=entity_name)
        view.smartvariables.add_variable.click()
        view.smartvariables.expander.click()
        view.fill(values)
        view.smartvariables.submit.click()

    def import_environments(self, entity_name):
        view = self.navigate_to(self, 'import')
        view.fill(entity_name)
        view.update.click()

@navigator.register(SmartVariableEntity, 'All')
class ShowAllSmartVariables(NavigateStep):
    VIEW = SmartVariableView

    def step(self, *args, **kwargs):
        self.view.menu.select('Configure', 'Smart Variables')


@navigator.register(SmartVariableEntity, 'AllClass')
class ShowAllClasses(NavigateStep):
    VIEW = PuppetClassesView

    def step(self, *args, **kwargs):
        self.view.menu.select('Configure', 'Classes')


@navigator.register(SmartVariableEntity, 'New')
class AddNewSmartVariable(NavigateStep):
    VIEW = SmartVariableCreateView

    prerequisite = NavigateToSibling('All')

    def step(self, *args, **kwargs):
        self.parent.browser.click(self.parent.new)


@navigator.register(SmartVariableEntity, 'NewVariable')
class EditPuppetClass(NavigateStep):
    VIEW = EditPuppetClassView

    def prerequisite(self, *args, **kwargs):
        return self.navigate_to(self.obj, 'AllClass')

    def step(self, *args, **kwargs):
        entity_name = kwargs.get('entity_name')
        self.parent.search(entity_name)
        self.parent.table.row(class_name=entity_name)['Class name'].widget.click()


@navigator.register(SmartVariableEntity, 'Edit')
class EditExistingSmartVariable(NavigateStep):
    VIEW = SmartVariableCreateView

    def prerequisite(self, *args, **kwargs):
        return self.navigate_to(self.obj, 'All')

    def step(self, *args, **kwargs):
        entity_name = kwargs.get('entity_name')
        self.parent.search(entity_name)
        self.parent.table.row(variable=entity_name)['Variable'].widget.click()


@navigator.register(SmartVariableEntity, 'import')
class ImportEnvironments(NavigateStep):
    VIEW = ChangedEnvironmentsView

    def prerequisite(self, *args, **kwargs):
        return self.navigate_to(self.obj, 'AllClass')

    def step(self, *args, **kwargs):
        self.parent.import_environments.click()
