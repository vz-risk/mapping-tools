from sqlalchemy.schema import Column

#TODO: where does this go?
def _cast_columns_as_properties(properties):
    casted_properties = {}
    for prop_name, prop in properties.items():
        if isinstance(prop, Column):
            casted_properties[prop_name] = ColumnProperty(prop)

    return casted_properties

class Mapper:

    def __init__(self, model, table, properties):
        self._table = table
        properties.update(_cast_columns_as_properties(properties))
        properties.update(self._automap_unmapped_columns(table, properties))
        self.composite_property = CompositeProperty(model, properties)

    @property
    def table(self):
        return self._table

    @property
    def columns(self):
        #TODO: if this is returning sqla columns, it should probably use the
        #table interface instead
        return self.composite_property.columns

    @staticmethod
    def _automap_unmapped_columns(table, properties):
        automapped_properties = {}
        unmapped_column_names = set(table.columns.keys())
        for prop in properties.values():
            unmapped_column_names -= set(c.name for c in prop.columns)
        for name in unmapped_column_names:
            automapped_properties[name] = ColumnProperty(table.columns[name])

        return automapped_properties

    def load(self, row):
        return self.composite_property.load(row)

    def dump(self, obj):
        return self.composite_property.dump(obj)

class CompositeProperty:

    def __init__(self, model, properties):
        self.model = model
        properties.update(_cast_columns_as_properties(properties))
        self.properties = properties

    @property
    def columns(self):
        columns = []
        for prop in self.properties.values():
            columns.extend(prop.columns)

        return columns

    def dump(self, obj):
        row = {}
        for prop_name, prop in self.properties.items():
            value = getattr(obj, prop_name)
            row.update(prop.dump(value))

        return row

    def load(self, row):
        model_kwargs = {}
        for prop_name, prop in self.properties.items():
            model_kwargs[prop_name] = prop.load(row)

        return self.model(**model_kwargs)

class ColumnProperty:

    def __init__(self, column):
        self.column = column

    @property
    def columns(self):
        return (self.column,)

    def dump(self, value):
        return {self.column.name:value}

    def load(self, row):
        return row[self.column]

