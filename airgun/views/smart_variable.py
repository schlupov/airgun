from widgetastic.widget import (
    Checkbox,
    Select,
    Text,
    TextInput,
    View,
    ConditionalSwitchableView,
)
from widgetastic_patternfly import BreadCrumb
from airgun.views.common import (
    BaseLoggedInView,
    SearchableViewMixin,
    SatTab,
    SatVerticalTab,
)
from airgun.widgets import (
    FilteredDropdown,
    ActionsDropdown,
    SatTable,
)


class SmartVariableView(BaseLoggedInView, SearchableViewMixin):

    """
    Basic view after clicking Configure->Smart Variables.
    In basic view, there can be seen title smart variables, button
    create smart variable (new) and table with existing smart variables
    """

    title = Text("//h1[text()='Smart Variables']")
    new = Text("//a[contains(@href, '/variable_lookup_keys/new')]")
    table = SatTable(
        './/table',
        column_widgets={
            'Variable': Text("//a[starts-with(@data-id,'aid_variable_lookup_keys_') and contains(@data-id,'_edit')]"),
            'Actions': Text("//*[contains(@data-confirm,'Delete')]"),
        }
    )

    @property
    def is_displayed(self):
        """Check if the right page is displayed"""
        return self.browser.wait_for_element(
            self.title, exception=False) is not None


class PuppetClassesView(BaseLoggedInView, SearchableViewMixin):

    """
    Basic view after clicking Configure->Classes.
    In basic view, there can be seen title Puppet Classes, button
    import environments from host (import) and
    table with existing Class names
    """

    title = Text("//h1[text()='Puppet Classes']")
    import_environments = Text("//a[contains(@href, '/puppetclasses/import')]")
    table = SatTable(
        './/table',
        column_widgets={
            'Class name': Text("./a"),
        }
    )

    @property
    def is_displayed(self):
        """Check if the right page is displayed"""
        return self.browser.wait_for_element(
            self.title, exception=False) is not None


class ChangedEnvironmentsView(BaseLoggedInView, SearchableViewMixin):

    """
    View after clicking on import environments in puppet classes
    """

    title = Text("//h1[text()='Changed environments']")
    update = Text('//input[@name="commit"]')
    checkbox_development = Checkbox(id='changed_new_development')
    table = SatTable(
        './/table',
        column_widgets={
            'Environment': Text('./a'),
        }
    )

    @property
    def is_displayed(self):
        """Check if the right page is displayed"""
        return self.browser.wait_for_element(
            self.title, exception=False) is not None


class SmartVariableCreateView(BaseLoggedInView):

    """
    Details view of page with boxes that have to be filled in to
    create a new smart variable
    """

    key = TextInput(id='variable_lookup_key_key')
    description = TextInput(id='variable_lookup_key_description')
    puppet_class = FilteredDropdown(
        id='s2id_variable_lookup_key_puppetclass_id')
    key_type = Select(id='variable_lookup_key_key_type')
    default_value = TextInput(id='variable_lookup_key_default_value')
    hidden_value = Checkbox(id='variable_lookup_key_hidden_value')
    expander = Text("//*[@class='caret']")
    validator_type = Select(id='variable_lookup_key_validator_type')
    order = TextInput(id='order')
    merge_overrides = Checkbox(id='variable_lookup_key_merge_overrides')
    merge_default = Checkbox(id='variable_lookup_key_merge_default')
    avoid_duplicates = Checkbox(id='variable_lookup_key_avoid_duplicates')
    add_matcher = Text(
        "//a[contains(@data-association, 'lookup_values')]")
    submit = Text('//input[@name="commit"]')

    @property
    def is_displayed(self):
        """Check if the right page is displayed"""
        return self.browser.wait_for_element(
            self.key, exception=False) is not None


class EditPuppetClassView(BaseLoggedInView):

    """
    Details view of page after clicking on puppet class name
    to edit puppet class and create new smart variable in
    the tab Smart Variables
    """

    breadcrumb = BreadCrumb()

    @property
    def is_displayed(self):
        breadcrumb_loaded = self.browser.wait_for_element(
            self.breadcrumb, exception=False)
        return (
                breadcrumb_loaded
                and self.breadcrumb.locations[0] == 'Puppetclasses'
                and self.breadcrumb.read().starts_with('Edit Puppet Class ')
        )

    @View.nested
    class smartvariables(SatTab):
        TAB_NAME = 'Smart Variables'
        title = Text("//h2[text()='Parameter Details']")
        add_variable = Text("//*[contains(@data-association,'lookup_keys')]")
        key = TextInput(
            locator="//input[starts-with(@id,'puppetclass_lookup_keys_attributes_') and @type='text']")
        description = TextInput(
            locator="//textarea[contains(@id,'_description') and contains(@name,'[description]')]")
        key_type = Select(
            "//select[contains(@id,'_key_type') and contains(@name,'[key_type]')]")
        default_value = TextInput(
            locator="//textarea[contains(@id,'_default_value') and contains(@name,'[default_value]')]")
        hidden_value = Checkbox(
            locator="//input[contains(@id,'_hidden_value') and contains(@name,'[hidden_value]')]")
        expander = Text("//*[@class='caret']")
        validator_type = Select(id='variable_lookup_key_validator_type')
        order = TextInput(id='order')
        merge_overrides = Checkbox(
            "//input[contains(@id,'_merge_overrides') and contains(@name,'[merge_overrides]')]")
        merge_default = Checkbox(
            "//input[contains(@id,'_merge_default') and contains(@name,'[merge_default]')]")
        avoid_duplicates = Checkbox(
            "//input[contains(@id,'_avoid_duplicates') and contains(@name,'[avoid_duplicates]')]")
        add_matcher = Text(
            "//*[@data-original-title='add a new matcher']")
        matcher_value = TextInput(locator="//input[contains(@class,'matcher_value')]")
        submit = Text('//input[@name="commit"]')
